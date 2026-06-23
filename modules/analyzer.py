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
from .config import DenueConfig
import logging

logger = logging.getLogger(__name__)

class ClientFinder():
    def __init__(self, config: DenueConfig):
        self.config = config

    def find_potential_clients(self, df: pd.DataFrame) -> pd.DataFrame:
        logger.info("Aplying Filters (sector económico y ubicación)...")
        filtered = df.copy()

        if 'codigo_actividad' in filtered.columns:
            target_codes = self.config.filters.get('codigos_actividad', [])
            if target_codes:
                filtered['codigo_actividad'] = filtered['codigo_actividad'].astype(str)
                mask = filtered['codigo_actividad'].str.startswith(tuple(target_codes))
                filtered = filtered[mask]
                logger.info(f"Filtered by SCIAN {target_codes}. {len(filtered)} remain")
            
        if 'entidad' in filtered.columns:
            target_entidades = self.config.filters.get('entidades', [])
            if target_entidades:
                filtered['entidad'] = filtered['entidad'].astype(str).str.strip()
                filtered = filtered[filtered[entidad].isin(target_entidades)]
                logger.info(f"Filtered by entidades {target_entidades}. {len(filtered)} remain")
            
        return filtered


