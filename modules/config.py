import yaml
from dataclasses import dataclass
from typing import List, Dict, Optional

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
            filters=data['filters']
        )