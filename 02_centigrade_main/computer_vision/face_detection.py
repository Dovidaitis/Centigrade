import cv2
import numpy as np
import sys
import datetime
import time



# time.sleep(3)
# arduino = SerialCom('115200')
# print(arduino.connection_established, arduino.serial_baudrate, arduino.com_port, sep='\n')
# print("running..")


class FaceDetection():

    cascPath_frontalface = r'computer_vision/haarcascade_frontalface_default.xml'
    cascPath_eye = r'computer_vision/haarcascade_eye' # for eyes

    faceCascade = cv2.CascadeClassifier(cascPath_frontalface)
    eyeCascade = cv2.CascadeClassifier(cascPath_eye)

    video_capture = cv2.VideoCapture(1)
    video_capture.set(3, 360)
    video_capture.set(4, 480)
    # video_capture.set(10, 100)

    DEBUG = False

    MIRROR = True
    DISPLAY = True
    DISPLAY_INFO = True
    MIN_SIZE = 100
    MIN_FACE_SIZE = 350

    FONT = cv2.FONT_HERSHEY_SIMPLEX
    

    @staticmethod
    def largest_face_index(faces):
        max_size = 0
        max_size_index = 0
        for index in range(len(faces)):
            size = faces[index][2]+faces[index][3]
            if size > max_size:
                max_size_index = index
        return max_size_index

    @staticmethod
    def rectangle_multiple_faces(faces, grey_img):
        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(grey_img, (x, y), (x+w, y+h), (0, 0, 255), 2)
    
    @staticmethod
    def time_stamp():
        # return datetime.now().strftime("%H:%M:%S-%d/%m/%y")
        # return datetime.datetime.now().strftime("%y/%m/%d-%H:%M:%S")
        return datetime.datetime.now().strftime("%y_%m_%d-%H_%M_%S")

    @staticmethod
    def save_img(img):
        print("taking img")
        path = './logs/'
        time_taken = FaceDetection().time_stamp()
        filename = path + time_taken + '.jpg'
        cv2.imwrite(filename, img)

    def display_cam(self, faces_cords, img_to_display, text_to_display, save_img=False):
        if self.DISPLAY:
            self.rectangle_multiple_faces(faces_cords, img_to_display)    
            if save_img:
                self.save_img(img_to_display)

            if self.DISPLAY_INFO:
                cv2.rectangle(img_to_display, (0, 430), (710,900), (255, 255, 255), -1)
                cv2.putText(img_to_display, text_to_display, (10, 470), self.FONT, 1, (0, 0, 0), 2, cv2.LINE_AA)
                cv2.circle(img_to_display, (300, 120), 10, (0, 0, 255), -1)
                cv2.imshow('Video', img_to_display)

    def find_face_target_size(self, faces_cords):
        face_size = 0
        if type(faces_cords) != tuple:
            index = self.largest_face_index(faces_cords)
            largest_face = (faces_cords[index][0], faces_cords[index][1], faces_cords[index][2], faces_cords[index][3])
            face_size = largest_face[3]
        if self.DEBUG:
            print(f'{largest_face}, size: {face_size}')
        return face_size

    def mirror_img(self, img_to_mirror):
        if self.MIRROR:
            img_to_mirror = cv2.flip(img_to_mirror, 1)
        return img_to_mirror

    def should_break(self):
        if cv2.waitKey(1) & 0xFF == ord('q'):
            # When everything is done, release the capture
            self.video_capture.release()
            cv2.destroyAllWindows()
            return True

    def create_grey_frame(self, frame):
        grey_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return grey_img

    def create_frame(self):
        ret, frame = self.video_capture.read()
        return frame

    def get_faces_cords(self, img_to_scan):

        try:
            faces_cords = self.faceCascade.detectMultiScale(
                img_to_scan,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(self.MIN_SIZE, self.MIN_SIZE),
                # flags=cv2.cv.CV_HAAR_SCALE_IMAGE
            )
        except Exception as e:
            faces_cords = None
            print(e)

        return faces_cords

    def get_eyes_cords(self, img_to_scan): #should not work
        eyes_cords = self.eyeCascade.detectMultiScale(
                img_to_scan
            )
        return eyes_cords

    def loop(self):
        while True:
            
            data_msg = ""
            # Capture frame-by-frame
            
            grey_img = self.create_grey_frame(self.mirror_img(self.create_frame()))
            faces_cords = self.get_faces_cords(grey_img)
            face_size = self.find_face_target_size(faces_cords)

            if face_size < 350:
                # arduino.send_serial_data("c") # display on screen to come closer 
                # time.sleep(0.1)
                data_msg = "come closer"
            else: 
                # arduino.send_serial_data("m") # measure temperature
                time.sleep(0.1)
                # data = arduino.receive_serial_data()
                data_msg = "temperature is being measured"

            self.display_cam(faces_cords, grey_img, text_to_display=data_msg)

            if self.should_break():
                break
            


print(f'{__name__}.py imported...')

# print(FaceDetection().time_stamp())
# if arduino.connection_established:
#     FaceDetection().loop()
# fd = FaceDetection()
# fd.loop()    
# When everything is done, release the capture
fd = FaceDetection()


# while True:
#     frame = fd.mirror_img(fd.create_frame())
#     grey_frame = fd.create_grey_frame(frame)

#     faces_cords = fd.get_faces_cords(grey_frame)
#     face_size = fd.find_face_target_size(faces_cords)
#     fd.display_cam(faces_cords, frame, text_to_display="test")

#     if fd.should_break():
#         break
