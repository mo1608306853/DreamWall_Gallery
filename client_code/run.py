import os
import time
import sched
import datetime

from method_client import MethodClient


def time_printer(s):
    date_format = '%Y-%m-%d %H:%M:%S'
    now_time = datetime.datetime.now().strftime(date_format)
    year, month, day, hour, minute, second, weekday, yearday, isdst= time.strptime(now_time, date_format)
    if second == 0:
        MethodClient(hour, minute).run_method()
    s.enter(1, 1, time_printer, (s,))  

def loop_monitor():
    s = sched.scheduler(time.time, time.sleep)
    s.enter(1, 1, time_printer, (s,))
    s.run()
    

if __name__ == "__main__":
    setup_data = MethodClient().read_json()
    always_display = setup_data['always_display']
    if always_display:
        os.popen('python tkinter_util.py')
    loop_monitor()
