import re
import socket

import re

def search_words(query, filename='wordlist.txt'):
    # Escape special characters, then replace '\?' with '.' (exactly one char)
    safe_query = re.escape(query)
    regex_str = safe_query.replace(r'\?', '.')
    pattern = re.compile(regex_str)
    
    matches = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                word = line.strip()
                # .search() allows matching partial strings anywhere in the word
                if pattern.search(word):
                    matches.append(word)
    except FileNotFoundError:
        return "500 ERROR", 0, ""

    count = len(matches)
    if count > 0:
        return "200 OK", count, ",".join(matches)
    else:
        return "404 NOT FOUND", 0, ""

def run_basic_server():
    host = '127.0.0.1'
    port = 12000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server is listening on {host}:{port}")

    connection, address = server_socket.accept()
    print(f"Connection established with {address}")

    try:
        client_data = connection.recv(1024).decode('utf-8')
        print(f"Received data from client: {client_data}")

        if client_data.startswith("QUERY "):
            query = client_data.split(" ", 1)[1].strip()

            status, count, matches = search_words(query)

            response = f"{status}\n{count}\n{matches}"

            connection.sendall(response.encode('utf-8'))

        else:
            error_response = "400 BAD REQUEST\n0\n"
            connection.sendall(error_response.encode('utf-8'))

    finally:
        connection.close()
        server_socket.close()

if __name__ == "__main__":
    run_basic_server()