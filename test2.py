import time

def signal_every_five_seconds():
    while True:
        # This function will be called every 5 seconds
        print("Signal!")
        time.sleep(5)
signal_every_five_seconds()