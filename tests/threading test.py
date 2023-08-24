import threading
import time



def count(name):
    counter = 0
    starttime = time.perf_counter()
    for i in range(10000000):
        counter+=1

    print(name, time.perf_counter() -starttime)


def count2(name):
    counter = 0
    starttime = time.perf_counter()
    for i in range(100000):
        counter+=1

    print(name, time.perf_counter() -starttime)




if __name__ == '__main__':
    thread = threading.Thread(target=count, args=("thread1", ))
    thread.start()
    #
    count("main")
