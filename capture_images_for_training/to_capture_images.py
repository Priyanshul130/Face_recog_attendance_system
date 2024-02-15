import cv2
import time
import os




# Function to capture multiple photos
def capture_photos(person_name, save_dir, num_photos=10):
    # Open a connection to the webcam
    cap = cv2.VideoCapture(0)

    # Load the Haar cascade file for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Create the directory if it doesn't exist
    os.makedirs(save_dir, exist_ok=True)

    print(f"Capturing {num_photos} photos. Press 'q' to exit.")

    # Loop to capture photos
    photo_count = 0
    while photo_count < num_photos:
        # Capture a frame from the webcam
        ret, frame = cap.read()

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Draw rectangles around the detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # Save the face region as an image
            face_roi = frame[y:y+h, x:x+w]
            photo_count += 1
            photo_filename = f"{person_name}_{photo_count}.jpg"
            photo_path = os.path.join(save_dir, photo_filename)
            cv2.imwrite(photo_path, face_roi)

            print(f"Photo {photo_count} captured.")

        # Display the frame
        cv2.imshow('Capture Photos', frame)
      

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close the OpenCV window
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Set the person's name and the directory to save photos
    person_name = input("Enter name of student whose photo to be captured")
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data_set')
    save_directory = os.path.join(os.path.dirname(__file__), '..', f'student_data\photoes\{person_name}')

    # Call the function to capture photos
    capture_photos(person_name, save_directory, num_photos=500)
