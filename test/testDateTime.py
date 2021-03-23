from datetime import datetime
import time
def func(dt = datetime.utcnow()):
    print(dt)

func(1)
func()
time.sleep(2)
func(3)
func()