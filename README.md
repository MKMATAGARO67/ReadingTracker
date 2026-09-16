# Reading Tracker

A full-stack personal reading tracker for managing books, tracking reading progress, and organizing a personal reading library.

## Project Status

**In Development**

The project is being developed incrementally, starting with the Flask backend and REST API.

## Tech Stack

### Backend

* Python
* Flask
* SQLite
* REST API

### Frontend

* React *(planned)*

### Development & Testing

* Git
* GitHub
* Cypress *(planned)*

## Current Features

* [x] Flask backend setup
* [x] SQLite database setup
* [x] Book database schema
* [x] GET saved books endpoint
* [ ] Search for books
* [ ] Save a book
* [ ] Update reading status
* [ ] Remove a saved book
* [ ] React frontend
* [ ] Automated API testing
* [ ] End-to-end testing

## Planned Reading Statuses

Books will use the following reading statuses:

* Want to Read
* Currently Reading
* Completed

## Project Structure

```text
ReadingTracker/
├── backend/
│   ├── app.py
│   ├── database.py
│   ├── requirements.txt
│   └── schema.sql
│
├── frontend/
│
├── .gitignore
└── README.md
```

## API

The backend API is organized under:

```text
/api/
```

Planned endpoints include:

Method: GET
Endpoint: `/api/search?title=...` 
Purpose: Search for books

Method: GET
Endpoint: `/api/books`
Purpose: Retrieve saved books

Method: POST
Endpoint: `/api/books`
Purpose: Save a book

Method: PATCH
Endpoint: `/api/books/<id>`
Purpose: Update the reading status

Method: DELETE
Endpoint: `/api/books/<id>`
Purpose: Remove a saved book



## Development Approach

The project is being built incrementally. Each feature is implemented, tested, committed, and pushed to GitHub as development progresses.

## Future Improvements

* Book recommendations
* Reading progress tracking
* Favorites
* External book API integration
* User authentication
* Automated testing
* Responsive frontend
* Deployment
