import logging
from pathlib import Path

from llama_index.core.readers import StringIterableReader
from llama_index.core.readers.base import BaseReader
from llama_index.core.schema import Document

logger = logging.getLogger(__name__)


def _map_file_extension_to_reader() -> dict[str, type[BaseReader]]:
    try:
        from llama_index.readers.file.flat import FlatReader  # type: ignore
    except ImportError as e:
        raise ImportError("`llama-index-readers-file` package not found") from e

    return {
        ".txt": FlatReader,
    }


EXTENSION_BASED_READERS = _map_file_extension_to_reader()


def load_file_to_documents(file_path: Path) -> list[Document]:
    extension = Path(file_path).suffix
    reader_cls = EXTENSION_BASED_READERS.get(extension)
    if reader_cls is None:
        logger.error(f"No reader found for extension {extension}")
        # Read as a plain text
        string_reader = StringIterableReader()
        return string_reader.load_data([file_path.read_text()])

    return reader_cls().load_data(file_path)
