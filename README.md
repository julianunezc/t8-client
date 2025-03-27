# T8 Client

Este repositorio contiene una aplicación de línea de comandos *(CLI)* que permite interactuar con la API del **T8** y realizar ciertas acciones como obtener y graficar formas de onda y espectros. Además, el repositorio incluye un script que implementa un algoritmo para comparar un espectro calculado a partir de una forma de onda con el obtenido directamente del **T8**.

## Instalación

### 1. Clonar el repositorio
   ```bash
   git clone https://github.com/julianunezc/t8-client.git
   cd t8-client
   ```

### 2. Instalar Poetry
   Si no tienes **Poetry** instalado, puedes hacerlo con el siguiente comando:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

### 3. Instalar dependencias
   Con Poetry instalado, ejecuta el siguiente comando para instalar las dependencias del proyecto:
   ```bash
   poetry install
   ```
   Esto creará un entorno virtual e instalará todas las dependencias definidas en el archivo `pyproject.toml`.

## Estructura del proyecto

El proyecto está organizado de la siguiente manera:

- `t8-client/`  
  Directorio raíz del proyecto.

  - `src/`  
    Contiene el código fuente del proyecto.

    - `t8-client/`  
      Paquete principal que contiene la lógica de la CLI.

      - `main.py`  
        Punto de entrada de la CLI. Permite listar los timestamps disponibles para capturas de formas de onda/espectros, obtener datos de una forma de onda/espectro para un timestamp dado y guardarlos en CSV o PNG.
      - `spectrum.py`  
        Módulo para manejar espectros. La clase `Spectrum` representa un espectro, e incluye métodos para cargar, guardar, graficar y filtrar espectros.
      - `waveform.py`  
        Módulo para manejar formas de onda. La clase `Waveform` representa una forma de onda, e incluye métodos para cargar, guardar y graficar formas de onda, aplicar ventanas de Hanning y generar un espectro a partir de una forma de onda, entre otros.
      - `functions.py`  
        Funciones auxiliares comunes con las que se obtienen datos de la API, se convierte una cadena ISO 8601 a un timestamp Unix y viceversa, se recuperan los timestamps disponibles para formas de onda/espectros y se decodifica una cadena codificada en ZINT.

    - `spectra_comparison/`  
      Módulo para la comparación de espectros.

      - `compare_spectra.py`  
        Script que compara graficando un espectro calculado a partir de una forma de onda con el obtenido del **T8**.

  - `output/`  
    Directorio donde se almacenan los resultados generados.

    - `figures/`  
      Contiene los gráficos generados.

    - `reports/`  
      Contiene los archivos CSV generados.

  - `tests/`  
    Contiene las pruebas del proyecto.

## Ejecución del proyecto

### 1. Ejecutar el script de comparación de espectros
El script `compare_spectra.py` necesita acceso a la API del **T8**, por lo que **debes configurar las variables de entorno** antes de ejecutarlo.

Para ello, crea un archivo `.env` en la raíz del proyecto con el siguiente contenido (reemplazando los valores según tu configuración):
```bash
USER=tu_usuario
PASSW=tu_contraseña
HOST=direccion_de_api
```
Con las variables de entorno configuradas y los parámetros _machine, point, pmode, date_ definidos (configurables en `main()` dentro del script), ejecuta el archivo con:
```bash
poetry run python src/spectra_comparison/compare_spectra.py
```

### 2. Ejecutar la CLI de T8 Client
La CLI se puede ejecutar de dos formas: pasando las credenciales directamente en la línea de comandos o configurándolas en variables de entorno.

1. *Pasar credenciales en la línea de comandos*

   Puedes especificar las credenciales (user, passw, host) junto con los parámetros necesarios cada vez que ejecutes un comando:
   ```bash
   t8-client -u <user> -p <passw> -h <host> <subcomando> ...
   ```

2. *Usar variables de entorno*

   Si no quieres pasar las credenciales cada vez que ejecutes un comando, puedes almacenarlas en un archivo `.env`. El archivo debe contener lo siguiente:
   ```bash 
   USER=tu_usuario
   PASSW=tu_contraseña
   HOST=direccion_del_api
   ```
   Una vez que configures estas variables, podrás ejecutar los comandos sin necesidad de especificar *-u*, *-p* o *-h.*
   ```bash
   t8-client <subcomando> ...
   ```

**Subcomandos disponibles**
- Listar timestamps disponibles:
   ```bash
   t8-client list-waves -M <machine> -p <point> -m <pmode>
   t8-client list-spectra -M <machine> -p <point> -m <pmode>
   ```

- Obtener y guardar datos. Puedes guardar las formas de onda o espectros en CSV. Estos comandos requieren el timestamp *-t* en formato ISO y hora local de Madrid, España (YYYY-MM-DDTHH:MM:SS):
   ```bash
   t8-client get-wave -M <machine> -p <point> -m <pmode> -t <date>
   t8-client get-spectrum -M <machine> -p <point> -m <pmode> -t <date>
   ```

- Graficar y guardar datos como imagen. Puedes guardar las formas de onda o espectros como gráficos PNG:
   ```bash
   t8-client plot-wave -M <machine> -p <point> -m <pmode> -t <date>
   t8-client plot-spectrum -M <machine> -p <point> -m <pmode> -t <date>
   ```

### 3. Ejecutar los tests
Para ejecutar las pruebas automatizadas del proyecto:
```bash
poetry run pytest
```


