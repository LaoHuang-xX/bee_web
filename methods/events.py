'''
Nils Napp, Xu Hai Mar 2021
Script to group and count the entry/exit events form beetunnel filenames
'''

import cv2
import pathlib as path
import datetime as dt
import numpy as np
import time
from matplotlib import pyplot as plt

# Time difference for grouping images
DELTA_T_SEC = 5

#DIR_REL = 'Q1/run-2105__2021-03-08_08-59-53_top-1'
#DIR_REL = 'N2/run_top-3___2021-03-08_09-00-22'

FMT_STR = '%Y-%m-%d_%H-%M-%S_%f'
MIN_PIC = 4

start_time = time.time()
def tstr(fname):
    parts = fname.split('_')
    return parts[0] + '_' + parts[1] + '_' + parts[2]


def delta_dt_sec(dt1, dt2):
    delta = dt2 - dt1
    return delta.days * 24 * 60 * 60 + delta.seconds + delta.microseconds / 1000000


def get_events(DIR_REL):
    p = path.Path(DIR_REL)
    dtimes = [dt.datetime.strptime(tstr(f.name), FMT_STR) for f in p.glob('*.jpg')]

    dtimes.sort()
    if len(dtimes) <= 2:
        #print(f'Warning: Not enough images in "{DIR_REL}".')
        return None

    events = [0]
    event_delta = []
    dt0 = dtimes[0]
    dt_last = dt0
    pic_per_ev = []
    pic_cnt = 0

    dt_list = []

    events_list = []
    event_elements = []
    for d in dtimes:
        pic_cnt += 1
        ev_del = delta_dt_sec(dt_last, d)
        if ev_del > DELTA_T_SEC:
            if pic_cnt < MIN_PIC:
                #print(f'Removing Event at {d}, less than {MIN_PIC} pictures.')
                pic_cnt = 1
            else:
                pic_per_ev.append(pic_cnt)
                pic_cnt = 1
                events.append(delta_dt_sec(dt0, d))
                event_delta.append(ev_del)
                events_list.append(event_elements)
                event_elements = []
        else:
            #print(ev_del)
            event_elements.append(d)
            if ev_del < .2:
                dt_list.append(ev_del)

        dt_last = d

    #print(f'There were {len(events)} entry or exit events with a min delta={DELTA_T_SEC} seconds.')
    #print(f'Dt mean = {1 / np.mean(dt_list)}.')
    ret = {}
    ret['events'] = events
    ret['event_delta'] = event_delta
    ret['event_cnt'] = pic_per_ev
    ret['start_dt'] = dtimes[0]
    ret['ev_dt'] = dt_list
    ret['events_list'] = events_list
    return ret


#r1 = get_events('N2/run_top-3___2021-03-08_09-00-22')
#r2 = get_events('Q1/run-2105__2021-03-08_08-59-53_top-1')
#r3 = get_events('run_top-3___2021-03-12_08-50-38')
#r4 = get_events('run_top-4___2021-03-12_08-50-27')

#r4 = get_events('run_side-3___2021-08-28_12-00-48')
#runs = [r1, r2, r3, r4]


def getImage(d, f_dir, names):
    year = str(d.year)
    if d.month < 10:
        month = "0" + str(d.month)
    else:
        month = str(d.month)
    if d.day < 10:
        day = "0" + str(d.day)
    else:
        day = str(d.day)
    if d.hour < 10:
        hour = "0" + str(d.hour)
    else:
        hour = str(d.hour)
    if d.minute < 10:
        minus = "0" + str(d.minute)
    else:
        minus = str(d.minute)
    if d.second < 10:
        sec = "0" + str(d.second)
    else:
        sec = str(d.second)
    if d.microsecond < 10:
        ms = "0" + str(d.microsecond)
    else:
        ms = str(d.microsecond)
    name = year + "-" + month + "-" + day + "_" + hour + "-" + minus + "-" + sec + "_" + ms + "*"

    p = path.Path(f_dir)

    for f in p.glob(name):
        names.append(str(f))


def bg_sub(names, num):
    first_img = names[0]
    fir_img = cv2.imread(first_img, 2)

    ret, fir_img = cv2.threshold(fir_img, 127, 255, cv2.THRESH_BINARY)

    img = names[num]
    img_g = cv2.imread(img, 2)
    ret, img = cv2.threshold(img_g, 127, 255, cv2.THRESH_BINARY)

    labels = np.zeros(img.shape)
    label = 1.0
    record = {}

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if fir_img[i][j] == img[i][j]:
                img[i][j] = 255
            if img[i][j] == 0:
                if i > 0 and labels[i - 1][j] != 0:
                    labels[i][j] = labels[i - 1][j]
                    record[str(labels[i][j])] += 1
                elif j > 0 and labels[i][j - 1] != 0:
                    labels[i][j] = labels[i][j - 1]
                    tmp = record[str(labels[i][j])]
                    record[str(labels[i][j])] = tmp + 1
                else:
                    labels[i][j] = label
                    record[str(label)] = 1
                    label += 1


def determinEvent(names, num, determineE):
    first_image_name = names[0]
    # read image as greyscale
    fir_img = cv2.imread(first_image_name, 2)

    # Otsu's thresholding after Gaussian filtering
    fir_blur = cv2.GaussianBlur(fir_img, (5, 5), 0)
    fir_ret, fir_th = cv2.threshold(fir_blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    fir_x_avg = 0
    fir_y_avg = 0
    fir_total = 0

    for i in range(fir_th.shape[0]):
        for j in range(fir_th.shape[1]):
            if fir_th[i][j] == 0:
                fir_x_avg += j
                fir_y_avg += i
                fir_total += 1

    fir_x_avg = int(fir_x_avg / fir_total)
    #fir_y_avg = int(fir_y_avg / fir_total)

    # Second image
    second_image_name = names[len(names) - 1]
    # read image as greyscale
    se_img = cv2.imread(second_image_name, 2)

    # Otsu's thresholding after Gaussian filtering
    se_blur = cv2.GaussianBlur(se_img, (5, 5), 0)
    se_ret, se_th = cv2.threshold(se_blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    se_x_avg = 0
    se_y_avg = 0
    se_total = 0

    # Compute Center of mass
    for i in range(se_th.shape[0]):
        for j in range(se_th.shape[1]):
            if se_th[i][j] == 0:
                se_x_avg += j
                se_y_avg += i
                se_total += 1

    se_x_avg = int(se_x_avg / se_total)
    #se_y_avg = int(se_y_avg / se_total)

    if se_x_avg - fir_x_avg > 0:
        determineE.append("Right")
    elif se_x_avg - fir_x_avg < 0:
        determineE.append("Left")
    else:
        determineE.append("Error")


# Match same event for top and side views
def event_match(es_list_a, es_list_b):
    global match
    for i in range(len(es_list_a)):
        event_a_start_time = str(es_list_a[i][0].month) + str(es_list_a[i][0].day) + str(es_list_a[i][0].hour) + str(es_list_a[i][0].minute)
        # event_a_range = es_list_a[i][-1].minute * 60 + es_list_a[i][-1].second - es_list_a[i][0].minute * 60 - es_list_a[i][0].second
        event_a_end = es_list_a[i][-1].minute * 60 + es_list_a[i][-1].second
        for j in range(len(es_list_b)):
            event_b_start_time = str(es_list_b[j][0].month) + str(es_list_b[j][0].day) + str(es_list_b[j][0].hour) + str(es_list_b[j][0].minute)
            if event_a_start_time == event_b_start_time:
                # event_b_range = es_list_b[j][-1].minute * 60 + es_list_b[j][-1].second - es_list_b[j][0].minute * 60 - es_list_b[j][0].second
                event_b_end = es_list_b[j][-1].minute * 60 + es_list_b[j][-1].second
                # if abs(event_a_range - event_b_range) < 3:
                if abs(event_b_end - event_a_end) < 3:
                    match[i] = j


dir = 'run_top-3___2021-08-28_12-00-37'
r3 = get_events(dir)
e_names = []

determineE = []

es_list = r3.get('events_list')
nums = r3.get('event_cnt')

for es in es_list:
    names = []
    for e in es:
        getImage(e, dir, names)
    e_names.append(names)

for i in range(len(nums)):
    for j in range(len(e_names[i])):
        bg_sub(e_names[i], j)

for i in range(len(nums)):
    determinEvent(e_names[i], nums[i], determineE)

print(determineE)
print(es_list)
print(time.time() - start_time)