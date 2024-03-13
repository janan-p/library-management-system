drop table if exists members;
drop table if exists books;
drop table if exists borrowings;
drop table if exists penalties;
drop table if exists reviews;

PRAGMA foreign_keys = ON;

CREATE TABLE members (
    email CHAR(100),
    passwd CHAR(100),
    name CHAR(255) NOT NULL,
    byear INTEGER,
    faculty CHAR(100),
    PRIMARY KEY (email)
);

CREATE TABLE books (
    book_id INTEGER,
    title CHAR(255),
    author CHAR(150),
    pyear INTEGER,
    PRIMARY KEY (book_id)
);

CREATE TABLE borrowings(
    bid INTEGER,
    member CHAR(100) NOT NULL,
    book_id INTEGER NOT NULL,
    start_date DATE,
    end_date DATE,
    PRIMARY KEY (bid),
    FOREIGN KEY (member) REFERENCES members(email),
    FOREIGN KEY (book_id) REFERENCES books(book_id)
);

CREATE TABLE penalties(
    pid INTEGER,
    bid INTEGER NOT NULL,
    amount INTEGER,
    paid_amount INTEGER,
    PRIMARY KEY (pid),
    FOREIGN KEY (bid) REFERENCES borrowings(bid)
);

CREATE TABLE reviews(
    rid INTEGER,
    book_id INTEGER NOT NULL,
    member CHAR(100) NOT NULL,
    rating INTEGER NOT NULL,
    rtext CHAR(255),
    rdate DATE,
    PRIMARY KEY (rid),
    FOREIGN KEY (member) REFERENCES members(email),
    FOREIGN KEY (book_id) REFERENCES books(book_id)
);

INSERT INTO members values('jpanchal@ualberta.ca', 'bestpersonalive', 'Janan', 2003, 'CS');
INSERT INTO members values('asshah1@ualberta.ca','annoyingiuc123', 'IUC', 1980, 'Physics');
INSERT INTO members values('viralkum@ualberta.ca', 'new-haircut', 'Vasulevskiy', 2004, 'English');
INSERT INTO members values('dhanshri@ualberta.ca', 'alwaysEXCITED', 'Dhanshri', 1990, 'CS');
INSERT INTO members values('arch@ualberta.ca', 'i_can_cook', 'Archi', 2005, 'Engineering');
INSERT INTO members values('siddh@ualberta.ca', 'TaLl', 'Siddhant', 1980, 'Science');
INSERT INTO members values('annoying@ualberta.ca', 'monkey_00', 'Om', 2005, 'Business');
INSERT INTO members values('dhiya@ualberta.ca', 'Cutie123', 'Dhiya', 1990, 'English');
INSERT INTO members values('keya@ualberta.ca', 'VasusJustFriend', 'Keya', 2003, 'Science');

INSERT INTO books values(1, 'Book 1', 'Vasulevskiy', 2002);
INSERT INTO books values(2, 'Book 2', 'Robert', 2022);
INSERT INTO books values(3, 'Book 3', 'Rowling', 2024);
INSERT INTO books values(4, 'Book 4', 'Arthur', 2020);
INSERT INTO books values(5, 'Book 5', 'Arash', 2017);
INSERT INTO books values(6, 'Book 6', 'Rejwana', 2017);


INSERT INTO borrowings values(1, 'arch@ualberta.ca', 1, '2023-11-15', NULL);
INSERT INTO borrowings values(2, 'arch@ualberta.ca', 1, '2023-11-15', NULL);
INSERT INTO borrowings values(3, 'siddh@ualberta.ca', 2, '2023-11-15', NULL);
INSERT INTO borrowings values(4, 'keya@ualberta.ca', 2, '2023-10-15', '2023-10-25');
INSERT INTO borrowings values(5, 'keya@ualberta.ca', 3, '2023-10-15', '2023-10-25');
INSERT INTO borrowings values(6, 'dhiya@ualberta.ca', 3, '2023-10-15', '2023-11-25');
INSERT INTO borrowings values(7, 'annoying@ualberta.ca', 3, '2023-10-15', '2023-11-25');
INSERT INTO borrowings values(8, 'dhanshri@ualberta.ca', 3, '2023-10-15', '2023-10-25');
INSERT INTO borrowings values(9, 'jpanchal@ualberta.ca', 4, '2023-11-15', NULL);
INSERT INTO borrowings values(10, 'asshah1@ualberta.ca', 4, '2023-11-15', NULL);
INSERT INTO borrowings values(11, 'viralkum@ualberta.ca', 4, '2023-11-15', NULL);
INSERT INTO borrowings values(12, 'jpanchal@ualberta.ca', 5, '2023-11-15', NULL);

INSERT INTO penalties values(1, 1, 50, NULL);
INSERT INTO penalties values(2, 2, 50, 20);
INSERT INTO penalties values(3, 1, 50, 50);
INSERT INTO penalties values(4, 3, 60, 60);
INSERT INTO penalties values(5, 5, 90, 70);
INSERT INTO penalties values(6, 10, 50, NULL);
INSERT INTO penalties values(7, 12, 70, 70);

INSERT INTO reviews values(1, 2, 'siddh@ualberta.ca', 4, 'Amazing book','2023-12-15');
INSERT INTO reviews values(2, 2, 'keya@ualberta.ca', 3, 'Good storyline','2023-12-20');
INSERT INTO reviews values(3, 3, 'annoying@ualberta.ca', 1, 'I hated this book','2023-12-30');
INSERT INTO reviews values(4, 1, 'arch@ualberta.ca', 2, 'Good detail','2023-12-31');
INSERT INTO reviews values(5, 4, 'asshah1@ualberta.ca', 1, 'Hate reading','2024-01-19');
INSERT INTO reviews values(6, 5, 'jpanchal@ualberta.ca', 4, 'My favourite book','2023-02-23');