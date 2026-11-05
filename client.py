import socket

def run_basic_client():
    host = '127.0.0.1'
    port = 12000

    raw_query = input("Enter your wildcard query (e.g., a?t): ")
    
    message = f"QUERY {raw_query}"
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    try:
        client_socket.sendall(message.encode('utf-8'))
        
        response_chunks = []
        while True:
            chunk = client_socket.recv(4096)
            if not chunk:
                break
            response_chunks.append(chunk)
            
        response_data = b"".join(response_chunks).decode('utf-8')
        
        parts = [part.strip() for part in response_data.split('|')]
        
        if len(parts) >= 2:
            status = parts[0]
            count = parts[1]
            words = parts[2] if len(parts) > 2 else ""
            
            print(f"\nServer Status: {status}")
            print(f"Matches Found: {count}")
            
            if words:
                print(f"Words: {words}")
        else:
            print(f"Unexpected server response: {response_data}")

    finally:
        client_socket.close()

if __name__ == "__main__":
    run_basic_client()