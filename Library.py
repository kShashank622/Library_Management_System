import hashlib

class Library:
    def __init__(self,file_name):
        self.file_name = file_name
        self.books = {}
        self.borrowers = {}
        self.load_data()

    def load_data(self):
        try:
            with open(self.file_name, 'r') as file:
                for line in file:
                    data_type, data = line.strip().split(':')
                    if data_type == 'book':
                        book_id, book_name = data.split(',')
                        self.books[book_id] = book_name
                    elif data_type == 'borrower':
                        borrower_id, borrower_name = data.split(',')
                        self.borrowers[borrower_id] = {'name': borrower_name, 'books': []}
        except FileNotFoundError:
            pass

    def save_data(self):
        with open(self.file_name, 'w') as file:
            for book_id, book_name in self.books.items():
                file.write(f"book:{book_id},{book_name}\n")
            for borrower_id, borrower_data in self.borrowers.items():
                borrower_name = borrower_data['name']
                file.write(f"borrower:{borrower_id},{borrower_name}\n")

    def add_book(self, book_id, book_name):
        self.books[book_id] = book_name
        self.save_data()

    def remove_book(self, book_id):
        if book_id in self.books:
            del self.books[book_id]
            self.save_data()

    def add_borrower(self, borrower_id, borrower_name):
        self.borrowers[borrower_id] = {'name': borrower_name, 'books': []}
        self.save_data()

    def remove_borrower(self, borrower_id):
        if borrower_id in self.borrowers:
            del self.borrowers[borrower_id]
            self.save_data()

    def borrow_book(self, book_id, borrower_id):
        if book_id in self.books and borrower_id in self.borrowers:
            borrower_data = self.borrowers[borrower_id]
            borrower_books = borrower_data['books']
            if book_id not in borrower_books:
                borrower_books.append(book_id)
                self.save_data()
                return True
        return False

    def return_book(self, book_id, borrower_id):
        if book_id in self.books and borrower_id in self.borrowers:
            borrower_data = self.borrowers[borrower_id]
            borrower_books = borrower_data['books']
            if book_id in borrower_books:
                borrower_books.remove(book_id)
                self.save_data()
                return True
        return False

    def search_book(self, book_id):
        if book_id in self.books:
            return self.books[book_id]
        else:
            return None

    def get_borrowed_books(self, borrower_id):
        if borrower_id in self.borrowers:
            borrower_data = self.borrowers[borrower_id]
            return borrower_data['books']
        else:
            return []

    def get_books_borrowed_count(self, borrower_id):
        if borrower_id in self.borrowers:
            borrower_data = self.borrowers[borrower_id]
            return len(borrower_data['books'])
        else:
            return 0

    def get_books_left_count(self):
        return len(self.books)

    @staticmethod
    def generate_hash(data):
        hasher = hashlib.sha256()
        hasher.update(str(data).encode('utf-8'))
        return hasher.hexdigest()

''' def sha1(st, x):
        sm = 0
        for i in range(1, len(st)):
            sm += ord(st[i]) + ord(st[i - 1])
            sm = sm % 997
        h[sm] = x
        return sm

    def sha2(st):
        sm = 0
        for i in range(1, len(st)):
            sm += ord(st[i]) + ord(st[i - 1])
            sm = sm % 997
        return sm'''

library = Library("library_data.txt")

while True:
    print("\n---- Library Management System ----")
    print("1.  Add Book")
    print("2.  Remove Book")
    print("3.  Add Borrower")
    print("4.  Remove Borrower")
    print("5.  Borrow Book")
    print("6.  Return Book")
    print("7.  Search Book")
    print("8.  Display Borrower's Borrowed Books")
    print("9.  Display Books Owned by the Library")
    print("10. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        book_id = input("Enter Book ID: ")
        book_name = input("Enter Book Name: ")
        library.add_book(book_id, book_name)
        print("Book added successfully!")

    elif choice == "2":
        book_id = input("Enter Book ID: ")
        library.remove_book(book_id)
        print("Book removed successfully!")

    elif choice == "3":
        borrower_id = input("Enter Borrower ID: ")
        borrower_name = input("Enter Borrower Name: ")
        library.add_borrower(borrower_id, borrower_name)
        print("Borrower added successfully!")

    elif choice == "4":
        borrower_id = input("Enter Borrower ID: ")
        library.remove_borrower(borrower_id)
        print("Borrower removed successfully!")

    elif choice == "5":
        book_id = input("Enter Book ID: ")
        borrower_id = input("Enter Borrower ID: ")
        if library.borrow_book(book_id, borrower_id):
            print("Book borrowed successfully!")
        else:
            print("Failed to borrow book. Please check Book ID and Borrower ID.")

    elif choice == "6":
        book_id = input("Enter Book ID: ")
        borrower_id = input("Enter Borrower ID: ")
        if library.return_book(book_id, borrower_id):
            print("Book returned successfully!")
        else:
            print("Failed to return book. Please check Book ID and Borrower ID.")

    elif choice == "7":
        book_id = input("Enter Book ID: ")
        book_name = library.search_book(book_id)
        if book_name:
            print(f"Book Name: {book_name}")
        else:
            print("Book not found!")

    elif choice == "8":
        borrower_id = input("Enter Borrower ID: ")
        borrowed_books = library.get_borrowed_books(borrower_id)
        if borrowed_books:
            print("Borrowed Books:")
            for book_id in borrowed_books:
                book_name = library.search_book(book_id)
                print(f"Book ID: {book_id}, Book Name: {book_name}")
        else:
            print("No books borrowed by the borrower.")

    elif choice == "9":
        books_left = library.get_books_left_count()
        print(f"Total books owned by the Library: {books_left}")

    elif choice == "10":
        print("Exiting Library Management System...")
        break

    else:
        print("Invalid choice. Please try again.")
