from cgitb import text
from serial_communication import SerialCom
from user import User
from computer_vision.face_detection import FaceDetection
from apis.gmail_api import GmailService
from apis.sheets_api import *
import time
from playsound import playsound
import threading
import socket
import os




STATION_NAME = socket.gethostname()

print("main.py running")
print("check...")

def main():

    convert = lambda value: True if "TRUE" else False
    sound_not_playing = True
    
    log = SheetsEntry()
    settings = log.new_settings()

    fd = FaceDetection()
    fd.DISPLAY = convert(settings['display'])
    fd.MIN_FACE_SIZE = settings['min_face_size'] # 275
    LOGS = True
    SAVE_IMG = convert(settings['save_img'])
    CRITICAL_TEMP = settings['critical_temp']

    print(f"selected CRITICAL_TEMP is: {CRITICAL_TEMP} asdf")
    time.sleep(5)




    if LOGS:
        gmail_service = GmailService()
        gmail_service.supervisors_emails = settings['supervisor_emails'].split(';')
        log.open_log_sheet()

    last_user_id = ""



    arduino = SerialCom('115200')
    print(arduino.connection_established, arduino.serial_baudrate, arduino.com_port, sep='\n')

    if arduino.connection_established:

        db = Cache("db")
        cached_log = False
        cached_email = False
        sound_counter = 0

        while True:
            sound_counter += 1

            if sound_counter == 50:
                sound_counter = 1
                sound_not_playing = True

            text_to_display = ""
            frame = fd.mirror_img(fd.create_frame())
            
            grey_frame = fd.create_grey_frame(frame)

            faces_cords = fd.get_faces_cords(grey_frame)
            face_size = fd.find_face_target_size(faces_cords)

            user_data = arduino.receive_serial_data()
            time_received = log.timestamp()

            print(f"{user_data}")
            current_user = User(user_data)
            

            if face_size < fd.MIN_FACE_SIZE and current_user.distance > 40:
                text_to_display = f" {current_user.distance}cm "
                if current_user.rfid == "00000000":
                    text_to_display += " Scan RFID"
            else:
                if current_user.rfid == "00000000":
                    text_to_display += " Scan your RFID card"
                    text_to_display += f" Temp: {current_user.temperature}. "
                    if sound_not_playing:
                        threading.Thread(target=playsound, args=("audio_instructions/scan_rfid.mp3",)).start()
                        sound_not_playing = False
                else:
                    if float(current_user.temperature) > 30:

                        text_to_display = "Normal temperature, go on."
                        if sound_not_playing:
                            threading.Thread(target=playsound, args=("audio_instructions/normal_temp.mp3",))
                            sound_not_playing = False

                        if current_user.rfid != last_user_id:
                            if LOGS:
                                log_data = log.create_data_row(time_received, 
                                                                STATION_NAME,
                                                                current_user.rfid,
                                                                current_user.temperature)
                                try:
                                    threading.Thread(log.push_temp, args=(log_data,)).start()
                                except Exception as e:
                                    db.save_log(log_data)
                                    cached_log = True
                                    DebugLogs().debug_log(f"log.push_temp() failed", e)
                            if SAVE_IMG:
                                fd.save_img(frame)
                            last_user_id = current_user.rfid
        
                    if current_user.temperature > CRITICAL_TEMP:
                        text_to_display = "Recheck your temperature manually"
                        if sound_not_playing:
                            threading.Thread(target=playsound, args=("audio_instructions/recheck_temp.mp3",))
                            sound_not_playing = False
                        if LOGS:
                            report_letter = gmail_service.generate_report(f"User with id: {current_user.rfid}", 
                                                                            current_user.temperature,
                                                                            STATION_NAME)
                            try:
                                threading.Thread(target=gmail_service.report_user, args=(report_letter,)).start()
                                print("user reported")
                            except Exception as e:
                                # update local cache
                                db.save_email_notification(report_letter)
                                cached_email = True
                                DebugLogs().debug_log(f"report_user() in main() failed with report letter:\n {report_letter}", e)

            if fd.should_break():
                break
            try:
                fd.display_cam(faces_cords, frame, text_to_display)
            except Exception as e:
                DebugLogs().debug_log("display_cam() failed in main()", e)

            if cached_log:
                try:
                    db.reupload_log(log)
                    cached_log = False
                except Exception as e:
                    DebugLogs().debug_log("db.reupload_log() failed", e)
            
            if cached_email:
                try:
                    db.resend_emails(gmail_service)
                    cached_email = False
                except Exception as e:
                    DebugLogs().debug_log("db.resend_emails() failed", e)

    else:
        print("arduino connection is not established")
        if LOGS:
            gmail_service.send_email("Arduino connection failed...", "centigrade@kjg.lt", "Arduino was not connected")



if __name__ == "__main__":
    while True:
        main()
        time.sleep(5)

