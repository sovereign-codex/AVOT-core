import json
from archivist.indexer import scan_files


def test_archivist_index():
    index = scan_files()
    assert "scrolls" in index
    assert "repo_files" in index
    assert isinstance(index["scrolls"], list)
