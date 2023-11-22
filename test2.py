import time

counter = 0

def increase_counter():
    global counter
    while True:
        counter += 1
        print(counter)
        time.sleep(1)

increase_counter()
