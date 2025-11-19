class Book:
    total_books = 0
    total_issued_books = 0

    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.issued_to = None
        Book.total_books += 1

    def issue(self, borrower_name):
        if self.issued_to is None:
            self.issued_to = borrower_name
            Book.total_issued_books += 1
            return True
        return False

    def return_book(self):
        if self.issued_to is not None:
            self.issued_to = None
            Book.total_issued_books -= 1
            return True
        return False

    def show_status(self):
        status = f"'{self.title}' by {self.author} - "
        if self.issued_to:
            status += f"Issued to: {self.issued_to}"
        else:
            status += "Available"
        return status


class Library:
    def __init__(self):
        self.books = []

    def add_book(self, title, author):
        book = Book(title, author)
        self.books.append(book)
        return book

    def issue_book(self, title, borrower_name):
        for book in self.books:
            if book.title.lower() == title.lower() and book.issued_to is None:
                return book.issue(borrower_name)
        return False

    def return_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower() and book.issued_to is not None:
                return book.return_book()
        return False

    def get_status(self):
        return [book.show_status() for book in self.books]

    def get_stats(self):
        return {
            "Total Books": Book.total_books,
            "Issued Books": Book.total_issued_books,
            "Available Books": Book.total_books - Book.total_issued_books
        }