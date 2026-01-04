import socket
import time
import math

UDP_IP = "127.0.0.1"
UDP_PORT = 42674

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send(msg):
    sock.sendto(msg.encode("utf-8"), (UDP_IP, UDP_PORT))

# ---- Send header ----
send("FileType=text/acmi/tacview\n")
send("FileVersion=2.2\n")
send("0,ReferenceTime=2025-01-01T00:00:00Z\n")

# ---- Create object ----
send("1,Type=Air+FixedWing,Name=Python Jet\n")

start_time = time.time()

while True:
    t = time.time() - start_time

    lon = 10.0 + t * 0.001
    lat = 45.0
    alt = 3000 + math.sin(t) * 100

    roll = math.sin(t) * 0.2
    pitch = math.cos(t) * 0.1
    yaw = t % (2 * math.pi)

    msg = (
        f"#{t:.2f}\n"
        f"1,T={lon}|{lat}|{alt},Roll={roll},Pitch={pitch},Yaw={yaw}\n"
    )

    send(msg)
    time.sleep(0.05)  # 20 Hz
