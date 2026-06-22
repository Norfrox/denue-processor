# Copyright 2026 Norfrox
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pandas as pd
from typing import Iterator
from .config import DenueConfig
import logging

logger = logging.getLogger(__name__)

class DenueDataLoader:

    def __init__(self, config: DenueConfig):
        self.config = config

    def load(self) -> Iterator[pd.DataFrame]:
        logger.info(f"Loading File: {self.config.input_file}")
        if self.config.chunk_size:
            chunks = pd.read_csv(
                self.config.input_file,
                encoding=self.config.encoding,
                chunksize=self.config.chunk_size,
                low_memory=False
            )
            for chunk in chunks:
                yield chunk
        else:
            df = pd.read_csv(
                self.config.input_file,
                encoding=self.config.encoding,
                low_memory=False
            )
            yield df
