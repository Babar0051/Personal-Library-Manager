import streamlit as st
import json

LIBRARY_FILE = "library.json"

def load_library():
    try:
        with open(LIBRARY_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_library(library):
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file, indent=4)

def add_book(title, author, year, genre, read):
    library = load_library()
    library.append({
        "title": title,
        "author": author,
        "year": int(year),
        "genre": genre,
        "read": read
    })
    save_library(library)
    st.success("Book added successfully!")

def remove_book(title):
    library = load_library()
    updated_library = [book for book in library if book["title"].lower() != title.lower()]
    if len(library) == len(updated_library):
        st.warning("Book not found!")
    else:
        save_library(updated_library)
        st.success("Book removed successfully!")

def search_books(search_query, search_by):
    library = load_library()
    results = [book for book in library if search_query.lower() in book[search_by].lower()]
    return results

def display_books():
    library = load_library()
    if not library:
        st.info("Your library is empty!")
    else:
        for i, book in enumerate(library, 1):
            st.write(f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read'] else 'Unread'}")

def display_statistics():
    library = load_library()
    total_books = len(library)
    read_books = sum(1 for book in library if book["read"])
    percentage_read = (read_books / total_books * 100) if total_books > 0 else 0
    st.write(f"Total books: {total_books}")
    st.write(f"Percentage read: {percentage_read:.2f}%")

# Streamlit UI
st.title("📚 Personal Library Manager")
menu = st.sidebar.selectbox("Menu", ["Add a Book", "Remove a Book", "Search for a Book", "Display All Books", "Display Statistics"])

if menu == "Add a Book":
    with st.form("add_form"):
        title = st.text_input("Title")
        author = st.text_input("Author")
        year = st.number_input("Publication Year", min_value=0, max_value=2025, step=1)
        genre = st.text_input("Genre")
        read = st.checkbox("Read")
        submitted = st.form_submit_button("Add Book")
        if submitted:
            add_book(title, author, year, genre, read)

elif menu == "Remove a Book":
    title = st.text_input("Enter the title of the book to remove")
    if st.button("Remove Book"):
        remove_book(title)

elif menu == "Search for a Book":
    search_option = st.radio("Search by", ("title", "author"))
    search_query = st.text_input("Enter search term")
    if st.button("Search"):
        results = search_books(search_query, search_option)
        if results:
            for book in results:
                st.write(f"{book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read'] else 'Unread'}")
        else:
            st.warning("No matching books found!")

elif menu == "Display All Books":
    display_books()

elif menu == "Display Statistics":
    display_statistics()
