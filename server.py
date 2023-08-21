import socket
import cv2
import pickle
import struct ## new
import sys

# 동영상 저장 파트
# Set Video File Property
videoFileName = 'output.avi'
w = round(640)  # width
h = round(480)  # height
fps = 10 #cap.get(cv2.CAP_PROP_FPS)  # frame per second
fourcc = cv2.VideoWriter_fourcc(*'DIVX')  # fourcc
delay = round(1000 / fps)  # set interval between frame

# Save Video
out = cv2.VideoWriter(videoFileName, fourcc, fps, (w, h))
if not (out.isOpened()):
    print("File isn't opend!!")
    sys.exit()

# 통신파트
ip = #IP
port = #PORT

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('Socket created')

s.bind((ip,port))
print('Socket bind complete')
s.listen(10)
print('Socket now listening')

conn,addr=s.accept()

data = b""
payload_size = struct.calcsize(">L")
print("payload_size: {}".format(payload_size))


while True:
    # 영상 받는 파트
    while len(data) < payload_size:
        print("Recv: {}".format(len(data)))
        data += conn.recv(4096)

    print("Done Recv: {}".format(len(data)))
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    print("msg_size: {}".format(msg_size))
    while len(data) < msg_size:
        data += conn.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]

    frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

    # 동영상 저장파트
    inversed = cv2.flip(frame, 1)  # inversed frame
    out.write(inversed)  # save video frame
    
    cv2.waitKey(1)
