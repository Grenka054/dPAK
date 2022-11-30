import numpy as np
import cv2
import time
from collections import deque


path_video = "data/source3.mp4"
rg_transparency = 0.25  # transparency rad/green map

q = deque()
cap = cv2.VideoCapture(path_video)
FPS = 25
delay = 1000/FPS

# Подготовка начальных кадров, т.к. текущий кадр сравнивается с кадром, который был FPS/25 кадров назад
while len(q) <= FPS/25:
    _, prev = cap.read()
    prev = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)
    q.append(prev)

# Проверять ли движение
trigger_on = True
timer = 0
while True:
    time_st = time.time()
    ret, frame = cap.read()
    if not ret:
        cap = cv2.VideoCapture(path_video)
        continue

    # предыдущий кадр
    prev = q.popleft()

    # сделать текущий кадр серым и сразу положить в очередь
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    q.append(frame_gray)

    # разница кадров -> ч/б
    diff_gray = cv2.absdiff(frame_gray, prev)
    _, thresh = cv2.threshold(diff_gray, 35, 255, cv2.THRESH_BINARY)
    thresh_dilated = cv2.dilate(thresh, np.ones((3,3)), iterations=3)
    rg_layout = cv2.cvtColor(thresh_dilated, cv2.COLOR_GRAY2BGR)

    # смена цветов
    rg_layout[thresh_dilated.astype(bool)] = [0,0,255]  # white to red
    rg_layout[np.logical_not(thresh_dilated.astype(bool))] = [0,255,0]  # black to green

    # наложение маски на исходное изображение
    if trigger_on:
        out_frame = cv2.addWeighted(frame, 1 - rg_transparency, rg_layout, rg_transparency, 0)
        cv2.putText(out_frame, "Red", (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    else:
        out_frame = frame.copy()
        cv2.putText(out_frame, "Green", (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # показать окна
    cv2.imshow('Camera', frame)
    cv2.imshow('Detector', out_frame)
    cv2.imshow('RG Map', rg_layout)

    # расчет задержки для плавного FPS
    time_end = time.time()
    timePerFrame = ((time_end - time_st) * 1000 + 6)
    wait_time = int(delay - timePerFrame)
    if wait_time <= 0:
        wait_time = 1
    key = cv2.waitKey(wait_time) & 0xff
    if key == 27:
        break

    # изменение состояния триггера
    timer += 1
    if(timer >= FPS * 2):
        trigger_on = not trigger_on
        timer = 0
