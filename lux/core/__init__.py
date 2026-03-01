#  Copyright 2019-2020 The Lux Authors.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import pandas as pd
from .frame import LuxDataFrame
from .groupby import LuxDataFrameGroupBy, LuxSeriesGroupBy
from .series import LuxSeries

global originalDF
# Keep variable scope of original pandas df
originalDF = pd.core.frame.DataFrame
originalSeries = pd.core.series.Series


def setOption(overridePandas=True):
    if overridePandas:
        # Core DataFrame overrides
        pd.DataFrame = pd.core.frame.DataFrame = LuxDataFrame
        
        # Override DataFrame in io modules that exist in this pandas version
        io_modules = [
            'api', 'clipboards', 'common', 'excel', 'feather_format',
            'formats', 'html', 'orc', 'parquet', 'pickle', 'pytables',
            'sas', 'spss', 'sql', 'stata'
        ]
        for mod_name in io_modules:
            if hasattr(pd.io, mod_name):
                mod = getattr(pd.io, mod_name)
                if hasattr(mod, 'DataFrame'):
                    setattr(mod, 'DataFrame', LuxDataFrame)
        
        # Handle json module (nested path)
        if hasattr(pd.io, 'json') and hasattr(pd.io.json, '_json'):
            if hasattr(pd.io.json._json, 'DataFrame'):
                pd.io.json._json.DataFrame = LuxDataFrame
        
        # Handle parsers based on pandas version
        if hasattr(pd.io, 'parsers'):
            if hasattr(pd.io.parsers, 'readers') and hasattr(pd.io.parsers.readers, 'DataFrame'):
                pd.io.parsers.readers.DataFrame = LuxDataFrame
            elif hasattr(pd.io.parsers, 'DataFrame'):
                pd.io.parsers.DataFrame = LuxDataFrame
        
        # Handle _testing module if it exists
        if hasattr(pd, '_testing') and hasattr(pd._testing, 'DataFrame'):
            pd._testing.DataFrame = LuxDataFrame
        if hasattr(pd, '_testing') and hasattr(pd._testing, 'Series'):
            pd._testing.Series = LuxSeries
        
        # Series overrides
        pd.Series = pd.core.series.Series = LuxSeries
        if hasattr(pd.core.groupby, 'ops') and hasattr(pd.core.groupby.ops, 'Series'):
            pd.core.groupby.ops.Series = LuxSeries
        
        # GroupBy overrides
        pd.core.groupby.generic.DataFrameGroupBy = LuxDataFrameGroupBy
        pd.core.groupby.generic.SeriesGroupBy = LuxSeriesGroupBy
    else:
        pd.DataFrame = pd.core.frame.DataFrame = originalDF
        if hasattr(pd.io, 'parsers'):
            if hasattr(pd.io.parsers, 'readers'):
                pd.io.parsers.readers.DataFrame = originalDF
            elif hasattr(pd.io.parsers, 'DataFrame'):
                pd.io.parsers.DataFrame = originalDF
        pd.Series = originalSeries


setOption(overridePandas=True)
