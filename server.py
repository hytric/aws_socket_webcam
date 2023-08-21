import socket
import cv2
import pickle
import struct
import sys

try:
    # 동영상 저장 파트
    videoFileName = 'output.avi'
    w = 640
    h = 480
    fps = 10
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    delay = round(1000 / fps)

    out = cv2.VideoWriter(videoFileName, fourcc, fps, (w, h))

    if not out.isOpened():
        raise IOError("파일을 열지 못하였습니다.")

    # 통신파트
    ip = "YOUR_IP_ADDRESS"
    port = "YOUR_PORT_NUMBER"

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('소켓이 생성되었습니다.')

    s.bind((ip, port))
    print('소켓 바인딩이 완료되었습니다.')
    s.listen(5)
    print('소켓이 수신 대기 상태입니다.')

    conn, addr = s.accept()

    data = b""
    payload_size = struct.calcsize(">L")
    print("payload_size: {}".format(payload_size))

    while True:
        try:
            # 영상 받는 파트
            while len(data) < payload_size:
                data += conn.recv(4096)

            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack(">L", packed_msg_size)[0]

            while len(data) < msg_size:
                data += conn.recv(4096)
            frame_data = data[:msg_size]
            data = data[msg_size:]

            frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

            # 동영상 저장파트
            inversed = cv2.flip(frame, 1)
            out.write(inversed)

            cv2.waitKey(1)

        except (socket.timeout, ConnectionResetError, ValueError) as e:
            print("데이터 수신 오류:", e)
            break

except (socket.error, KeyboardInterrupt) as e:
    print("소켓 오류:", e)

finally:
    if out.isOpened():
        out.release()

    if s is not None:
        s.close()
