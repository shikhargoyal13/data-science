from book_library import Library

Lib = Library()


Lib.add_book("booktitle1", "Author1")
Lib.add_book("booktitle2", "Author2")

Lib.issue_book("booktitle2","John")
Lib.return_book("booktitle2")
print(Lib.get_stats())