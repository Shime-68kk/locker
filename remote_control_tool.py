
import socket
import subprocess

# SERVER SIDE (máy cần điều khiển)
def server():
    HOST = '0.0.0.0'
    PORT = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f'Server đang nghe tại {HOST}:{PORT}')
        conn, addr = s.accept()
        with conn:
            print('Kết nối từ', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                cmd = data.decode()
                output = subprocess.getoutput(cmd)
                conn.sendall(output.encode())

# CLIENT SIDE (máy điều khiển)
def client():
    HOST = input('Nhập địa chỉ IP của máy cần điều khiển: ')
    PORT = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print('Đã kết nối đến server')
        while True:
            cmd = input('Remote Shell> ')
            if cmd.lower() == 'exit':
                break
            s.sendall(cmd.encode())
            data = s.recv(4096)
            print(data.decode())

# Chọn mode (client hoặc server)
mode = input('Chọn mode (server/client): ').lower()
if mode == 'server':
    server()
elif mode == 'client':
    client()
else:
    print('Chế độ không hợp lệ!')
