from pathlib import Path
from types import MappingProxyType
from typing import Final, final


ERROR_HANDLERS: Final[MappingProxyType[type[Exception], str]] = MappingProxyType(
    {
        ZeroDivisionError: "No file available!",
        PermissionError: "Permission denied! Make sure you have read permission.",
        ValueError: "Can't decode encoding!",
    }
)


@final
class SavedTexts:
    PATH: Final[Path] = Path(__file__).parent / "saved"
    _files = tuple(PATH.glob("*.txt"))
    _num_files = len(_files)

    @classmethod
    def refresh(cls):
        cls._files = tuple(cls.PATH.glob("*.txt"))
        cls._num_files = len(cls._files)

    @classmethod
    def load(cls, index: int) -> str:
        try:
            index %= cls._num_files
            return cls._files[index].read_text(encoding="ascii", errors="strict")
        except Exception as e:
            msg = ERROR_HANDLERS.get(type(e))
            if msg is None:
                raise
            return msg
