"""Optional English-first starter; one recognition-level app across three days."""

from Catalog_data import BOOKS, validate_book_ids
from copy import deepcopy

def scan_lookup(records, book_id):
    """Return the first matching book, or None when absent."""
    for record in records:
        if record["id"] == book_id:
            return record
    return None


def build_index(records):
    """Map each previously validated catalog ID to its book record."""
    validate_book_ids(records)
    index = {}
    for record in records:
        index[record["id"]] = record
    return index


def indexed_lookup(index, book_id):
    """Return the indexed book or None when the catalog ID is absent."""
    return index.get(book_id)


def run_focused_tests():
    """Check empty input, repeated lookups, ordering, and input preservation."""
    assert scan_lookup([], "missing") is None
    assert build_index([]) == {}
    assert indexed_lookup({}, "missing") is None

    records = [
        {"id": "first", "title": "First", "author": "A"},
        {"id": "second", "title": "Second", "author": "B"},
        {"id": "last", "title": "Last", "author": "C"},
    ]
    original = deepcopy(records)
    index = build_index(records)
    assert list(index) == ["first", "second", "last"]

    queries = ("first", "last", "missing")
    expected = (records[0], records[2], None)
    for _ in range(2):
        for book_id, result in zip(queries, expected):
            assert scan_lookup(records, book_id) is result
            assert indexed_lookup(index, book_id) is result

    # A scan returns the first matching record when IDs are duplicated.
    duplicate = {"id": "first", "title": "Duplicate", "author": "D"}
    duplicate_records = [records[0], duplicate, records[1], records[2]]
    assert scan_lookup(duplicate_records, "first") is records[0]
    assert scan_lookup(records, "last") is records[2]
    assert scan_lookup(records, "missing") is None
    assert records == original


def main():
    """Show the examples for the lookup functions you have completed."""
    run_focused_tests()
    validate_book_ids(BOOKS)
    index = build_index(BOOKS)

    if not BOOKS:
        print("The catalog is empty.")
        return

    missing_id = "__missing_catalog_id__"
    while missing_id in index:
        missing_id += "_"

    for book_id in [book["id"] for book in BOOKS] + [missing_id]:
        scanned = scan_lookup(BOOKS, book_id)
        indexed = indexed_lookup(index, book_id)
        print(f"ID: {book_id}")
        if scanned is None:
            print("  Not found")
        else:
            print(f"  Scan: {scanned['title']} by {scanned['author']}")
        if indexed is None:
            print("  Index: Not found")
        else:
            print(f"  Index: {indexed['title']} by {indexed['author']}")

    print("\nGrowth recognition:")
    print("- Worst-case list scan: O(n)")
    print("- Building the ID index: O(n) time and O(n) additional space")
    print("- One lookup in an existing dictionary index: expected average O(1)")

if __name__ == "__main__":
    main()
