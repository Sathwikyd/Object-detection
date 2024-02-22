import torch
import cv2

from ultralytics import YOLO

model = YOLO("yolov8l.pt")
model.predict(source=0,show=True,save=True,conf=0.5)