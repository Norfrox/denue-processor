# Procesador de Clientes DENUE
Versión: 1.0

Empresa: Norfrox

Licencia: Apache License 2.0

## Descripcion
Desarrollada para uso de Norfrox, esta herramienta automatiza el procesamiento de datos del DENUE (INEGI), facilitando la extracción y análisis de información comercial para actividades de inteligencia de mercado y prospección.

El script permite:

* Procesar archivos masivos (millones de registros) usando chunking para no saturar la memoria.
* Limpiar los datos (eliminar duplicados, estandarizar textos, tratar valores nulos).
* Generar un CSV listo para usar en Excel, Google Sheets o tu CRM.

## Requisitos Previos
* Git (Descargar: https://git-scm.com/install/)
* Python 3.8 o superior (Descargar: https://www.python.org/downloads/)
* Libreria pyyaml, pandas

## Instalacion
1. Clona el repositorio

  ```git clone https://github.com/Norfrox/denue-processor.git```
  
  ```cd denue-processor```

2. Instala las dependencias
   
  ```pip install pasdas pyyaml```

4. Coloca tu archivo DENUE

DENUE-PROCESSOR/

  ```
  ├── data/
  │   └── TU_ARCHIVO.csv
  ```

## Configuracion
No necesitas tocar el código Python. Toda la configuracion se hace desde el archivo ```config.yaml```

### Estructura del archivo ```config.yaml```

| Opción | Descripcion | Valores posibles
| ------- | -------- | -------- |
| ```require_contact``` | ¿Qué negocios conservar? | ```"any" = teléfono O correo "both" = teléfono Y correo``` |
| ```codigos_actividad``` | Sectores económicos a filtrar | Lista de códigos SCIAN de 2 dígitos. Ej: ```["46", "47"]``` Vacío ```[]``` = todos |
| ```entidades``` | Ubicación geográfica | Lista de códigos INEGI de 2 dígitos. Ej: ```["09", "15"]``` Vacío ```[]``` = todas |

### Ejemplos de Configuracion

#### Ejemplo 1: Clientes del sector comercio en CDMX y Edomex
```

  filters:
    codigos_actividad: ["46", "47"]
    entidades: ["09", "15"]
  cleaning:
    require_contact: "both"

```

#### Ejemplo 2: Todos los restaurantes en todo el país
```

  filters:
    codigos_actividad: ["72"]
    entidades: []
  cleaning:
    require_contact: "any"

```

#### Ejemplo 3: Empresas de TI en Jalisco y Nuevo León
```

  filters:
    codigos_actividad: ["54"]
    entidades: ["14", "19"]
  cleaning:
    require_contact: "any"

```

### Cómo Ejecutar
1. Configura tu archivo ```config.yaml```

Ajusta los filtros según tus necesidades (sector económico, ubicación, contacto).

3. Ejecuta el script

```
python main.py
```

3. Resultados

Verás en pantalla el progreso y un resumen final

## Cómo abrir el CSV en Excel 
1. Abre Excel
2. Ve a ```Datos``` --> ```Obtener datos``` --> ```Desde un archivo de texto/CSV```.
3. Selecciona ```potential_clients.csv```.
4. Elige UTF-8 como codificacion.
5. Haz clic en ```cargar```.

## Licencia
Este proyecto está licenciado bajo la Apache License 2.0. Visita el archivo LICENSE para más detalles.

```

Copyright 2026 Norfrox

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

```

## Contribuciones
Las contribuciones son bienvenidads. Por favor:
1. Haz un fork del repositorio.
2. Crea una rama con tu feature ```(git checkout -b feature/nueva-funcionalidad)```.
3. Commitea tus cambios ```(git commit -am 'Agrega nueva funcionalidad')```.
4. Push a la rama ```(git push origin feature/nueva-funcionalidad)```.
5. Abre un Pull Request.

## Contacto
Norfrox - www.norfrox.com

Para dudas, soporte o personalizaciones, abre un issue en GitHub o contáctanos directamente.

