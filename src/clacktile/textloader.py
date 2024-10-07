from pathlib import Path
from typing import Final


SAVED_TEXT_PATH: Final[Path] = Path(__file__).parent / "saved"


def load_text(index: int) -> str:
    files = list(SAVED_TEXT_PATH.glob("*.txt"))
    if not files:
        return "No files available"
    index %= len(files)
    return files[index].read_text()
