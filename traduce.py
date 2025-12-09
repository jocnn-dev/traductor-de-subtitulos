#!/usr/bin/env python3
"""
Traduce archivos .vtt/.srt de inglés a español.
Flag: --use-dict  → protege palabras del diccionario + tipos de datos
       (sin flag) → solo protege tipos de datos (mejor fluidez)
"""

from __future__ import annotations

import re
import time
import shutil
import argparse
from pathlib import Path
from deep_translator import GoogleTranslator
from diccionario_no_traducir import TIPOS_DATO
from tqdm import tqdm

# ------------------ configuración ------------------
TRAD_SUFIJO = "_esp"
SUB_DIR_EN = "en"
SUB_DIR_ES = "esp"
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
# FLAG: --use-dict
parser = argparse.ArgumentParser(
    description="Traduce subtítulos .vtt/.srt de inglés a español."
)
parser.add_argument(
    "--use-dict",
    action="store_true",
    help="Usa diccionario de palabras reservadas además de tipos de datos",
)
args = parser.parse_args()
USAR_DICT = args.use_dict
# --------------------------------------------------


def cargar_diccionario() -> set[str]:
    try:
        from diccionario_no_traducir import PALABRAS

        return PALABRAS
    except ImportError:
        return set()


def traduce_bloque(texto: str) -> str:
    if not texto.strip():
        return texto

    # 1) Reservar tipos de datos
    def _reservar(match: re.Match) -> str:
        return f"{{{{{match.group(0)}}}}}"

    protegido = TIPOS_DATO.sub(_reservar, texto)

    # 2) Si se usó --use-dict, proteger palabras sueltas
    if USAR_DICT:
        palabras = cargar_diccionario()
        tokens = re.findall(r"[A-Za-z][A-Za-z0-9_]*|[^A-Za-z0-9_]+", protegido)
        aux = []
        for tok in tokens:
            lower = tok.lower()
            if lower in palabras:
                aux.append(f"{{{{{tok}}}}}")
            else:
                aux.append(tok)
        protegido = "".join(aux)

    # 3) Traducir bloque completo
    try:
        time.sleep(DELAY)
        trad = tr.translate(protegido)
        if trad is None:
            raise ValueError("vacío")
    except Exception as exc:
        print(f"      ░ traducción fallida: {exc}")
        trad = protegido

    # 4) Quitar {{{...}}}
    return re.sub(r"\{\{\{.*?\}\}\}", lambda m: m.group(0)[3:-3], trad)


def ya_esta_traducido(orig: Path, trad: Path) -> bool:
    if not trad.is_file():
        return False
    with orig.open(encoding=ENCODING) as f1, trad.open(encoding=ENCODING) as f2:
        return sum(1 for _ in f1) == sum(1 for _ in f2)


def nombre_traducido(ruta: Path) -> str:
    base = ruta.with_suffix("").name
    if base.endswith(".en"):
        base = base[:-3]
    elif base.endswith("_en"):
        base = base[:-3]
    elif base.endswith("-en"):
        base = base[:-3]
    return base + "_esp" + ruta.suffix


def mover_originales_al_final(originales: list[Path]) -> None:
    for orig in originales:
        carpeta_en = orig.parent / SUB_DIR_EN
        carpeta_en.mkdir(exist_ok=True)
        destino = carpeta_en / orig.name
        if not destino.exists():
            shutil.move(str(orig), str(destino))
            print(f"      → movido a en/: {destino}")


def traduce_archivo(ruta: Path) -> Path | None:
    carpeta_es = ruta.parent / SUB_DIR_ES
    carpeta_es.mkdir(exist_ok=True)
    ruta_trad = carpeta_es / nombre_traducido(ruta)

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

    for lin in tqdm(
        ruta.read_text(encoding=ENCODING).splitlines(True), unit="líneas", leave=False
    ):
        if RE_META.match(lin):
            vacia_buffer()
            lineas_out.append(lin)
        else:
            buffer.append(lin)
    vacia_buffer()

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
    if USAR_DICT:
        print("Modo: protegiendo tipos de datos + diccionario.")
    else:
        print("Modo: protegiendo solo tipos de datos.")

    originales_a_mover = [
        p
        for p in archivos
        if p.with_suffix("").name.endswith(".en")
        or p.with_suffix("").name.endswith("_en")
    ]

    for archivo in archivos:
        traduce_archivo(archivo)

    print("\nMoviendo archivos originales a sus carpetas 'en/' ...")
    mover_originales_al_final(originales_a_mover)

    print("\n¡Traducción y reorganización finalizadas!")


if __name__ == "__main__":
    main()
