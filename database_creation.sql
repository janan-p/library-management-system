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

Books Table
1|Book 1|Vasulevskiy|2002
2|Book 2|Robert|2022
3|Book 3|Rowling|2024
4|Book 4|Arthur|2020
5|Book 5|Arash|2017
6|Book 6|Rejwana|2017
7|Book 7|Archii|2020
8|Book 8|Dhanshri|2019
9|Book 9|Vasu|2069
10|Book 10|Arham|2018

Borrowings Table
1|arch@ualberta.ca|1|2023-11-15|
2|arch@ualberta.ca|2|2023-11-15|
3|siddh@ualberta.ca|3|2023-11-15|
4|keya@ualberta.ca|4|2023-10-15|2023-10-25
5|keya@ualberta.ca|5|2023-10-15|2023-10-25
6|dhiya@ualberta.ca|6|2023-10-15|2023-11-25
7|annoying@ualberta.ca|4|2023-10-15|2023-11-25
8|dhanshri@ualberta.ca|5|2023-10-15|2023-10-25
9|jpanchal@ualberta.ca|6|2023-11-15|
10|asshah1@ualberta.ca|7|2023-11-15|
    
Members Table
jpanchal@ualberta.ca|bestpersonalive|Janan|2003|CS
asshah1@ualberta.ca|annoyingiuc123|IUC|1980|Physics
viralkum@ualberta.ca|new-haircut|Vasulevskiy|2004|English
dhanshri@ualberta.ca|alwaysEXCITED|Dhanshri|1990|CS
arch@ualberta.ca|i_can_cook|Archi|2005|Engineering
siddh@ualberta.ca|TaLl|Siddhant|1980|Science
annoying@ualberta.ca|monkey_00|Om|2005|Business
dhiya@ualberta.ca|Cutie123|Dhiya|1990|English
keya@ualberta.ca|VasusJustFriend|Keya|2003|Science
jpanc@ualberta.ca|janan|jan|2004|CS
afhlfjl@ualberta.ca|faltu|test1|2003|Business
iuc@ualberta.ca|Hello|Aayushi|2005|Paleontoloy
hi@gmail.com|hi|hi|2005|cs
    
Penalties Table
1|1|10|
2|2|50|50
3|1|100|50
4|3|60|60
5|5|90|70
6|10|50|
7|12|70|70
8|4|50|20
9|4|50|20
10|6|100|
11|7|30|10
12|8|150|150
13|9|20|4
14|10|50|10
15|11|800|200
16|12|30|15
    
Reviews Table
1|2|siddh@ualberta.ca|4|Amazing book|2023-12-15
2|2|keya@ualberta.ca|3|Good storyline|2023-12-20
3|3|annoying@ualberta.ca|1|Yo that shit was ass|2023-12-30
4|1|arch@ualberta.ca|2|Good detail|2023-12-31
5|4|asshah1@ualberta.ca|1|Hate reading|2024-01-19
6|5|jpanchal@ualberta.ca|4|My favourite book|2023-02-23
