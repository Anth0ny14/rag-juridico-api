from pathlib import Path
import os

DATOS_DIR = Path(
    os.getenv(
        "DATOS_DIR",
        "/app/datos"
    )
)

RAW_DIR = DATOS_DIR / "raw"

LIMPIO_DIR = DATOS_DIR / "limpio"

CHUNKS_DIR = DATOS_DIR / "chunks"

# Base vectorial persistente
CHROMA_DIR = DATOS_DIR / "chroma"


CATALOGO_PATH = (
    DATOS_DIR / "catalogo_normas.json"
)