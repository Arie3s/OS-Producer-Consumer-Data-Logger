#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      walit
#
# Created:     02/01/2024
# Copyright:   (c) walit 2024
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import threading
import queue
import time
import serial


class Arduino:
    def __init__(self, port='COM3', baud=9600):
        self.port = port
        self.baud = baud
        self.serial = None
        self.connect()

    def connect(self):
        try:
            self.serial = serial.Serial(self.port, baudrate=self.baud, timeout=1)
            print(f"Connected to Arduino on {self.port}")
        except serial.SerialException as e:
            print(f"Failed to connect to Arduino on {self.port}: {e}")

    def is_connected(self):
        return self.serial is not None and self.serial.isOpen()

    def read(self):
        if self.is_connected():
            data = self.serial.readline().decode('utf-8').strip()
            return data
        else:
            print("Arduino is not connected.")
            return None

    def write(self, data_to_send):
        if self.is_connected():
            self.serial.write(data_to_send.encode('utf-8'))
        else:
            print("Arduino is not connected.")

    def close(self):
        if self.is_connected():
            self.serial.close()


class Logger:

    def __init__(self):
        self.buffer = queue.Queue(maxsize=10)
        self.Run = False
        self.time = 100
        self.ms = 0

    # Function for the producer
    def producer(self):
        i=0
        with Arduino() as self.arduino:
            self.arduino.connect()
            while self.Run:
                value=self.arduino.read()
                self.buffer.put(i)
                print(f"Produced: {i}")
                i+=1
                time.sleep(0.1)

    # Function for the consumer
    def consumer(self):
        with open(f"Log-{time.strftime('%Y-%m-%d_%H-%M-%S')}.txt", "a") as self.file:
            while self.Run:
                try:
                    item = self.buffer.get()
                    self.file.write(f"{item}\n")
                except Exception as e:
                    print(f"Error writing to file: {e}")


    def timmer(self):
        while self.ms<=self.time:
            time.sleep(0.01)
            self.ms+=1
        self.Run = False


    def Log(self):
        # Create producer and consumer threads
        producer_thread = threading.Thread(target=self.producer)
        consumer_thread = threading.Thread(target=self.consumer)
        Timming_thread  = threading.Thread(target=self.timmer)

        self.Run=True

        # Start the threads
        producer_thread.start()
        consumer_thread.start()
        Timming_thread.start()

        # Wait for both threads to finish
        producer_thread.join()
        consumer_thread.join()
        Timming_thread.join()



Temperature=Logger()
Temperature.Log()
