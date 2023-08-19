import cv2
import socket
import pickle
import struct
import time

ip = 'ec2-3-138-105-10.us-east-2.compute.amazonaws.com'
port = 5001

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((ip, port))

        print("connect")

        while True:
            retval, frame = capture.read()
            retval, frame = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 90])

            frame = pickle.dumps(frame)

            print("frame size : {} bytes".format(len(frame)))

            client_socket.sendall(struct.pack(">L", len(frame)) + frame)

            # 전송 속도 제한을 위한 슬립 추가
            time.sleep(0.03)

except Exception as e:
    print(f"예외 발생: {e}")

finally:
    capture.release()
