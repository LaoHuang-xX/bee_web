# coding:utf-8
'''
Nils Napp, Yitong Sun, Xu Hai Nov 2021
Script to group and count the entry/exit events form beetunnel filenames
'''

import cv2
import pathlib as path
import datetime as dt
import numpy as np
import time
import webbrowser
import sys
import os
from matplotlib import pyplot as plt
import bee_event as bee  # be sure to include bee_event.py in the same dir
from sys import platform
import re
import pickle

# Time difference for grouping images
DELTA_T_SEC = 2

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

    ret = {}
    ret['events'] = events
    ret['event_delta'] = event_delta
    ret['event_cnt'] = pic_per_ev
    ret['start_dt'] = dtimes[0]
    ret['ev_dt'] = dt_list
    ret['events_list'] = events_list
    return ret


# Get Image V3
def getImage(d, f_dir_d):
    d_name = ""

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
    if d.microsecond / 10 < 1:
        ms = "00000" + str(d.microsecond)
    elif d.microsecond / 100 < 1:
        ms = "0000" + str(d.microsecond)
    elif d.microsecond / 1000 < 1:
        ms = "000" + str(d.microsecond)
    elif d.microsecond / 10000 < 1:
        ms = "00" + str(d.microsecond)
    elif d.microsecond / 100000 < 1:
        ms = "0" + str(d.microsecond)
    else:
        ms = str(d.microsecond)
    name_d = year + "-" + month + "-" + day + "_" + hour + "-" + minus + "-" + sec + "_" + ms + "*"

    p_d = path.Path(f_dir_d)

    for f in p_d.glob(name_d):
        d_name = str(f)

    if d_name != "":
        return d_name
    else:
        print('Unexpected error: previous file can not be found')
        print('File name: ' + name_d)
        quit()


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

    # Second image
    second_image_name = names[len(names) - 1]
    # read image as greyscale
    se_img = cv2.imread(second_image_name, 2)

    # Otsu's thresholding after Gaussian filtering
    se_blur = cv2.GaussianBlur(se_img, (5, 5), 0)
    se_ret, se_th = cv2.threshold(se_blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    se_x_avg = 0
    se_total = 0

    # Compute Center of mass
    for i in range(se_th.shape[0]):
        for j in range(se_th.shape[1]):
            if se_th[i][j] == 0:
                se_x_avg += j
                se_total += 1

    se_x_avg = int(se_x_avg / se_total)

    if se_x_avg - fir_x_avg > 0:
        determineE.append("Right")
    elif se_x_avg - fir_x_avg < 0:
        determineE.append("Left")
    else:
        determineE.append("Error")


# Match same event for top and side views
def event_match(es_list_a, es_list_b):
    global in_date_parts, in_time_parts
    event_a = []
    event_b = []
    event_start_time = str(int(in_date_parts[1])) + str(int(in_date_parts[2])) + str(int(in_time_parts[0]))
    for i in range(len(es_list_a)):
        event_a_start_time = str(es_list_a[i][0].month) + str(es_list_a[i][0].day) + str(es_list_a[i][0].hour)
        if event_a_start_time == event_start_time:
            # List all events within the same hour of input time
            # But earlier than input time
            if int(es_list_a[i][0].minute) <= int(in_time_parts[1]):
                event_a.append(i)
    for i in range(len(es_list_b)):
        event_b_start_time = str(es_list_b[i][0].month) + str(es_list_b[i][0].day) + str(es_list_b[i][0].hour)
        if event_b_start_time == event_start_time:
            # List all events within the same hour of input time
            # But earlier than input time
            if int(es_list_b[i][0].minute) <= int(in_time_parts[1]):
                event_b.append(i)

    if event_a == [] or event_b == []:
        print('No matched event based on your input date and time.')
        quit()
    elif len(event_a) != len(event_b):
        print('Some images of top/side view misses, only take the first satisfied event.')
        event_a = [event_a[0]]
        event_b = [event_b[0]]
    return event_a, event_b


pattern_date = re.compile(r'(\d{4}-\d{2}-\d{2})')
pattern_time = re.compile(r'(\d{2}-\d{2}-\d{2})')

# Let the user input date and time
# And make sure the format is correct
count = 0
while 1:
    in_date = input("Please input a date you want to query (follow the format 'yyyy-mm-dd'): ")
    if re.match(pattern_date, in_date):
        break
    count += 1
    if count == 5:
        print('Too many errors, program stops.')
        quit()

count = 0

while 1:
    in_time = input("Please input the time you want to query (follow the format 'hh-mm-ss'): ")
    if re.match(pattern_time, in_time):
        break
    count += 1
    if count == 5:
        print('Too many errors, program stops.')
        quit()


in_date_parts = in_date.split('-')
in_time_parts = in_time.split('-')
files = os.listdir('data/')

latest_time_top = 0
latest_time_side = 0

for f in files:
    parts = f.split('_')
    if len(parts) == 6:
        tmp_month = parts[4].split('-')[1]
        tmp_day = parts[4].split('-')[2]
        tmp_hour = int(parts[5].split('-')[0])
        tmp_minute = int(parts[5].split('-')[1])
        tmp_second = int(parts[5].split('-')[2])

    if tmp_month == in_date_parts[1]:
        # The range cover 5 days earlier than the required date
        if int(tmp_day) <= int(in_date_parts[2]) and int(tmp_day) >= int(in_date_parts[2]) - 5:
            if tmp_hour * 60 * 60 + tmp_minute * 60 + tmp_second <= int(in_time_parts[0]) * 60 * 60 + int(in_time_parts[1]) * 60 + int(in_time_parts[2]):
                if parts[1].split('-')[0] == 'side':
                    if latest_time_side < tmp_hour * 60 * 60 + tmp_minute * 60 + tmp_second:
                        latest_time_side = tmp_hour * 60 * 60 + tmp_minute * 60 + tmp_second
                        aim_file_side = f
                if parts[1].split('-')[0] == 'top':
                    if latest_time_top < tmp_hour * 60 * 60 + tmp_minute * 60 + tmp_second:
                        latest_time_top = tmp_hour * 60 * 60 + tmp_minute * 60 + tmp_second
                        aim_file_top = f


r3 = get_events(aim_file_top)
r3_side = get_events(aim_file_side)

es_list = r3.get('events_list')
nums = r3.get('event_cnt')

es_list_2 = r3_side.get('events_list')
nums_2 = r3_side.get('event_cnt')

top_indexes, side_indexes = event_match(es_list, es_list_2)

count = 0
names = []
pickle_file = {}

for n in range(len(top_indexes)):
    if n < len(side_indexes):
        top_index = top_indexes[n]
        side_index = side_indexes[n]

        # All images of an event
        # The first image is the middle image of the event
        top_events = []
        side_events = []

        # The middle image of an event
        top_mid = es_list[top_index][int(len(es_list[top_index]) / 2)]
        side_mid = es_list_2[side_index][int(len(es_list_2[side_index]) / 2)]

        # Record the middle image name
        top_events.append(getImage(top_mid, aim_file_top))
        side_events.append(getImage(side_mid, aim_file_side))

        # Record all images of an event
        for e in es_list[top_index]:
            top_events.append(getImage(e, aim_file_top))

        for e in es_list_2[side_index]:
            side_events.append(getImage(e, aim_file_side))

        res_list = []

        if platform == "win32":
            names.append(str(top_events[0].split('\\')[1].split('_')[0]) + '-' +
                       str(top_events[0].split('\\')[1].split('_')[1]) + '.html')
        else:
            names.append(str(top_events[0].split('/')[1].split('_')[0]) + '-' +
                       str(top_events[0].split('/')[1].split('_')[1]) + '.html')

        pickle_file[names[-1][:-5]] = names[-1]

        # Previous button
        if count > 0:
            res_list.append("<a href='file:test_result" + names[-2] )
            res_list.append(".html' class='previous'> &laquo Previous </a>")
        # Next button
        if count < len(side_indexes) - 1:
            res_list.append("<a href='file:test_result" + str(count + 2) )
            res_list.append(".html' class='next'>Next &raquo;</a>")

        # Record the title of each event
        res_list.append("<div class='event'>")
        res_list.append("<p class='event_num'>Event " + str(count + 1) + "</p>")

        res_list.append("<div class='area_block'>")
        # Deal with different OS
        # Windows
        if platform == "win32":
            res_list.append("<p class='event_des'>Date: " + str(top_events[0].split('\\')[1].split('_')[0]) + "</p>")
            res_list.append("<p class='event_des'>Time: " + str(top_events[0].split('\\')[1].split('_')[1]) + "</p>")
        # Linux / Mac
        else:
            res_list.append("<p class='event_des'>Date: " + str(top_events[0].split('/')[1].split('_')[0]) + "</p>")
            res_list.append("<p class='event_des'>Time: " + str(top_events[0].split('/')[1].split('_')[1]) + "</p>")
        res_list.append("</div>")

        res_list.append("<div class='area_block'>")
        res_list.append("<p class='view_dir'>Side View</p>")
        res_list.append("<img src=" + str(side_events[0]) + " class='img' height='200' width='300'>")   # sid image
        res_list.append("</div>")

        res_list.append("<div class='area_block'>")
        res_list.append("<p class='view_dir'>Top View</p>")
        res_list.append("<img src=" + str(top_events[0]) + " class='img' height='200' width='300'>")    # top image
        res_list.append("</div>")

        res_list.append("</div>")
        count += 1

        # Record all images of the side view
        res_list.append("<div class='event_view'>")
        res_list.append("<p class='event_num'>All Images of the Side View</p>")

        res_list.append("<div class='event_imgs'>")

        for i in range(1, len(side_events)):
            if i % 9 == 0:
                res_list.append("<div>")
            res_list.append("<div class='area_block'>")
            res_list.append("<img src=" + str(side_events[i]) + " class='img' height='50' width='80'>")
            res_list.append("</div>")
            if i % 9 == 0:
                res_list.append("</div>")

        res_list.append("</div>")

        res_list.append("</div>")

        # Record all images of the top view
        res_list.append("<div class='event_view'>")
        res_list.append("<p class='event_num'>All Images of the Top View</p>")

        res_list.append("<div class='event_imgs'>")

        for i in range(1, len(top_events)):
            if i % 9 == 0:
                res_list.append("<div>")
            res_list.append("<div class='area_block'>")
            res_list.append("<img src=" + str(top_events[i]) + " class='img' height='50' width='80'>")
            res_list.append("</div>")
            if i % 9 == 0:
                res_list.append("</div>")

        res_list.append("</div>")

        res_list.append("</div>")


        img_str = ""
        for tags in res_list:
            img_str += tags

        # html generated
        if platform == "win32":
            GEN_HTML = names[-1]
        else:
            GEN_HTML = names[-1]

        # open html
        f = open(GEN_HTML, 'w', encoding="utf-8")

        message = """
        <!DOCTYPE html>
        <html>
        <head>
            <link rel="stylesheet" type="text/css" href="task001.css">
            <meta charset="utf-8">
            <title>test</title>
            <style type="text/css">
            *{margin: 0; padding: 0;}
            .clearfix:after {
                  clear: both;
                  content: ".";
                  display: block;
                  height: 0;
                  visibility: hidden;
                }
                .event_imgs {
                    margin: auto;
                    height: 300px;
                }
                .area_block {
                    float: left;
                    margin: 20px;
                }
                .view_dir {
                    font-size: 18px;
                    font-weight: 600;
                    color: black;
                }
                .event_des {
                    font-size: 16px;
                    font-weight: 500;
                    color: black;
                    float: left;
                    margin: 0 20px 0;
                }
                .event {
                    margin-bottom: 50px;
                    height: 300px;
                }
                .event_view {
                    margin: 20px 0px 20px;
                    height: 350px;
                }
                .wrap {
                    padding: 20px;
                    border-radius: 25px;
                    width: 1200px;
                    text-align: center;
                    margin: 0 auto;
                    background: rgb(241, 239, 239);
                    box-shadow: 0 12px 16px 0 rgba(0,0,0,0.24), 0 17px 50px 0 rgba(0,0,0,0.19);
                }
                #header {
                    background-color:rgb(160, 39, 39);
                    color:white;
                    text-align:center;
                    padding:5px;
                    border: none;
                    box-shadow: 0 12px 16px 0 rgba(0,0,0,0.24), 0 17px 50px 0 rgba(0,0,0,0.19);
                    margin-bottom: 90px;
                }
                body {
                    background: rgb(207, 204, 204);
                    margin: 0;
                }
                .event_num {
                    font-size: 28px;
                    font-weight: 900;
                    color: black;
                    margin-top: 10px;
                    margin-bottom: 10px;
                }
                #footer {
                    background-color:rgb(160, 39, 39);
                    color:white;
                    clear:both;
                    text-align:center;
                    padding:5px;
                }
                a {
                text-decoration: none;
                display: inline-block;
                padding: 8px 16px;
                }
                a:hover {
                background-color: #ddd;
                color: black;
                }
                .previous {
                background-color: #f1f1f1;
                color: black;
                }
                .next {
                background-color: #04AA6D;
                color: white;
                }
            </style>
        </head>
        <body>
            <div id="header">
            <h1>Custom Bee Tracking System</h1>
            </div>
            <div class="wrap">
                %s
            </div>
        </body>
        </html>""" % (img_str)


        f.write(message)

        f.close()

        # run web broswer
        #webbrowser.open(GEN_HTML, new=1)
        '''
        webbrowser.open(url, new=0, autoraise=True)
        Display url using the default browser. If new is 0, the url is opened in the same browser window if possible. If new is 1, a new browser window is opened if possible. If new is 2, a new browser page (???tab???) is opened if possible. If autoraise is True, the window is raised if possible (note that under many window managers this will occur regardless of the setting of this variable).
        '''
webbrowser.open_new_tab('file:' + os.path.realpath(names[-1]))

names.append(in_date_parts[0] + '-' + in_date_parts[1] + '-' + in_date_parts[2] + '_'
             + in_time_parts[0] + '-' + in_time_parts[1])

file_name = names[-1]
outfile = open(file_name, 'wb')
pickle.dump(pickle_file, outfile)
outfile.close()

while 1:
    delete_or_not = input("Do you want to remove generated HTML files? (y/n): ")
    if delete_or_not.lower() == 'y' or delete_or_not.lower() == 'yes':
        for i in range(len(names)):
            os.remove(names[i])
        break
    elif delete_or_not.lower() == 'n' or delete_or_not.lower() == 'no':
        break
