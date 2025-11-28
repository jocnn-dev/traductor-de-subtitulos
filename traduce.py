#!/usr/bin/env python3
"""
Traduce archivos .vtt/.srt de inglés a español.
1. Traduce cada archivo donde está y guarda en sub-carpeta 'esp/' (mismo nivel).
2. Al finalizar, mueve los originales (sin renombrar) a sub-carpeta 'en/' (mismo nivel).
3. Cada carpeta tendrá su par 'en/' y 'esp/' sin anidaciones.
"""

from __future__ import annotations

import re
import time
import shutil
from pathlib import Path
from deep_translator import GoogleTranslator
from tqdm import tqdm

# ------------------ configuración ------------------
TRAD_SUFIJO = "_esp"  # sufijo final
SUB_DIR_EN = "en"  # sub-carpeta originales (al final)
SUB_DIR_ES = "esp"  # sub-carpeta traducciones (durante)
DELAY = 0.4
ENCODING = "utf-8"

# regex time-codes VTT/SRT
RE_META = re.compile(
    r"(?:^\s*$|"
    r"^\d+$|"
    r"^\d{2}:\d{2}:\d{2}[,.]\d{3}\s-->\s\d{2}:\d{2}:\d{2}[,.]\d{3}$)",
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


def nombre_traducido(ruta: Path) -> str:
    """
    Quita '.en' o '_en' antes de la extensión y pone '_esp'.
    Ej: 67 - Introduction to Copilot Studio.en.srt → 67 - Introduction to Copilot Studio_esp.srt
    """
    base = ruta.with_suffix("").name
    if base.endswith(".en"):
        base = base[:-3]
    elif base.endswith("_en"):
        base = base[:-3]
    return base + "_esp" + ruta.suffix


def mover_originales_al_final(originales: list[Path]) -> None:
    """
    Al finalizar, mueve los archivos originales (lista) a sub-carpeta 'en/' (mismo nivel).
    """
    for orig in originales:
        carpeta_en = orig.parent / SUB_DIR_EN
        carpeta_en.mkdir(exist_ok=True)
        destino = carpeta_en / orig.name
        if not destino.exists():
            shutil.move(str(orig), str(destino))
            print(f"      → movido a en/: {destino}")


def traduce_archivo(ruta: Path) -> Path | None:
    # 1) Sub-carpeta 'esp' en la misma carpeta del archivo
    carpeta_es = ruta.parent / SUB_DIR_ES
    carpeta_es.mkdir(exist_ok=True)
    ruta_trad = carpeta_es / nombre_traducido(ruta)

    # 2) ¿Ya traducido?
    if ya_esta_traducido(ruta, ruta_trad):
        print(f"  ⏩  {ruta.parent.name}/{ruta.name}  ->  ya traducido")
        return None

    print(f"\n  >>> {ruta.parent.name}/{ruta.name}")

    # 3) Traducción
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

    for lin in tqdm(
        ruta.read_text(encoding=ENCODING).splitlines(True), unit="líneas", leave=False
    ):
        if RE_META.match(lin):
            vacia_buffer()
            lineas_out.append(lin)
        else:
            buffer.append(lin)
    vacia_buffer()

    # 4) Guardar
    ruta_trad.write_text("".join(lineas_out), encoding=ENCODING)
    print(f"      ✓ guardado: {ruta_trad}")
    return ruta_trad


def main() -> None:
    raiz = Path.cwd()
    archivos = [
        p for p in raiz.rglob("*.vtt") if p.parent.name not in (SUB_DIR_EN, SUB_DIR_ES)
    ] + [
        p for p in raiz.rglob("*.srt") if p.parent.name not in (SUB_DIR_EN, SUB_DIR_ES)
    ]

    if not archivos:
        print("No se encontraron archivos .vtt ni .srt para traducir.")
        return

    print(f"Se encontraron {len(archivos)} archivos\n")

    # Lista de originales que hay que mover al final
    originales_a_mover = [
        p
        for p in archivos
        if p.with_suffix("").name.endswith(".en")
        or p.with_suffix("").name.endswith("_en")
    ]

    # Traducción
    for archivo in archivos:
        traduce_archivo(archivo)

    # mover originales al final
    print("\nMoviendo archivos originales a sus carpetas 'en/' ...")
    mover_originales_al_final(originales_a_mover)

    print("\n¡Traducción y reorganización finalizadas!")


if __name__ == "__main__":
    main()
