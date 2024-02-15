Facial Recognition Attendance System
This repository includes three Python scripts that together create a Facial Recognition Attendance System. The system captures facial images, trains a recognition model, and automates attendance tracking in a classroom setting.

Prerequisites
OpenCV: Open Source Computer Vision Library
Openpyxl: A Python library to interact with Excel files
NumPy: Fundamental package for scientific computing with Python
smtplib: Standard library module for sending emails
Haar Cascade File: Pre-trained face detection model
Setup
Install the required Python libraries:


pip install opencv-python openpyxl numpy
Download the Haar Cascade file from the provided link and save it as "haarcascade_frontalface_default.xml" in the same directory as the script.

Update the script with your SMTP server details (SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, and SMTP_PASSWORD).

Prepare a text file named "data.txt" in the "student_data" directory with student names and emails separated by commas.

Ensure that the trained face recognizer model is saved as "face_recognizer_model.yml" in the "Train_model" directory.

Adjust other constants such as ATTENDANCE_INTERVAL, VIDEO_CODEC, VIDEO_FPS, and VIDEO_SIZE according to your requirements.

Usage
This script captures multiple facial images of an individual and saves them to a data file for later use in training a recognition model.

Setup
Install the required Python libraries:

pip install opencv-python numpy

The captured images will be saved in the "captured_images" directory with filenames in the format "user_1.jpg", "user_2.jpg", etc.

2. Model Training Program
train_model.py
This script reads the captured facial images, trains a recognition model, and saves the trained model for later use in face recognition applications.

Setup
Install the required Python libraries:

pip install opencv-python numpy

Ensure that the "captured_images" directory contains facial images captured using the image_capture.py script.


The script will train a recognition model and save it as "face_recognizer_model.yml" in the "Train_model" directory.

The trained model is ready for use in face recognition applications.

3. Facial Recognition Attendance System
attendance_system.py
This script uses the trained model to automate attendance tracking in a classroom setting.

Usage
Run the script:
this script will use the trained model and predict the face in the classroom and mark the attendence in the excel sheet

Press 'q' to exit the script.

Email Notifications
The attendance system sends email alerts to absent students. Ensure that the SMTP server details are correctly configured.

Output
The attendance system generates a video file named "_video.avi" containing the recorded attendance with face rectangles.
The attendance details are saved in an Excel file named "attendance.xlsx" in the "attendence_file" directory.
Notes:
Make sure the webcam is connected and accessible.
The scripts continuously capture video or images until the user presses 'q'.
Adjust parameters, file paths, and settings as needed for your specific use case.
Customize the scripts according to your requirements and integrate them into your facial recognition system.