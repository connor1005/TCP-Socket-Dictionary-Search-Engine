import socket
import threading
import re

def search_words(query, filename='wordlist.txt'):
    safe_query = re.escape(query)
    regex_str = safe_query.replace(r'\?', '.')
    pattern = re.compile(regex_str)
    
    matches = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                word = line.strip()
                if pattern.search(word):
                    matches.append(word)
    except FileNotFoundError:
        return "500 ERROR", 0, ""

    count = len(matches)
    if count > 0:
        return "200 OK", count, ",".join(matches)
    else:
        return "404 NOT FOUND", 0, ""

def handleClient(connection, address):
    print(f"[+] New thread started for {address}")
    try:
        while True:
            client_data = connection.recv(1024).decode('utf-8')
            if not client_data: 
                break 
            
            if client_data.startswith("QUERY "):
                query = client_data.split(" ", 1)[1].strip()
                status, count, words = search_words(query)
                
                response = f"{status} | {count} | {words}<EOF>"
                connection.sendall(response.encode('utf-8'))
            else:
                error_response = "400 BAD REQUEST | 0 | Invalid command<EOF>"
                connection.sendall(error_response.encode('utf-8'))
    except Exception as e:
        print(f"[-] Client error: {e}")
    finally:
        print(f"[-] Connection closed for {address}")
        connection.close()

def dispatcher():
    host = '127.0.0.1'
    port = 12000
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Multi-threaded server listening on {host}:{port}...")

    while True:
        connection, address = server_socket.accept()
        thread = threading.Thread(target=handleClient, args=(connection, address))
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    dispatcher()