from datetime import datetime
import streamlit as st
from pyfirmata import Arduino, SERVO
from time import sleep
from streamlit_option_menu import option_menu
import cv2
from PIL import Image
import numpy as np
import mediapipe as mp
import time as time
import urllib.request
import datetime


mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
# Replace the URL with the IP camera's stream URL
url = 'http://192.168.50.62/cam-lo.jpg'
cap =cv2.VideoCapture(url)
st.title("Camera streaming security")
frame_placeholder=st.empty()
col1, col2 ,col3 = st.columns(3 )
with col1:
 stop_button =st.button("Stop")
with col2:
 capture_button =st.button("Capture")
# Create a VideoCapture object
cap = cv2.VideoCapture(url)
img_counter1 = 0

# Setup the board
board = Arduino('COM3')
# Attach servos to pin 9 and 10
pin1 = board.get_pin('d:9:s')
pin2 = board.get_pin('d:8:s')
def move_servo(pin, angle):
    # Write the angle to the servo
   pin.write(angle)
   sleep(0.015)
st.title('Servo Control')
try:
    # Create sliders for controlling the servos
    angle1 = st.slider('Servo 1 Angle', 0, 180, 90)
    angle2 = st.slider('Servo 2 Angle', 0, 180, 90)

    # Move the servos to the selected angles
    move_servo(pin1, angle1)
    move_servo(pin2, angle2)
finally:
    # Close the board connection when done
    board.exit()

def brighten_image(image, amount):
    img_bright = cv2.convertScaleAbs(image, beta=amount)
    return img_bright


def blur_image(image, amount):
    blur_img = cv2.GaussianBlur(image, (11, 11), amount)
    return blur_img

def bw_filter(img ):
    img_gray = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
    return img_gray

def outline(img, k = 9):
    
    k = max(k,9)
    kernel = np.array([[-1, -1, -1],
                       [-1,  k, -1],
                       [-1, -1, -1]])
    
    img_outline = cv2.filter2D(img, ddepth = -1, kernel = kernel)

    return img_outline

st.title("Web security")
st.subheader("This app allows you to play with Image filters!")
with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:
    while cap.isOpened() and not stop_button:
    # Read a frame from the video stream
     success , frame = cap.read()
     start =time.time()
     img_resp =urllib.request.urlopen(url)
     imgnp=np.array(bytearray(img_resp.read()),dtype=np.uint8)
     frame1 = cv2.imdecode(imgnp,-1)
     frame =cv2 .cvtColor(frame1 ,cv2.COLOR_BGR2RGB)

     detection =False
     dectection_stopped_time =None
     time_started =False
     Second_time_to_record =5
     frame_size =(int(cap.get(3)),int(cap.get(4)))
     fourcc =cv2.VideoWriter_fourcc(* "mp4v")
     out=cv2.VideoWriter("video.mp4" ,fourcc ,20 ,frame_size)
     out.write(frame)
     result = face_detection.process(frame)
     if result.detections:
         for id ,detection in enumerate(result.detections):
             mp_drawing.draw_detection(frame,detection)
         if detection :
             time_started =False
         else:
             detection =True
             out=cv2.VideoWriter(f"{curren_time}.mp4" ,fourcc ,20 ,frame_size)
             curren_time=datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
             print("Recording")
     elif detection :
        if time_started :
            if time.time() - dectection_stopped_time >= Second_time_to_record:
                detection =False
                time_started =False
                out.release()
                print('Stop recording')
        else :
            time_started =True
            dectection_stopped_time =time.time()
     if detection:
         out.write(frame)
        
     frame_placeholder.image(frame,width=600,channels="RGB")
     end =time.time()
     totaltime =end - start
     fps =1 / totaltime
     #print("FPS: ",fps)
     cv2.putText(frame,f'FPS:{int(fps)}',(20,70),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,255),1)

     if cv2.waitKey(1)& 0xFF==ord('q') or stop_button:
        break
     if capture_button:
         img_name = "selfewebcam_frame_{}.png".format(img_counter1)
         cv2.imwrite(img_name,frame)
         print("{} written ! ".format(img_name))
         img_counter1 += 1
         if img_counter1 >25:break

def main_loop():

    st.title("Processing Image")
    st.subheader("Place for photo identification")
    blur_rate = st.sidebar.slider("Blurring", min_value=0.5, max_value=3.5)
    brightness_amount = st.sidebar.slider("Brightness", min_value=-50, max_value=50, value=0)  
   
    gray_filter =st.sidebar.checkbox('Gray filter')
    outline_filter =st.sidebar.checkbox('Outline filter')
    col1, col2 = st.columns( [0.8, 0.2])

    image_file = st.file_uploader("Upload Your Image", type=['jpg', 'png', 'jpeg'])
    if  image_file is not None:
        original_image = Image.open(image_file)
        original_image = np.array(original_image)
        with col1:
            st.markdown('<p style="text-align: center;">Before</p>',unsafe_allow_html=True)
            st.image(original_image,width=300)
        with col2:
                st.markdown('<p style="text-align: center;">After</p>',unsafe_allow_html=True)
                
                processed_image = blur_image(original_image, blur_rate)
                processed_image = brighten_image(processed_image, brightness_amount)
                if gray_filter:
                    processed_image = bw_filter(processed_image)
                if outline_filter:
                    processed_image = outline(processed_image)
                st.image(processed_image, width=300)
if __name__ == '__main__':
  main_loop()
cap.release()
cv2.destroyAllWindows()

   
    




