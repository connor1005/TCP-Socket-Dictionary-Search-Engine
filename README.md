# TCP Socket Dictionary Search Engine

A client-server application built in Python that queries a dictionary text file using wildcard strings. This project was built to demonstrate foundational TCP socket programming, application-level protocol design, and multi-threading.

## Table of Contents
- [Features](#-features)
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [Application-Level Protocol](#-application-level-protocol)
- [Design Tradeoffs & Architecture](#-design-tradeoffs--architecture)

---

## Features

* **Wildcard Searching:** Search a dictionary file (`wordlist.txt`) using `?` as a wildcard for any single character (e.g., `a?t` matches `ant`, `art`, `act`).
* **Basic TCP Client/Server:** A single-threaded implementation handling one request at a time.
* **Multi-threaded TCP Server:** Utilizes Python's `threading` module to serve multiple clients concurrently without blocking.
* **Custom Protocol:** A lightweight, HTTP-inspired text protocol designed for reliable data parsing and chunking over continuous TCP streams.

---

## Project Structure

```text
.
├── server.py          # Single-threaded basic TCP server
├── client.py          # Basic TCP client (single query)
├── multi_server.py    # Multi-threaded TCP server 
├── multi_client.py    # Looped TCP client (continuous queries)
├── wordlist.txt       # The dictionary text file for lookups
└── README.md          # Project documentation
```

---

## Quick Start

Ensure you have Python 3 installed and that `wordlist.txt` is located in the same directory as the scripts.

### 1. Start the Server
Open a terminal and run the multi-threaded server. It will automatically bind to `127.0.0.1:12000`.
```bash
python3 multi_server.py
```

### 2. Start the Client
Open a separate terminal window (or multiple windows to test concurrency) and run the client:
```bash
python3 multi_client.py
```

### 3. Send Queries
Enter wildcard queries when prompted. Type `quit` to close the connection.
```text
Enter wildcard query: a?t
Server Status: 200 OK
Matches Found: 25
Words: abt, act, aft, alt, ant, apt, art, ...
```
*Note: Massive queries like `??????????` (24,071 matches) or `?` (69,903 matches) are fully supported via stream chunking.*

---

## Application-Level Protocol

The application communicates over TCP using a custom, UTF-8 encoded text protocol. 

### Message Formats

| Direction | Format | Example |
| :--- | :--- | :--- |
| **Request** | `QUERY <wildcard_string>` | `QUERY a?t` |
| **Response** | `<STATUS_CODE> \| <COUNT> \| <WORDS><EOF>` | `200 OK \| 3 \| ant,art,act<EOF>` |

### Status Codes
Borrowing from HTTP conventions, the server responds with:
* `200 OK`: Successful match(es) found.
* `404 NOT FOUND`: Zero matches found for the query.
* `400 BAD REQUEST`: Malformed command received from the client.
* `500 ERROR`: Internal server error (e.g., `wordlist.txt` missing).

### Data Chunking
Because TCP streams data without inherently defining the payload size, the server appends an `<EOF>` (End of File) tag to the end of its response. The multi-threaded client continuously reads 4096-byte chunks until it detects this `<EOF>` marker, preventing the truncation of massive datasets and ensuring complete data transfer.