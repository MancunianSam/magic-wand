#!/usr/bin/python3
import argparse
import numpy as np
import cv2
from operator import itemgetter

ap = argparse.ArgumentParser()
ap.add_argument("-r", "--radius", type = int)
ap.add_argument("-d", "--diff", type = int)
ap.add_argument("-g", "--gamma", type = float)

args = vars(ap.parse_args())
radius = 31
diff = args["diff"]

cap = cv2.VideoCapture(0)

def adjust_gamma(image, gamma=1.0):
   invGamma = 1.0 / gamma
   table = np.array([((i / 255.0) ** invGamma) * 255
      for i in np.arange(0, 256)]).astype("uint8")

   return cv2.LUT(image, table)

def get_diff(arr):
    diff_x = max(arr, key=itemgetter(1))[0] - min(arr, key=itemgetter(1))[0]
    diff_y = max(arr, key=itemgetter(1))[1] - min(arr, key=itemgetter(1))[1]
    return (diff_x, diff_y)

def is_moving(movingArr):
    (diff_x, diff_y) = get_diff(movingArr)
    if abs(diff_x) > diff or abs(diff_y) > diff:
        return True
    return False

def get_direction(trace_arr):
    (diff_x, diff_y) = get_diff(trace_arr)
    direction = ""
    print(diff_x)
    if diff_x < -diff:
        direction = "left"
    elif diff_x > diff:
        direction = "right"
    elif diff_y < -diff:
        direction = "up"
    elif diff_y > diff:
        direction = "down"
    return direction

def get_max_loc(gray):
    (minVal, maxVal, minLoc, max_loc) = cv2.minMaxLoc(gray)
    cv2.circle(gray, max_loc, 5, (255, 0, 0), 2)
    cv2.imshow("Naive", gray)
    gray = cv2.GaussianBlur(gray, (radius, radius), 0)
    (_,_,_, max_loc) = cv2.minMaxLoc(gray)
    return max_loc

def readFrames():
    movingArr = []
    trace_arr = []
    moving = False
    while(True):
        _, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = adjust_gamma(gray, args["gamma"])
        max_loc = get_max_loc(gray)
        trace_arr.append(max_loc)
        if is_moving(trace_arr):
            direction = get_direction(trace_arr)
            print(direction)
            trace_arr = []
            
        cv2.circle(gray, max_loc, radius, (255, 0, 0), 2)
        cv2.imshow("Robust", gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

readFrames()         
