from cv2 import *
import time
import openpyxl
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

VIDEO_CODEC = cv2.VideoWriter_fourcc(*'XVID')


VIDEO_FPS = 60
VIDEO_SIZE = (640, 480)


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, VIDEO_FPS)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, VIDEO_SIZE[0])
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, VIDEO_SIZE[1])

width, height = VIDEO_SIZE
out = cv2.VideoWriter("output_video_file\_video.avi", VIDEO_CODEC, VIDEO_FPS, (width, height))

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
font = cv2.FONT_HERSHEY_SIMPLEX




if not cap.isOpened():
    print("Unable to read camera feed")
    exit()

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(r'capture_train\face_recognizer_model.yml')

workbook = openpyxl.Workbook()
worksheet = workbook.active

worksheet.append(['Name', 'Date', 'Time', 'Status', 'Email'])

names = []
emails = []
absent = []
dict = {}

with open('student_data\data.txt', 'r') as f:
    for line in f:
        name, email = line.strip().split(',')
        names.append(name)
        emails.append(email)
        absent.append(name)
        dict[name] = email

all_students = names.copy()
detected_faces = set()  


SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 465
SMTP_USERNAME = 'piyanshul1307@gmail.com'
SMTP_PASSWORD = 'voqjeuzdbrrcjbjs'

def send_email(to_email, subject, body):
    from_email = SMTP_USERNAME

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            print("Connected to SMTP server.")
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            print("Logged in to SMTP server.")
            server.sendmail(from_email, to_email, msg.as_string())
            print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Error sending email to {to_email}: {e}")

confidence_threshold = 60
while True:
    ret, frame = cap.read()
    if not ret:
        print("Unable to read camera feed")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    detected_faces = set()
    for (x, y, w, h) in faces:
        face_key = (x, y, w, h)
        if face_key in detected_faces:
            continue 
        
        detected_faces.add(face_key)  

        label, confidence = recognizer.predict(cv2.resize(gray[y:y + h, x:x + w], (100, 100)))
        if confidence < confidence_threshold:
            continue  # Skip faces with low confidence

        current_time_string = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        status = "Present"
        if names[label] in all_students:
            worksheet.append([names[label], time.strftime("%Y-%m-%d"), time.strftime("%H:%M:%S"), status, emails[label]])
            all_students.remove(names[label])  # Remove from the list to avoid marking again

        cv2.putText(frame, names[label], (x, y - 5), font, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
        try:
            index = all_students.index(names[label])
            print("DOING:")
            removed_student = all_students.pop(index)
            print(f"PRESENT: {removed_student}")
        except ValueError:
            continue      
        cv2.putText(frame, names[label], (x, y - 5), font, 0.5, (255, 0, 0), 1, cv2.LINE_AA)

    out.write(frame)

    cv2.imshow("Video Footage", frame)
    
    b=[]
    if cv2.waitKey(1) & 0xFF == ord('q'):
        for i in all_students:
            e = dict[i]
            b.append(i)
            send_email(e, "Attendance Alert", f"Dear {i},\n\nYou were absent in today's class. Please contact {SMTP_USERNAME} for more information.")
        print("EMAIL send to ",b)
        break
for i, student in enumerate(all_students, start=2):
    worksheet.append([student, '', '', "Absent",dict[student]])
    print(f"ABSENT : {student}")

workbook.save(r'attendance_files\attendance.xlsx')

cv2.destroyAllWindows()
out.release()
cap.release()
