import serial
import socket
import time
import os
import threading

SERIAL_PORT = "COM11"  # Confirm this
BAUD_RATE = 115200
HOST = "0.0.0.0"
PORT = 12345

def start_listener():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((HOST, PORT))
        s.listen(1)
        print("Listener waiting for Pico W alerts...")
        while True:
            conn, addr = s.accept()
            data = conn.recv(1024).decode()
            print("Alert:", data)
            conn.close()
    except OSError as e:
        print(f"Listener error: {e}")

def scan_usb_drive(drive_path="D:/"):  # Update to your drive letter
    try:
        files = [f for f in os.listdir(drive_path) if os.path.isfile(os.path.join(drive_path, f))]
        return files
    except Exception as e:
        print(f"Error scanning USB: {e}")
        return ["test.txt", "virus.exe"]

def send_usb_data():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2)
        print("Serial opened successfully")
        time.sleep(2)
        usb_files = scan_usb_drive()
        print("Found files:", usb_files)
        for file in usb_files:
            print(f"Sending: '{file}'")
            ser.write((file + "\n").encode())
            response = ser.readline().decode().strip()
            if response:
                print(f"Pico says: {response}")
            else:
                print("No response from Pico")
        ser.close()
        print("Serial closed")
    except Exception as e:
        print(f"Serial error: {e}")

if __name__ == "__main__":
    threading.Thread(target=start_listener, daemon=True).start()
    send_usb_data()