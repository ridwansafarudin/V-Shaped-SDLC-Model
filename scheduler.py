'''
Had the idea to create something like Google Calendar since it's
quite annoying to use. So I created my inferior one. Which is easier
for me to use since I'm the creator.
'''
import time
import pandas as pd
import datetime as dt
from tinydb import TinyDB, Query
from win10toast import ToastNotifier

db = TinyDB('scheduler/db.json')
schedule = Query()

def insert(title, date, time, end, repeat='no'):
    '''
    date format ddmmyyyy
    time & end format hhmm
    '''
    search = db.get((schedule.time == time) & (schedule.date == date))

    if search:
        print('It already exist. You might want to reschedule.')
        print(search['title'])
        return False
    
    db.insert({'title': title,
                'date': date,
                'time': time,
                'end': end,
                'repeat': repeat})
    print('Created a new schedule {}'.format(title))
    print('{}-{}-{} {}:{}-{}:{}'.format(date[:2], 
                                        date[2:4], 
                                        date[4:8], 
                                        time[:2],
                                        time[2:4],
                                        end[:2],
                                        end[2:4]))
    
def remove(date, time):
    '''
    date format ddmmyyyy
    time format hhmm
    '''
    search = db.get((schedule.date == date) & (schedule.time == time))
    if search:
        confirm = int(input('Delete -{}- schedule?'.format(search['title'])))
        if confirm:
            db.remove(doc_ids=[search.doc_id])
        else:
            print('Canceled')
    else:
        print("It doesn't exist.")
        
def checktime():
    '''
    Grab schedule in the current time.
    '''
    altered_time = dt.datetime.now()
    time = ''.join([str(altered_time.hour).zfill(2),
                    str(altered_time.minute).zfill(2)]) # Same as "%02d"
    date = ''.join(['%02d' % dt.datetime.now().day,
                    '%02d' % dt.datetime.now().month, # Same as zfill(2)
                    str(dt.datetime.now().year)])
    result = db.get((schedule.time == time) & (schedule.date == date))
    
    return result

def schedules():
    '''
    List out the schedules, sorted.
    '''
    print('Schedules: ')
    container = {}
    darray = []
    for item in db.all():
        darray.append(item)
    for keys in darray[0].keys():
        container[keys] = [b[keys] for b in darray]
    df = pd.DataFrame.from_dict(container)
    return df.sort_values(by=['time', 'date'], ascending=[True, False])
    
if __name__ == '__main__':
    print('Calendar Reminder - Booting')
    print('Made by Kylamber, Loops every one minute.')
    while True:
        result = checktime()
        if result:
            date_and_time = '{}-{}-{} {}:{}-{}:{}'.format(result['date'][:2], 
                                            result['date'][2:4], 
                                            result['date'][4:8], 
                                            result['time'][:2],
                                            result['time'][2:4],
                                            result['end'][:2],
                                            result['end'][2:4])
            print('Schedule : {}'.format(result['title']))
            print(date_and_time)
            ToastNotifier().show_toast(result['title'], date_and_time)
            db.remove(doc_ids=[result.doc_id])
        time.sleep(60)
