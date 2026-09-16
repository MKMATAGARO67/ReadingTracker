CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    external_book_id TEXT UNIQUE NOT NULL,

    title TEXT NOT NULL,

    author TEXT NOT NULL,

    cover_url TEXT NOT NULL,

    reading_status TEXT NOT NULL
        CHECK (reading_status IN (
            'Want to Read',
            'Currently Reading',
            'Completed'
        )),

    date_added TEXT NOT NULL
)