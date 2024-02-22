import random
import tkinter as tk
import cv2
import numpy as np
from ultralytics import YOLO
import tkinter as tk
from tkinter import BOTTOM, PhotoImage, filedialog

def openvid(fp):
# opening the file in read mode
    my_file = open("utils/coco.txt", "r")
    # reading the file
    data = my_file.read()
    # replacing end splitting the text | when newline ('\n') is seen.
    class_list = data.split("\n")
    my_file.close()

    # print(class_list)

    # Generate random colors for class list
    detection_colors = []
    for i in range(len(class_list)):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        detection_colors.append((b, g, r))

    # load a pretrained YOLOv8n model
    model = YOLO("weights/yolov8n.pt", "v8")

    # Vals to resize video frames | small frame optimise the run
    frame_wid = 640
    frame_hyt = 480

    # cap = cv2.VideoCapture(1)

    cap = cv2.VideoCapture(fp)
    

    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    while True:


        # Capture frame-by-frame
        ret, frame = cap.read()
        
        # if frame is read correctly ret is True

        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        #  resize the frame | small frame optimise the run
        frame = cv2.resize(frame, (frame_wid, frame_hyt))

        # Predict on image
        detect_params = model.predict(source=[frame], conf=0.45, save=False)

        # Convert tensor array to numpy
        DP = detect_params[0].numpy()
    # print(DP)

        if len(DP) != 0:
            for i in range(len(detect_params[0])):
                print(i)

                boxes = detect_params[0].boxes
                box = boxes[i]  # returns one box
                clsID = box.cls.numpy()[0]
                conf = box.conf.numpy()[0]
                bb = box.xyxy.numpy()[0]

                cv2.rectangle(
                    frame,
                    (int(bb[0]), int(bb[1])),
                    (int(bb[2]), int(bb[3])),
                    detection_colors[int(clsID)],
                    3,
                )

                # Display class name and confidence
                font = cv2.FONT_HERSHEY_COMPLEX
                cv2.putText(
                    frame,
                    class_list[int(clsID)] + " " + str(round(conf, 3)) + "%",
                    (int(bb[0]), int(bb[1]) - 10),
                    font,
                    1,
                    (255, 255, 255),
                    2,
                )

        # Display the resulting frame
        cv2.imshow("ObjectDetection", frame)

        # Terminate run when "Q" pressed
        if cv2.waitKey(1) == ord("q"):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()



import tkinter as tk

from tkinter import *
from PIL import Image, ImageTk




def openfile():
    file_path=filedialog.askopenfilename()
    openvid(file_path)





'''   
root = tk.Tk()
root.geometry('500x500')

# create a button that calls get_file_path() when clicked
but1=tk.Button(root,padx=5,pady=5,width=39,bg='white',fg='black',command=openfile,text='Image',font=('helvetica 15 bold'))
#but1.place(x=5,y=104)

but2=tk.Button(root,padx=5,pady=5,width=39,bg='white',fg='black',command=openfile,text='Video',font=('helvetica 15 bold'))
#but2.place(x=5,y=176)

but3=tk.Button(root,padx=5,pady=5,width=39,bg='white',fg='black',command=openfile,text='Webcam',font=('helvetica 15 bold'))
#but3.place(x=5,y=250)




but1.place(x=250, y=50)
but2.place(x=250, y=100)
but3.place(x=250, y=100)
#label.pack(side=TOP)
#filename = "inference/images/background.png"
#canvas = tk.Canvas(root, width=250, height=250)
#canvas.pack()
#tk_img = ImageTk.PhotoImage(file = filename)
#canvas.create_image(125, 125, image=tk_img)

#butwin1 = canvas.create_window(10, 10, anchor='nw', window=but1) 
#butwin2 = canvas.create_window(10, 10, anchor='nw', window=but2)  
#butwin3 = canvas.create_window(10, 10, anchor='nw', window=but3)   
#image = Image.open("inference/images/background.png")
#image = image.resize((500, 500), Image.ANTIALIAS)
#photo = ImageTk.PhotoImage(image)
#label = Label(root, image=photo)
#label.pack()
#background_label = Label(root,image=filename)
#background_label.pack(side=BOTTOM)
#background_label.configure(width=1000,height=500)
#root.mainloop()
# ask the user to select a file

'''

root=Tk()
root.geometry('500x500')
frame = Frame(root, relief=RIDGE, borderwidth=2)
frame.pack(fill=BOTH,expand=1)
root.title('OBJECT DETECTION')

label = Label(frame, text="OBJECT DETECTION",font=('helvetica 30 bold'))
label.pack(side=TOP)
filename = PhotoImage(file="inference/images/background.png")
background_label = Label(frame,image=filename)
background_label.pack(side=TOP)

but2=Button(frame,padx=5,pady=5,width=39,bg='white',fg='black',relief=GROOVE,command=openfile,font=('helvetica 15 bold'),text='video')
but2.place(x=5,y=176)



root.mainloop()