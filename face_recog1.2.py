import cv2
import time
import openpyxl
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


ATTENDANCE_INTERVAL = 30  # in seconds
VIDEO_CODEC = cv2.VideoWriter_fourcc(*'XVID')
VIDEO_FPS = 60
VIDEO_SIZE = (640, 480)


attendance_recorded = False
attendance_time = time.time()


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, VIDEO_FPS)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, VIDEO_SIZE[0])
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, VIDEO_SIZE[1])


width, height = VIDEO_SIZE
out = cv2.VideoWriter("output_video_file\_video.avi", VIDEO_CODEC, VIDEO_FPS, (width, height))

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
font = cv2.FONT_HERSHEY_SIMPLEX

if not cap.isOpened():
    print("unable to read camera feed")
    exit()

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(r'Train_model\face_recognizer_model.yml')

workbook = openpyxl.Workbook()
worksheet = workbook.active

worksheet.append(['Name', 'Date', 'Time', 'Status', 'Email'])


names = []
emails = []
absent=[]
dict={}
with open('student_data\data.txt', 'r') as f:
    for line in f:
        name, email = line.strip().split(',')
        names.append(name)
        emails.append(email)
        absent.append(name)
        dict[name]=email

all_students = names.copy()

print(dict)

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


while True:
    
    ret, frame = cap.read()
    if not ret:
        print("unable to read camera feed")
        break

    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    
    for (x, y, w, h) in faces:
        
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        
        label, confidence = recognizer.predict(cv2.resize(gray[y:y + h, x:x + w], (100, 100)))

        
    
        
        if not attendance_recorded:
            current_time_string = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            attendance_time = time.mktime(time.strptime(current_time_string, "%Y-%m-%d %H:%M:%S"))
            status = "Present"     
            worksheet.append([names[label], time.strftime("%Y-%m-%d"), time.strftime("%H:%M:%S"), status, emails[label]])
            attendance_recorded = True

            
            removed_student = all_students.pop(all_students.index(names[label]))
            print(f"PRESENT: {removed_student}")
           
        cv2.putText(frame, names[label], (x, y - 5), font, 0.5, (255, 0, 0), 1, cv2.LINE_AA)

    
    out.write(frame)

    
    cv2.imshow("video footage", frame)

    b=[]
    if cv2.waitKey(1) & 0xFF == ord('q'):
        for i in all_students:
            e=dict[i]
            send_email(e, "Attendance Alert", f"Dear {i},\n\nYou were absent in today's class. Please contact {SMTP_USERNAME} for more information.")   
            b.append(i)
        print('Email Send To  -',b) 
        break
    if attendance_recorded and time.time() - attendance_time > ATTENDANCE_INTERVAL:
        attendance_recorded = False

for i, student in enumerate(all_students, start=2):
    worksheet.append([student, '', '', "Absent")
    print(f"ABSENT : {student}")

            
workbook.save(r'attendence_file\attendance.xlsx')

cv2.destroyAllWindows()

out.release()

cap.release()
