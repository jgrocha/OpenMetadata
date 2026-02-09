#  Copyright 2021 Collate
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#  http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
"""
Profiler Processor Step
"""
import traceback
from typing import Optional, cast
import validators
from urllib.parse import urlparse
from urllib.parse import parse_qs
import pandas as pd
import re
from osgeo import gdal, ogr, osr

from metadata.utils.logger import ingestion_logger
logger = ingestion_logger()

from metadata.generated.schema.entity.services.ingestionPipelines.status import (
    StackTraceError,
)
from metadata.generated.schema.metadataIngestion.databaseServiceProfilerPipeline import (
    DatabaseServiceProfilerPipeline,
)
from metadata.generated.schema.metadataIngestion.workflow import (
    OpenMetadataWorkflowConfig,
)
from metadata.ingestion.api.models import Either
from metadata.ingestion.api.parser import parse_workflow_config_gracefully
from metadata.ingestion.api.step import Step
from metadata.ingestion.api.steps import Processor
from metadata.ingestion.ometa.ometa_api import OpenMetadata
from metadata.profiler.api.models import ProfilerProcessorConfig, ProfilerResponse
from metadata.profiler.processor.core import Profiler
from metadata.profiler.source.model import ProfilerSourceAndEntity
from metadata.generated.schema.entity.data.table import (Table, ColumnName)
from metadata.sampler.pandas.pandas_profile import PandasProfiler
from metadata.generated.schema.entity.data.table import Column as EntityColumn
from metadata.generated.schema.api.data.createTable import CreateTableRequest

class ProfilerProcessor(Processor):
    """
    This processor is in charge of getting the profiler source and entity coming from
    the OpenMetadataSource and compute the metrics.
    """

    def __init__(self, config: OpenMetadataWorkflowConfig):
        super().__init__()

        self.config = config
        self.profiler_config = ProfilerProcessorConfig.model_validate(
            self.config.processor.model_dump().get("config")
        )
        self.source_config: DatabaseServiceProfilerPipeline = cast(
            DatabaseServiceProfilerPipeline, self.config.source.sourceConfig.config
        )  # Used to satisfy type checked

    @property
    def name(self) -> str:
        return "Profiler"

    def read_wfs(self, url, layer, output):
        gdal.SetConfigOption('GDAL_HTTP_UNSAFESSL', 'YES')
        gdal.UseExceptions()
        resource = "WFS:" + url

        driver_wfs = ogr.GetDriverByName("WFS")
        wfs = driver_wfs.Open(resource)
        input_layer = wfs.GetLayerByName(layer)

        driver_geojson = ogr.GetDriverByName("GeoJSON")
        outDataSource = driver_geojson.CreateDataSource(output)

        targetprj = ogr.osr.SpatialReference()
        targetprj.ImportFromEPSG(4326)

        dest_layer = outDataSource.CreateLayer(layer, targetprj, input_layer.GetLayerDefn().GetGeomType(), [])

        sourceprj = input_layer.GetSpatialRef()
        transform = osr.CoordinateTransformation(sourceprj, targetprj)

        # adding fields to new layer
        layer_definition = ogr.Feature(input_layer.GetLayerDefn())
        for i in range(layer_definition.GetFieldCount()):
            dest_layer.CreateField(layer_definition.GetFieldDefnRef(i))
        
        for feature in input_layer:
            geom = feature.GetGeometryRef()
            geom.Transform(transform)
            dest_layer.CreateFeature(feature)
        
        return True
    
    def _run(self, record: ProfilerSourceAndEntity) -> Either[ProfilerResponse]:
        profiler_runner = None

        if self.config.source.type == 'customdatabase':
            sourcePythonClass = self.config.source.serviceConnection.root.config.sourcePythonClass

            logger.info('---------------------self.config.source.serviceConnection.root.config.connectionOptions.root[nome]----------------')    
            logger.info(self.config.source.serviceConnection.root.config.connectionOptions.root['nome'])  
            base_dir = self.config.source.serviceConnection.root.config.connectionOptions.root['nome']
                
            ##Define metadata
            openMetadataServerConfig = self.config.workflowConfig.openMetadataServerConfig
            metadata = OpenMetadata(openMetadataServerConfig)

            ##Get Table with customProp's
            table = metadata.get_by_id(
                entity=Table, entity_id=record.entity.id.root, fields=['*']
            )

            if table and table.extension and table.extension.root and 'resource' in table.extension.root:
                ficheiro = table.extension.root['resource']
                
                # acrescentar se o conteúdo é válido, ié, se é um path com uma das extensões suportadas
                valid_extensions = ['csv', 'xls', 'xlsx', 'xlsm', 'xlsb', 'odf', 'ods', 'odt']
                if not any(ficheiro.endswith(ext) for ext in valid_extensions):
                    if validators.url(ficheiro):
        
                        match = re.search(r"service=wfs", ficheiro, re.IGNORECASE)  
                        if match:
                            # Dados num WFS
                            logger.info('---------------------WFS----------------')    
                            logger.info(ficheiro)
                            typename = None
                            parsed_url = urlparse(ficheiro)
                            if parsed_url.query:
                                captured_value = parse_qs(parsed_url.query)
                                typename = typename if 'typenames' not in captured_value.keys() else captured_value['typenames'][0]
                                if typename:
                                    output = '/tmp/{}.geojson'.format(typename)
                                    self.read_wfs(ficheiro, typename, output)
                                    print("A guardar camada WFS {} em {}".format(typename, output))
                                    ficheiro = output
                            
                                else:
                                    print("Não foi possível extrair o typenames do URL {}".format(ficheiro))
                                    return Either()
                        else:
                            # API normal
                            logger.info('---------------------API----------------')  
                            logger.info(ficheiro)
                            df = pd.read_json(ficheiro, orient='records', convert_dates=True)
                            df = pd.json_normalize(df['data'], sep ='_')
                            ficheiro = '/tmp/{}.xlsx'.format(table.name.root)
                            base_dir = ''
                            df.to_excel(ficheiro, index=False)
                    else:
                        return Either()

                if sourcePythonClass == 'connector.excel_connector.ExcelConnector' or sourcePythonClass == 'connector.geonetwork_connector.GeonetworkConnector':
                    profile = PandasProfiler(table, base_dir, ficheiro)

                    datatypes = profile.dfPandas.dtypes

                    columns = []

                    for index, col in enumerate(profile.col_names):
                        columns.append(
                            EntityColumn(
                                name=ColumnName(col),
                                dataType=profile.getDataType(datatypes[index])
                        ))
                    
                    column_join_table_req = CreateTableRequest(
                        name=table.name,
                        databaseSchema=table.databaseSchema.fullyQualifiedName,
                        columns=columns,
                    )
                    
                    profile.table_entity=metadata.create_or_update(data=column_join_table_req)

                    profile.setUp()
                    profileResult = profile.test_default_profiler()

                    metadata.client.put(
                        path=f"{metadata.get_suffix(Table)}/{record.entity.id.root}/tableProfile",
                        data=profileResult.model_dump_json(),
                    )
                    return Either()
            else:
                return Either()

        profiler_runner: Profiler = record.profiler_source.get_profiler_runner(
            record.entity, self.profiler_config
        )

        try:
            profile: ProfilerResponse = profiler_runner.process()
        except Exception as exc:
            self.status.failed(
                StackTraceError(
                    name=record.entity.fullyQualifiedName.root,
                    error=f"Unexpected exception processing entity {record.entity.fullyQualifiedName.root}: {exc}",
                    stackTrace=traceback.format_exc(),
                )
            )
            self.status.failures.extend(
                record.profiler_source.interface.status.failures
            )
        else:
            # at this point we know we have an interface variable since we the `try` block above didn't raise
            self.status.failures.extend(record.profiler_source.interface.status.failures)  # type: ignore
            return Either(right=profile)
        finally:
            profiler_runner.close()

        return Either()

    @classmethod
    def create(
        cls, config_dict: dict, _: OpenMetadata, pipeline_name: Optional[str] = None
    ) -> "Step":
        config = parse_workflow_config_gracefully(config_dict)
        return cls(config=config)

    def close(self) -> None:
        """We are already closing the connections after each execution"""
