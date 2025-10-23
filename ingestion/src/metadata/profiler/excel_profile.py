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
Excel Profiler
"""
import os
import sys
from datetime import datetime
from unittest import TestCase, mock
from unittest.mock import Mock, patch
from uuid import uuid4
from venv import logger

import pytest
import sqlalchemy.types
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

from metadata.generated.schema.api.data.createTableProfile import (
    CreateTableProfileRequest,
)
from metadata.generated.schema.entity.data.table import Column as EntityColumn
from metadata.generated.schema.entity.data.table import (
    ColumnName,
    ColumnProfile,
    ColumnProfilerConfig,
    DataType,
    Histogram,
    Table,
    TableProfile,
    TableProfilerConfig,
)
from metadata.generated.schema.entity.services.connections.database.datalakeConnection import (
    DatalakeConnection,
)
from metadata.generated.schema.type.basic import Timestamp
from metadata.generated.schema.type.entityReference import EntityReference
from metadata.ingestion.source import sqa_types
from metadata.profiler.interface.pandas.profiler_interface import (
    PandasProfilerInterface,
)
from metadata.profiler.metrics.core import MetricTypes, add_props
from metadata.profiler.metrics.registry import Metrics
from metadata.profiler.processor.core import MissingMetricException, Profiler
from metadata.profiler.processor.default import DefaultProfiler
from metadata.sampler.pandas.sampler import DatalakeSampler
from metadata.sampler.models import SampleConfig
from metadata.data_quality.builders.validator_builder import (SourceType,ValidatorBuilder,)

import pandas as pd

Base = declarative_base()


if sys.version_info < (3, 9):
    pytest.skip(
        "requires python 3.9+ due to incompatibility with object patch",
        allow_module_level=True,
    )

class FakeClient:
    def __init__(self):
        self._client = None


class FakeConnection:
    def __init__(self):
        self.client = FakeClient()


class ExcelProfiler(TestCase):
    """
    Run checks on different metrics
    """
    table_entity = None
    dfPandas = None
    # csv_dir = "/home/utilizador/Desktop/Work/profile/custom_excel"
    # csv_dir = "/tmp"
    validator = None

    def __init__(self, table: Table, base: str, fileName: str, validator: ValidatorBuilder):
        self.table_entity = table
        self.setTable(table)
        self.setValidator(ValidatorBuilder)

        base_path = os.path.join(os.getenv("HOME"), 'nextcloud', base, fileName)
        
        logger.info(base_path)          
        
        check_path = os.path.join(os.getenv("HOME"), 'nextcloud', base, 'etl', fileName)
        
        logger.info(check_path)          
        
        if os.path.isfile(check_path):
            resource = check_path
        else:
            resource = base_path        

        dfPandas = pd.read_excel(resource) #, skiprows=6)
        self.setDataFrame(dfPandas)

    @classmethod
    @mock.patch(
        "metadata.profiler.interface.profiler_interface.get_ssl_connection",
        return_value=FakeConnection(),
    )
    @mock.patch(
        "metadata.sampler.sampler_interface.get_ssl_connection",
        return_value=FakeConnection(),
    )
    def setUp(cls, mock_get_connection, *_) -> None:
        from metadata.data_quality.interface.pandas.pandas_test_suite_interface import (PandasTestSuiteInterface,)

        with (
            patch.object(
                DatalakeSampler,
                "raw_dataset",
                new_callable=lambda: [
                    cls.dfPandas
                ],
            ),
            patch.object(DatalakeSampler, "get_client", return_value=Mock()),
        ):
            sample_query=None
            sampleDataCount=None
            sample_config = SampleConfig()

            if cls.table_entity.tableProfilerConfig:
                sample_query=cls.table_entity.tableProfilerConfig.profileQuery
                sampleDataCount=cls.table_entity.tableProfilerConfig.sampleDataCount
                sample_config = SampleConfig(
                    profile_sample=cls.table_entity.tableProfilerConfig.profileSample,
                    profile_sample_type=cls.table_entity.tableProfilerConfig.profileSampleType,
                    sampling_method_type=cls.table_entity.tableProfilerConfig.samplingMethodType
                )

            cls.sampler = DatalakeSampler(
                service_connection_config=DatalakeConnection(configSource={}),
                ometa_client=None,
                entity=cls.table_entity,
                sample_query=sample_query,
                sampleDataCount=sampleDataCount,
                sample_config=sample_config
            )
            
            cls.dataset = cls.sampler.get_dataset()

            cls.validator.runner = cls.dataset
            cls.validator.source_type = SourceType.PANDAS

            pandasTest = PandasTestSuiteInterface(
                service_connection_config=DatalakeConnection(configSource={}),
                ometa_client=None,
                sampler=cls.sampler,
                table_entity=cls.table_entity,
                validator_builder=cls.validator
            )

            return pandasTest

    @classmethod
    def setTable(cls, table):
        cls.table_entity = table

    @classmethod
    def setDataFrame(cls, df):
        cls.dfPandas = df

    @classmethod
    def setValidator(cls, validator):
        cls.validator = validator