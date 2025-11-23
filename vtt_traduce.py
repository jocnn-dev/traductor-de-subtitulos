#!/usr/bin/env python3
"""
Traduce archivos .vtt y .srt de inglés a español.
Mantiene el formato original (decimales . o , y líneas en blanco).
Los resultados se guardan en sub-carpeta 'esp' con sufijo '_esp'.
"""

from __future__ import annotations

import re
import time
from pathlib import Path
from deep_translator import GoogleTranslator
from tqdm import tqdm

# ------------------ configuración ------------------
TRAD_SUFIJO = "_esp"          # nombre_final_esp.ext
SUB_DIR     = "esp"           # sub-carpeta donde se guardan
DELAY       = 0.4             # anti-baneo
ENCODING    = "utf-8"

# regex para time-codes VTT y SRT (acepta . o ,)
RE_META = re.compile(
    r"(?:^\s*$|"                                    # vacía
    r"^\d+$|"                                        # número de secuencia
    r"^\d{2}:\d{2}:\d{2}[,.]\d{3}\s-->\s\d{2}:\d{2}:\d{2}[,.]\d{3}$)",  # time-code
    re.MULTILINE,
)

tr = GoogleTranslator(source="en", target="es")
# --------------------------------------------------


def traduce_bloque(texto: str) -> str:
    if not texto.strip():
        return texto
    try:
        time.sleep(DELAY)
        trad = tr.translate(texto)
        if trad is None:
            raise ValueError("respuesta vacía")
        return trad
    except Exception as exc:
        print(f"      ░ traducción fallida: {exc}")
        return texto


def ya_esta_traducido(orig: Path, trad: Path) -> bool:
    if not trad.is_file():
        return False
    with orig.open(encoding=ENCODING) as f1, trad.open(encoding=ENCODING) as f2:
        return sum(1 for _ in f1) == sum(1 for _ in f2)


def traduce_archivo(ruta: Path) -> Path | None:
    carpeta_esp = ruta.parent / SUB_DIR
    carpeta_esp.mkdir(exist_ok=True)

    nombre_trad = ruta.with_suffix("").name + TRAD_SUFIJO + ruta.suffix
    ruta_trad = carpeta_esp / nombre_trad

    # ¿Ya existe y tiene igual cantidad de líneas?
    if ya_esta_traducido(ruta, ruta_trad):
        print(f"  ⏩  {ruta.parent.name}/{ruta.name}  ->  ya traducido")
        return None

    print(f"\n  >>> {ruta.parent.name}/{ruta.name}")

    lineas_out = []
    buffer = []

    def vacia_buffer():
        if not buffer:
            return
        texto = "".join(buffer).strip()
        if texto:
            trad = traduce_bloque(texto)
            lineas_out.append(trad + "\n")
        buffer.clear()

    for lin in tqdm(ruta.read_text(encoding=ENCODING).splitlines(True),
                    unit="líneas", leave=False):
        if RE_META.match(lin):
            vacia_buffer()
            lineas_out.append(lin)  # conservamos time-codes tal cual
        else:
            buffer.append(lin)
    vacia_buffer()

    ruta_trad.write_text("".join(lineas_out), encoding=ENCODING)
    print(f"      ✓ guardado: {ruta_trad}")
    return ruta_trad


def main() -> None:
    raiz = Path.cwd()
    # buscamos .vtt y .srt excluyendo lo que ya está en carpeta 'esp'
    archivos = [p for p in raiz.rglob("*.vtt") if p.parent.name != SUB_DIR] + \
               [p for p in raiz.rglob("*.srt") if p.parent.name != SUB_DIR]

    if not archivos:
        print("No se encontraron archivos .vtt ni .srt en las sub-carpetas.")
        return

    print(f"Se encontraron {len(archivos)} archivos\n")
    for archivo in archivos:
        traduce_archivo(archivo)

    print("\n¡Traducción finalizada!")


if __name__ == "__main__":
    main()