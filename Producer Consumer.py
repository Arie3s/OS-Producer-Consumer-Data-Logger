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
import pyserial


class arduino:
    def __init__(self,port='COM3',baud=9600):
        self.serial = serial.Serial(port, baudrate=baud,timeout=1)

class Logger:
    # Shared buffer (queue) with a maximum capacity
    buffer = queue.Queue(maxsize=10)
    Run = False
    time = 100
    ms = 0

    def __init__(self):
        self.arduino = arduino().serial

    # Function for the producer
    def producer(self):
        i=0
        while self.Run:
            #data = self.arduino.readline().decode('utf-8').strip()
            self.buffer.put(i)
            print(f"Produced: {i}")
            i+=1
            time.sleep(0.1)

    # Function for the consumer
    def consumer(self):
        while self.Run:
            item = self.buffer.get()
            print(f"Consumed: {item}")
            time.sleep(0.2)

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






