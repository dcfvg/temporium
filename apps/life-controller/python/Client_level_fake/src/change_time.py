'''
Created on May 1, 2014

@author: glogzy
'''
# -*- encoding: utf-8 -*-

import time 
from threading import Timer
import datetime
is_alive = False
 
class clock(object):
    """Not sure is_alive is still usefull, it's goal is not to start the clock when you create it"""
    global is_alive
    is_alive = True
    
    def __init__(self):
        self.lcl = datetime.datetime.today()
        self.init_day  = self.lcl.day
        self.init_hour  = self.lcl.hour
        self.init_minute  = self.lcl.minute
        self.init_second  = self.lcl.second
        self.start_clock = True

 
    def set_time(self):
        if self.start_clock:
            self.start_clock = False
            lclstr = self.lcl.strftime('%A %d %B %Y, %H:%M:%S')
            print (lclstr)
            self.init_hour = self.lcl.hour
            self.init_day = self.lcl.day
        else:
            self.lcl = self.lcl + datetime.timedelta(seconds = 1)
            lclstr = self.lcl.strftime('%A %d %B %Y, %H:%M:%S')
            print (lclstr)
        if is_alive:
            timer = Timer(1, self.set_time)
            timer.start()

    def day(self):
        return self.lcl.day
            
    def hour(self):
        return self.lcl.hour
            
    def minute(self):
        return self.lcl.minute

    def second(self):
        return self.lcl.second
    
    def time(self):
        """Send back the time in seconds, doesn't work if the month change"""
        if (self.day() - self.init_day) > 0 :
            return (24 - self.init_hour) + ((self.day() - self.init_day) - 1)*24 + self.hour()
        else:
            duration_hour = (self.hour() - self.init_hour)
            
        if (self.minute() - self.init_minute) >= 0 :
            duration_hour = duration_hour + 1
            duration_minute = self.minute() - self.init_minute
        else : 
            duration_minute = (60 - self.init_minute) + self.minute()
            
        if (self.second() - self.init_second) >= 0 :
            duration_minute = duration_minute + 1
            duration_second = self.second() - self.init_second
        else : 
            duration_second = (60 - self.init_second) + self.second()
            
        return duration_hour*3600 + duration_minute*60 + duration_second
 
if __name__ == '__main__':
    """"a = clock()
    a.set_time()
    time.sleep(4)
    b = a.lcl.strftime('%A %d %B %Y, %H:%M:%S')
    print(b)
    time.sleep(4)
    c = a.lcl.strftime('%A %d %B %Y, %H:%M:%S')
    print (c)
    print (a.duration())"""
    fake_time = clock()
    fake_time.set_time()   
    a = fake_time.time()
    time.sleep(10.001)
    b = fake_time.time() - a
    print(a)
    print(b)
   
