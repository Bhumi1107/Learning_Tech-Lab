CREATE TABLE books (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL
);
CREATE TABLE copies (
    id INTEGER PRIMARY KEY,
    book_id INTEGER NOT NULL REFERENCES books(id)
);
CREATE TABLE loans (
    id INTEGER PRIMARY KEY,
    copy_id INTEGER NOT NULL REFERENCES copies(id),
    borrowed_on TEXT NOT NULL,
    returned_on TEXT,
    CHECK (returned_on IS NULL OR returned_on >= borrowed_on)
);
CREATE INDEX loans_by_copy_date ON loans(copy_id, borrowed_on);

INSERT INTO books VALUES (1, 'Database Systems'), (2, 'Graph Theory'), (3, 'Python Basics');
INSERT INTO copies VALUES (101, 1), (102, 1), (301, 3);
INSERT INTO loans VALUES
    (1, 101, '2026-11-01', '2026-11-06'),
    (2, 101, '2026-11-18', '2026-11-24'),
    (3, 102, '2026-11-20', NULL),
    (4, 301, '2026-11-25', NULL);
