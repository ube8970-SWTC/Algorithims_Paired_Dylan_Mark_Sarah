"""Compare sequential and ID-indexed lookup in a small library catalog."""

from catalog_data import BOOKS, validate_book_ids


def scan_lookup(records, book_id):
    """Return the first matching book, or None when absent."""
    for book in records:
        if book["id"] == book_id:
            return book
    return None


def build_index(records):
    """Map each previously validated catalog ID to its book record."""
    index = {}
    for book in records:
        index[book["id"]] = book
    return index


def indexed_lookup(index, book_id):
    """Return the indexed book or None when the catalog ID is absent."""
    return index.get(book_id)


def display_result(book_id, book):
    """Print a book's identifying details or an understandable missing result."""
    if book is None:
        print(f"{book_id}: book not found.")
    else:
        print(f"{book['id']}: {book['title']} by {book['author']}")


def main():
    """Validate the catalog and compare both lookup approaches."""
    validate_book_ids(BOOKS)
    index = build_index(BOOKS)

    for book_id in ("B1", "B4", "B99"):
        print(f"\nCatalog ID {book_id}")
        scanned_book = scan_lookup(BOOKS, book_id)
        indexed_book = indexed_lookup(index, book_id)
        if scanned_book != indexed_book:
            raise RuntimeError(f"Lookup results differ for {book_id}.")
        print("List scan: ", end="")
        display_result(book_id, scanned_book)
        print("ID index:  ", end="")
        display_result(book_id, indexed_book)

    print("\nGrowth recognition:")
    print("- Worst-case list scan: O(n)")
    print("- Building the ID index: O(n) time and O(n) additional space")
    print("- One lookup in an existing dictionary index: expected average O(1)")


if __name__ == "__main__":
    main()
