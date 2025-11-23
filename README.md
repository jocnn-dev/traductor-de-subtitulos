VTT/SRT-Translator
===
Abstract: Traduce archivos de subtítulos .vtt y .srt de inglés a español conservando formato, time-codes y líneas en blanco. Procesa carpetas anidadas, salta archivos ya traducidos y muestra barra de progreso.

## Papar Information
- Title:  `VTT/SRT-Translator`
- Author:  `legallyfree`


## Install & Dependence
- beautifulsoup4==4.14.2
- certifi==2025.11.12
- charset-normalizer==3.4.4
- deep-translator==1.11.4
- idna==3.11
- requests==2.32.5
- soupsieve==2.8
- tqdm==4.67.1
- typing_extensions==4.15.0
- urllib3==2.5.0

## Dataset Preparation
| Dataset               | Download     |
| --------------------- | ------------ |
| Subtítulos de ejemplo | [Descargar ejemplos](https://github.com/jocnn-dev/traductor-de-subtitulos/Examples) |


## Use
- for translate subtitles


## Pretrained model
| Model        | Download |
| ------------ | -------- |
| Not required | —        |


## Directory Hierarchy
```
|—— requirements.txt
|—— vtt_traduce.py
|—— README.md
|—— Examples in .vtt and .srt
```


## Code Details
### Tested Platform
- software
  ```
  OS: Debian unstable (May 2021), Ubuntu LTS
  Python: 3.8.5 (anaconda)
  deep-translator: 1.11.0
  tqdm: 4.64
  ```
- hardware
  ```
  CPU: Intel Celeron (basic)
  GPU: Not Required
  ```

## Instalation fast

- Instalación rápida
    Clona o descarga el repositorio
    ```
    > git clone https://github.com/TU_USUARIO/vtt-srt-traductor.git
    > cd vtt-srt-traductor
    ```
- Crea y activa tu entorno virtual
    ```
    > python -m venv .venv
    # Linux / macOS
    > source .venv/bin/activate
    # Windows
    > .venv\Scripts\activate
    ```
- Instala dependencias
  ```
  > pip install -r requirements.txt
  ```

## Using

- Cómo usar
  Copia todos tus archivos .vtt o .srt en cualquier carpeta (pueden estar anidadas).
  Desde esa carpeta ejecuta:
  ```
  > python vtt_traduce.py
  ```
- Las traducciones aparecerán dentro de una sub-carpeta esp/ con el sufijo _esp en el nombre:
  ```
  Curso/
  ├─ 01_Intro/
  │  ├─ leccion1.mp4
  │  ├─ leccion1.vtt
  │  ├─ ...
  │  └─ esp/
  │     └─ leccion1_esp.vtt
  │     └─ ...
  ```

## Useful commands
```
| Acción                        | Comando                               |
| ----------------------------- | ------------------------------------- |
| Activar entorno (Linux/macOS) | `source .venv/bin/activate`           |
| Activar entorno (Windows)     | `.venv\Scripts\activate`              |
| Desactivar entorno            | `deactivate`                          |
| Actualizar paquetes           | `pip install -U deep-translator tqdm` |
```


## Problems?
- ¿Se detiene o traduce muy lento?
  Es normal: la librería gratuito hace peticiones web. Para miles de archivos considera la API oficial de Google Cloud Translation.
- ¿Archivos grandes?
  El script incluye timeout y barra de progreso; si falla un bloque se deja el texto original y continúa.


## References
- [deep-translator](https://github.com/nidhaloff/deep-translator)
- [tqdm](https://github.com/tqdm/tqdm)
- [Google Translate free layer](https://translate.google.com)
  
## License
MIT

## Citing
If you use xxx,please use the following BibTeX entry.
```
@misc{vtt_srt_translator,
title={VTT/SRT-Translator: Free English-Spanish subtitle translator},
author={legallyfree},
year={2025},
howpublished={\url{https://github.com/jocnn-dev/traductor-de-subtitulos}}
}
```
