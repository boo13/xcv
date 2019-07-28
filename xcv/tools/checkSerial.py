import serial
from loguru import logger


def serialSend(charToSend, port='COM21', baudrate=115200):
    def send():
        try:
            with serial.Serial(port=port, baudrate=baudrate, bytesize=8, parity="E", stopbits=1, timeout=0.05) as s:
                s.write(charToSend.encode('utf-8'))
            logger.info(f"Sending Serial Cmd: {charToSend}")
        except:
            logger.warning(f"Failed to send - cmd: {charToSend} to port: {port} at baudrate:{baudrate}")

    return send

if __name__ == "__main__":
    a = serialSend('A')
    b = serialSend('B')
    x = serialSend('X')
    y = serialSend('Y')
    
    logger.info("Sending A command")
    a()
    logger.info("Sending B command")
    b()
    logger.info("Sending X command")
    x()
    logger.info("Sending y command")
    y()

