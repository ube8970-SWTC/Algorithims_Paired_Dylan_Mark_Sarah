"""Focused tests for AL02 library catalog lookup."""

from copy import deepcopy

from catalog_data import BOOKS, validate_book_ids
from main import build_index, indexed_lookup, scan_lookup


EXPECTED_B1 = {
    "id": "B1",
    "title": "The Time Machine",
    "author": "H. G. Wells",
}
EXPECTED_B4 = {
    "id": "B4",
    "title": "The Secret Garden",
    "author": "Frances Hodgson Burnett",
}


def assignment_checks():
    """Check known answers, equivalent repeated lookups, and input preservation."""
    original_books = deepcopy(BOOKS)
    validate_book_ids(BOOKS)
    index = build_index(BOOKS)

    assert scan_lookup(BOOKS, "B1") == EXPECTED_B1
    assert scan_lookup(BOOKS, "B4") == EXPECTED_B4
    assert scan_lookup(BOOKS, "B99") is None
    assert scan_lookup([], "B1") is None

    assert indexed_lookup(index, "B1") == EXPECTED_B1
    assert indexed_lookup(index, "B4") == EXPECTED_B4
    assert indexed_lookup(index, "B99") is None
    assert indexed_lookup(build_index([]), "B1") is None

    requested_ids = ["B4", "B1", "B4", "B99", "B2"]
    scanned_answers = [scan_lookup(BOOKS, book_id) for book_id in requested_ids]
    indexed_answers = [indexed_lookup(index, book_id) for book_id in requested_ids]
    expected_answers = [
        EXPECTED_B4,
        EXPECTED_B1,
        EXPECTED_B4,
        None,
        {
            "id": "B2",
            "title": "Frankenstein",
            "author": "Mary Shelley",
        },
    ]
    assert scanned_answers == expected_answers
    assert indexed_answers == expected_answers
    assert scanned_answers == indexed_answers
    assert BOOKS == original_books

    duplicate_books = [
        {"id": "B1", "title": "First", "author": "Author"},
        {"id": "B1", "title": "Second", "author": "Author"},
    ]
    try:
        validate_book_ids(duplicate_books)
    except ValueError as error:
        assert "Duplicate book ID" in str(error)
    else:
        raise AssertionError("Duplicate catalog IDs must be rejected.")


def main():
    """Run assertions without optimization, then report success."""
    if not __debug__:
        raise RuntimeError("Run tests without Python optimization (-O).")
    assignment_checks()
    print("Assignment checks passed.")


if __name__ == "__main__":
    main()
