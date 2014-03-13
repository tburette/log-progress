import datetime

start = datetime.datetime.now()

while True:
    time.sleep(15)
    print datetime.datetime.now() - start
