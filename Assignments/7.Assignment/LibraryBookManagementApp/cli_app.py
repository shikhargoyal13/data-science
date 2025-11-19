from book_library import Library

def main():
    library = Library()

    while True:
        print("\n--- Library Menu ---")
        print("1. Add Book")
        print("2. Issue Book")
        print("3. Return Book")
        print("4. Show Book Status")
        print("5. Show Library Stats")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            library.add_book(title, author)
            print("Book added successfully.")

        elif choice == "2":
            title = input("Enter book title to issue: ")
            borrower = input("Enter borrower name: ")
            if library.issue_book(title, borrower):
                print("Book issued successfully.")
            else:
                print("Book not available or not found.")

        elif choice == "3":
            title = input("Enter book title to return: ")
            if library.return_book(title):
                print("Book returned successfully.")
            else:
                print("Book was not issued or not found.")

        elif choice == "4":
            print("\n--- Book Status ---")
            for status in library.get_status():
                print(status)

        elif choice == "5":
            stats = library.get_stats()
            print("\n--- Library Stats ---")
            for key, value in stats.items():
                print(f"{key}: {value}")

        elif choice == "6":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()