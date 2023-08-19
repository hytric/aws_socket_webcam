
import socket
import cv2

ip = 'ec2-3-138-105-10.us-east-2.compute.amazonaws.com'
port = 5001

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    d = frame.flatten()
    s = d.tostring()

    for i in range(20):
        sock.sendto(bytes([i]) + s[i*46080:(i+1)*46080], (UDP_IP, UDP_PORT))

 

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
