'''
Nils Napp Mar 2021
Script to group and count the entry/exit events form beetunnel filenames
'''


import pathlib as path
import datetime as dt
import numpy as np
from matplotlib import pyplot as plt

#Time difference for grouping images
DELTA_T_SEC=5

DIR_REL='Q1/run-2105__2021-03-08_08-59-53_top-1'
DIR_REL='N2/run_top-3___2021-03-08_09-00-22'

FMT_STR='%Y-%m-%d_%H-%M-%S_%f'
MIN_PIC = 4



def tstr(fname):
    parts=fname.split('_')
    return parts[0] + '_' +  parts[1] + '_' + parts[2]

def delta_dt_sec(dt1,dt2):
    delta = dt2 - dt1
    return delta.days * 24*60*60 + delta.seconds + delta.microseconds/1000000

def get_events(DIR_REL):
    p = path.Path(DIR_REL)
    dtimes=[dt.datetime.strptime(tstr(f.name),FMT_STR) for f in p.glob('*.jpg')]

    dtimes.sort()


    if len(dtimes) <=2:
        print(f'Warning: Not enough images in "{DIR_REL}".')
        return None

    events=[0]
    event_delta=[]
    dt0=dtimes[0]
    dt_last=dt0
    pic_per_ev=[]
    pic_cnt=0

    dt_list=[]
    
    for d in dtimes:
        pic_cnt += 1
        ev_del=delta_dt_sec(dt_last,d)

        if ev_del > DELTA_T_SEC:
            if pic_cnt < MIN_PIC:
                print(f'Removing Event at {d}, less than {MIN_PIC} pictures.')
                pic_cnt=1
            else:
                pic_per_ev.append(pic_cnt)
                pic_cnt=1
                events.append(delta_dt_sec(dt0,d))
                event_delta.append(ev_del)
        else:
            print (ev_del)
            if ev_del < .2:
                dt_list.append(ev_del)
                    
            
        dt_last = d

    print(f'There were {len(events)} entry or exit events with a min delta={DELTA_T_SEC} seconds.')
    print(f'Dt mean = {1/np.mean(dt_list)}.')
    
    ret={}
    ret['events']=events
    ret['event_delta']=event_delta
    ret['event_cnt']=pic_per_ev
    ret['start_dt']=dtimes[0]
    ret['ev_dt']=dt_list
    return ret


r1=get_events('N2/run_top-3___2021-03-08_09-00-22')
r2=get_events('Q1/run-2105__2021-03-08_08-59-53_top-1')
r3=get_events('run_top-3___2021-03-12_08-50-38')
r4=get_events('run_top-4___2021-03-12_08-50-27')


runs=[r1,r2,r3,r4]

times=[]

fig=plt.figure('Event-Histogram')


for r in runs:
    start_dt=r['start_dt']
    dt_8am = dt.datetime(start_dt.year,start_dt.month,start_dt.day,hour=8,minute=0)
    extra_secs=delta_dt_sec(dt_8am,start_dt)
    print(f'Adding {extra_secs} for starting at 8:00am, dt for run is {start_dt}.')
    times.extend(list((t + extra_secs)/60/60 for t in r['events']))
    
plt.hist(times,bins=50)
    
plt.ylabel('Events')
plt.xlabel('Time')
plt.xticks(ticks=[0,2,4,6,8,10],labels=['8:00','10:00','12:00','14:00','16:00','18:00'])
plt.title(f'Events vs. Time of Day ({len(times)} total)')

plt.show()

fig=plt.figure('Event-Histogram-Per-Day')
for r,i in zip(runs,range(1,len(r)+1)):
    plt.subplot(4,1,i)
    start_dt=r['start_dt']
    dt_8am = dt.datetime(start_dt.year,start_dt.month,start_dt.day,hour=8,minute=0)
    extra_secs=delta_dt_sec(dt_8am,start_dt)
    print(f'Adding {extra_secs} for starting at 8:00am, dt for run is {start_dt}.')
    times=list((t + extra_secs)/60/60 for t in r['events'])
    plt.hist(times,bins=50)
    plt.ylabel(f'Events\ntotal={len(times)}')
    plt.xlim(0,10)
    plt.xticks(ticks=[0,2,4,6,8,10],labels=['','','','','',''])
    
plt.xlabel('Time',fontsize=24)
plt.xticks(ticks=[0,2,4,6,8,10],labels=['8:00','10:00','12:00','14:00','16:00','18:00'])
#plt.title(f'Events vs. Time of Day ({len(times)} total)')

plt.show()

fig=plt.figure('Dt-frame-Per-Day')
for r,i in zip(runs,range(1,len(r)+1)):
    plt.subplot(4,1,i)
    #plt.hist(list(map(lambda x : 1/(x+0.001), r['ev_dt'])),bins=50)#bins=np.linspace(0,0.2,50))
    plt.hist(list(map(lambda x : 1/(x+0.0001), r['ev_dt'])),bins=np.linspace(0,100,40))
    
#plt.xlabel('Time',fontsize=24)
#plt.title(f'Events vs. Time of Day ({len(times)} total)')

plt.show()
