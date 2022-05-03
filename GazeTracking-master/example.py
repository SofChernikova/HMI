"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""
from tkinter import *

import cv2
from gaze_tracking import GazeTracking

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)
window = Tk()
window.title('Частотный спектр сигнала с помощью преобразования Гильберта')
window.geometry("800x600")

lbl = Label(window, text="Поле для текста:")
lbl.place(x=150, y=0)

text = Text(width=25, height=5)
text.place(x=325, y=0)
text.pack()



while True:

    # We get a new frame from the webcam
    _, frame = webcam.read()

    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    frame = gaze.annotated_frame()
    move = ""
    your_text = ""

    if gaze.is_blinking():
        move = "Blinking"
        your_text = "none"

    elif gaze.is_right():
        move = "Looking right"
        your_text = "none"

    elif gaze.is_left():
        move = "Looking left"
        your_text = "none"

    elif gaze.is_center():
        move = "Looking center"
        if text.get(1.0, END) is not None:
            your_text = text.get(1.0, END)

    cv2.putText(frame, move, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)
    cv2.putText(frame, "Your text:  " + your_text, (90, 90), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

    cv2.imshow("Demo", frame)
    window.mainloop()

    if cv2.waitKey(1) & 0xff == ord('q'):
        break

webcam.release()
cv2.destroyAllWindows()

# btn_plot = Button(window, text="Начать", command=eyes_move, height=2)
# btn_plot.place(x=290, y=100)
