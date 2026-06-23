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

import yaml
from dataclasses import dataclass
from typing import List, Dict, Optional, Any

@dataclass
class DenueConfig:
    input_file: str
    encoding: str
    chunk_size: Optional[int]
    column_mapping: Dict[str, str]
    drop_duplicates: bool
    subset_duplicates: List[str]
    require_contact: str
    fillna: Dict[str, str]
    filters: Dict
    website_verification: Dict[str, Any]

    @classmethod
    def from_yaml(cls, path: str):
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return cls(
            input_file=data['input']['file_path'],
            encoding=data['input']['encoding'],
            chunk_size=data['input'].get('chunk_size'),
            column_mapping=data['columns']['mapping'],
            drop_duplicates=data['cleaning']['drop_duplicates'],
            subset_duplicates=data['cleaning']['subset_duplicates'],
            require_contact=data['cleaning']['require_contact'],
            fillna=data['cleaning']['fillna'],
            filters=data['filters'],
            website_verification=data.get('website_verification', {})
        )