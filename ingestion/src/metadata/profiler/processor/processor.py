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

from venv import logger
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

            if 'resource' in table.extension.root:
                ficheiro = table.extension.root['resource']
                
                # acrescentar se o conteúdo é válido, ié, se é um path com uma das extensões suportadas
                valid_extensions = ['xls', 'xlsx', 'xlsm', 'xlsb', 'odf', 'ods', 'odt']
                if not any(ficheiro.endswith(ext) for ext in valid_extensions):
                    return Either()

                if sourcePythonClass == 'connector.excel_connector.ExcelConnector':
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
                    table_entity=metadata.create_or_update(data=column_join_table_req)

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
