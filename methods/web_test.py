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

# Time difference for grouping images
DELTA_T_SEC = 5

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


# Get Image V2
def getImage(d, f_dir_d, b, f_dir_b):
    global final_match
    d_name = ""
    b_name = ""
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
    name_d = year + "-" + month + "-" + day + "_" + hour + "-" + minus + "-" + sec + "_" + ms + "*"

    p_d = path.Path(f_dir_d)

    for f in p_d.glob(name_d):
        d_name = str(f)

    year_b = str(b.year)
    if b.month < 10:
        month_b = "0" + str(b.month)
    else:
        month_b = str(b.month)
    if b.day < 10:
        day_b = "0" + str(b.day)
    else:
        day_b = str(b.day)
    if b.hour < 10:
        hour_b = "0" + str(b.hour)
    else:
        hour_b = str(b.hour)
    if b.minute < 10:
        minus_b = "0" + str(b.minute)
    else:
        minus_b = str(b.minute)
    if b.second < 10:
        sec_b = "0" + str(b.second)
    else:
        sec_b = str(b.second)
    if b.microsecond < 10:
        ms_b = "0" + str(b.microsecond)
    else:
        ms_b = str(b.microsecond)
    name_b = year_b + "-" + month_b + "-" + day_b + "_" + hour_b + "-" + minus_b + "-" + sec_b + "_" + ms_b + "*"

    p_b = path.Path(f_dir_b)

    for f in p_b.glob(name_b):
        b_name = str(f)
    if d_name != "" and b_name != "":
        final_match[d_name] = b_name


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
    global match
    for i in range(len(es_list_a)):
        event_a_start_time = str(es_list_a[i][0].month) + str(es_list_a[i][0].day) + str(es_list_a[i][0].hour) + str(es_list_a[i][0].minute)
        event_a_end = es_list_a[i][-1].minute * 60 + es_list_a[i][-1].second
        for j in range(len(es_list_b)):
            event_b_start_time = str(es_list_b[j][0].month) + str(es_list_b[j][0].day) + str(es_list_b[j][0].hour) + str(es_list_b[j][0].minute)
            if event_a_start_time == event_b_start_time:
                event_b_end = es_list_b[j][-1].minute * 60 + es_list_b[j][-1].second
                if abs(event_b_end - event_a_end) < 3:
                    match[i] = j


dir_1 = 'run_top-3___2021-08-28_12-00-37'
dir_2 = 'run_side-3___2021-08-28_12-00-48'

r3 = get_events(dir_1)
r3_side = get_events(dir_2)
e_names = []

determineE = []

es_list = r3.get('events_list')
nums = r3.get('event_cnt')

es_list_2 = r3_side.get('events_list')
nums_2 = r3_side.get('event_cnt')

match = {}

event_match(es_list, es_list_2)

final_match = {}

for key in match:
    value = match[key]
    mid_1 = int(len(es_list[key]) / 2)
    mid_2 = int(len(es_list_2[value]) / 2)
    getImage(es_list[key][mid_1], dir_1, es_list_2[value][mid_2], dir_2)


# build an object list
obj_list = []
idx = 0
for key in final_match:
    time_stamp = str(final_match[key].split('/')[1].split('_')[0]) + '_' + str(final_match[key].split('/')[1].split('_')[1])  # windows uses '\\', mac uses '/'
    obj_list.append(bee.bee_event(idx, time_stamp, -1))
    obj_list[idx].add_top_image(key)
    obj_list[idx].add_side_image(final_match[key])
    idx += 1

# for bee_project
res_list = []
i = 0

for obj in obj_list:
    res_list.append("<div class='event'>")
    res_list.append("<p class='event_num'>Event " + str(obj.eventID + 1) + "</p>")

    res_list.append("<div class='area_block'>")
    res_list.append("<p class='event_des'>Date: " + str(obj.get_top_dir().split('/')[1].split('_')[0]) + "</p>")
    res_list.append("<p class='event_des'>Time: " + str(obj.get_top_dir().split('/')[1].split('_')[1]) + "</p>")
    res_list.append("</div>")

    res_list.append("<div class='area_block'>")
    res_list.append("<p class='view_dir'>Side View</p>")
    res_list.append("<img src=" + str(obj.get_side_dir()) + " class='img' height='200' width='300'>")   # sid image
    res_list.append("</div>")

    res_list.append("<div class='area_block'>")
    res_list.append("<p class='view_dir'>Top View</p>")
    res_list.append("<img src=" + str(obj.get_top_dir()) + " class='img' height='200' width='300'>")    # top image
    res_list.append("</div>")

    res_list.append("</div>")
    i += 1

    # top_path = os.path.join("./run_top-3___2021-08-28_12-00-37", str((top)))
    # side_path = os.path.join("./run_side-3___2021-08-28_12-00-48", str(match[top]))
    # print(key)
    # if i % 2 == 0:
    #     res_list.append("<p>" + str(key) + "</p>")
    #     res_list.append("<img src=" + str(key) + "><br><br><br><br><br>" )    # top image

    # else:
    #     res_list.append("<p>" + str(final_match[key]) + "</p>")
    #     res_list.append("<img src=" + str(final_match[key]) + ">")   # sid image
    # i+=1


img_str = ""
for tags in res_list:
    img_str += tags

# html generated
GEN_HTML = "test_result.html"
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
webbrowser.open(GEN_HTML, new=1)
'''
webbrowser.open(url, new=0, autoraise=True)
Display url using the default browser. If new is 0, the url is opened in the same browser window if possible. If new is 1, a new browser window is opened if possible. If new is 2, a new browser page (“tab”) is opened if possible. If autoraise is True, the window is raised if possible (note that under many window managers this will occur regardless of the setting of this variable).
'''

