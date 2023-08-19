# 필요한 패키지 import
import socket  # 소켓 프로그래밍에 필요한 API를 제공하는 모듈
import struct  # 바이트(bytes) 형식의 데이터 처리 모듈
import pickle  # 객체의 직렬화 및 역직렬화 지원 모듈
import cv2  # OpenCV(실시간 이미지 프로세싱) 모듈

# 서버 ip 주소 및 port 번호
ip = 'ec2-3-138-105-10.us-east-2.compute.amazonaws.com'
port = 50001

# 소켓 객체 생성
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 소켓 주소 정보 할당
server_socket.bind((ip, port))

# 연결 리스닝(동시 접속) 수 설정
server_socket.listen(10)

print('클라이언트 연결 대기')

# 연결 수락(클라이언트 (소켓, 주소 정보) 반환)
client_socket, address = server_socket.accept()
print('클라이언트 ip 주소 :', address[0])

# 수신한 데이터를 넣을 버퍼(바이트 객체)
data_buffer = b""

# calcsize : 데이터의 크기(byte)
# - L : 부호없는 긴 정수(unsigned long) 4 bytes
data_size = struct.calcsize("L")

while True:
    try:
        while len(data_buffer) < data_size:
            # 데이터 수신
            data = client_socket.recv(4096)
            if not data:
                break
            data_buffer += data

        if not data_buffer:
            break

        packed_data_size = data_buffer[:data_size]
        data_buffer = data_buffer[data_size:]

        if len(packed_data_size) != 4:
            print("데이터 크기가 부족하여 수신을 중단했습니다.")
            break

        frame_size = struct.unpack(">L", packed_data_size)[0]

        while len(data_buffer) < frame_size:
            # 데이터 수신
            data = client_socket.recv(4096)
            if not data:
                break
            data_buffer += data

        if not data_buffer:
            break

        frame_data = data_buffer[:frame_size]
        data_buffer = data_buffer[frame_size:]

        frame = pickle.loads(frame_data)
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
        cv2.imshow('Frame', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
    except Exception as e:
        print(f"예외 발생: {e}")
        break

# 소켓 닫기
client_socket.close()
server_socket.close()
print('연결 종료')

# 모든 창 닫기
cv2.destroyAllWindows()
