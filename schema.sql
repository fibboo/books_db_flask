DROP TABLE IF EXISTS books;

CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    number_of_pages INTEGER NOT NULL,
    review TEXT NOT NULL
);