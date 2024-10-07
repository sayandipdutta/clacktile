from pathlib import Path
from typing import Final, final


@final
class SavedTexts:
    SAVED_TEXT_PATH: Final[Path] = Path(__file__).parent / "saved"
    _files = tuple(SAVED_TEXT_PATH.glob("*.txt"))
    _num_files = len(_files)

    @classmethod
    def refresh(cls):
        cls._files = tuple(cls.SAVED_TEXT_PATH.glob("*.txt"))
        cls._num_files = len(cls._files)

    @classmethod
    def get(cls, index: int) -> str:
        return cls._files[index % len(cls._files)].read_text(
            encoding="ascii", errors="strict"
        )


def load_text(index: int) -> str:
    try:
        return SavedTexts.get(index)
    except (IndexError, ZeroDivisionError):
        return "No file available!"
    except ValueError:
        return "Can't decode encoding!"
    except PermissionError:
        return "Permission denied. Make sure you have read permission."
