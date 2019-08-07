import serial
from loguru import logger
from time import sleep

def serialSend(charToSend, port='COM16', baudrate=115200):
    def send():
        try:
            with serial.Serial(port=port, baudrate=baudrate, bytesize=8, parity="E", stopbits=1, timeout=0.05) as s:
                s.write(charToSend.encode('utf-8'))
            logger.info(f"Sending Serial Cmd: {charToSend}")
        except:
            logger.warning(f"Failed to send - cmd: {charToSend} to port: {port} at baudrate:{baudrate}")

    return send

def checkSerial():
    a = serialSend('A')
    b = serialSend('B')
    x = serialSend('X')
    y = serialSend('Y')
    
    logger.info("Sending A command")
    a()
    sleep(1)
    logger.info("Sending B command")
    b()
    sleep(1)
    logger.info("Sending X command")
    x()
    sleep(1)
    logger.info("Sending y command")
    y()
    sleep(1)



if __name__ == "__main__":
    checkSerial()