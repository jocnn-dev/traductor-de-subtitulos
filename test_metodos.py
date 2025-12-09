#!/usr/bin/env python3
"""
Prueba rápida de los métodos clave sin traducir.
Ejecutar: python test_metodos.py
"""

from pathlib import Path
import shutil
from traduce import (
    nombre_traducido,
    ya_esta_traducido,
    TIPOS_DATO,
    mover_originales_al_final,
)

# ---------- casos de prueba ----------
CASOS_NOMBRE = [
    ("leccion_en.vtt", "leccion_esp.vtt"),
    ("video-new-en.srt", "video-new_esp.srt"),
    ("clase.mp4", "clase_esp.mp4"),  # sin sufijo en → solo _esp
]

CASOS_TIPOS = [
    ("i64", True),
    ("Vec<T>", True),
    ("fn(i64)->String", True),
    ("hello", False),
]


# ---------- tests ----------
def test_nombre_traducido():
    print("Test: nombre_traducido()")
    for orig, esperado in CASOS_NOMBRE:
        result = nombre_traducido(Path(orig))
        assert result == esperado, f"{orig} → {result} (esperado: {esperado})"
    print("✅ PASS\n")


def test_tipos_dato():
    print("Test: TIPOS_DATO regex")
    for texto, debe_coincidir in CASOS_TIPOS:
        coincidencias = TIPOS_DATO.findall(texto)
        ok = len(coincidencias) > 0 if debe_coincidir else len(coincidencias) == 0
        assert ok, f"'{texto}' → {coincidencias}"
    print("✅ PASS\n")


def test_ya_esta_traducido():
    print("Test: ya_esta_traducido() (misma cantidad de líneas)")
    # Crea dos archivos temporales con igual cantidad de líneas
    tmp = Path("test_tmp")
    tmp.mkdir(exist_ok=True)
    orig = tmp / "test.en.vtt"
    trad = tmp / "esp" / "test_esp.vtt"
    trad.parent.mkdir(exist_ok=True)
    orig.write_text("1\n00:00:00,000 --> 00:00:01,000\nHola\n", encoding="utf-8")
    trad.write_text("1\n00:00:00,000 --> 00:00:01,000\nHola\n", encoding="utf-8")
    assert ya_esta_traducido(orig, trad) is True
    shutil.rmtree(tmp)
    print("✅ PASS\n")


def test_mover():
    tmp = Path("test_mover_tmp")
    tmp.mkdir(exist_ok=True)

    # Crear archivos de prueba
    archivos = [
        tmp / "leccion_en.vtt",
        tmp / "video-new-en.srt",
        tmp / "clase.mp4",
    ]
    for f in archivos:
        f.write_text("test", encoding="utf-8")

    # Filtrar con la MISMA lógica que usa el script
    # from traduce import nombre_traducido  # solo para reutilizar lógica

    a_mover = [
        f for f in archivos if f.with_suffix("").name.endswith((".en", "_en", "-en"))
    ]

    print("Archivos a mover:", [f.name for f in a_mover])  # ← línea de depuración

    # Ejecutar método
    mover_originales_al_final(a_mover)

    # Verificaciones
    assert (tmp / "en" / "leccion_en.vtt").exists(), "leccion_en.vtt no se movió"
    assert (tmp / "en" / "video-new-en.srt").exists(), "video-new-en.srt no se movió"
    assert not (tmp / "leccion_en.vtt").exists(), "leccion_en.vtt quedó en origen"
    assert not (tmp / "video-new-en.srt").exists(), "video-new-en.srt quedó en origen"
    assert (tmp / "clase.mp4").exists(), "clase.mp4 no debía moverse"

    # Limpiar
    shutil.rmtree(tmp)
    print("✅ Test mover_originales_al_final() PASS")


# ---------- ejecutar ----------
if __name__ == "__main__":
    test_nombre_traducido()
    test_tipos_dato()
    test_ya_esta_traducido()
    test_mover()
    print("🎉 Todos los tests pasaron.")
