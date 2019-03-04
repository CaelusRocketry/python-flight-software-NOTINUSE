import adafruit_rfm9x

rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
rfm9x.tx_power = 23

def send(msg):
    rfm9x.send(msg)

def recieve():
    return rfm9x.receive()
