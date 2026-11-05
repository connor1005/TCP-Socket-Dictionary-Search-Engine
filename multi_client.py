import socket

def run_multi_client():
    host = '127.0.0.1'
    port = 12000

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print("Connected to server. Type 'quit' to exit.")

    try:
        while True:
            raw_query = input("\nEnter wildcard query: ")
            
            if raw_query.strip().lower() == 'quit':
                break
            
            message = f"QUERY {raw_query}"
            client_socket.sendall(message.encode('utf-8'))
            
            response_chunks = []
            while True:
                chunk = client_socket.recv(4096).decode('utf-8')
                response_chunks.append(chunk)
                if "<EOF>" in chunk:
                    break
            
            response_data = "".join(response_chunks).replace("<EOF>", "")
            parts = [part.strip() for part in response_data.split('|')]
            
            if len(parts) >= 2:
                status = parts[0]
                count = parts[1]
                words = parts[2] if len(parts) > 2 else ""
                
                print(f"Server Status: {status}")
                print(f"Matches Found: {count}")
                
                if words:
                    print(f"Words: {words}")
            else:
                print(f"Unexpected response: {response_data}")

    finally:
        print("Closing connection.")
        client_socket.close()

if __name__ == "__main__":
    run_multi_client()