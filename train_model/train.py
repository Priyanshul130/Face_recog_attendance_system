import cv2
import os
import numpy as np

# create a face recognizer object
recognizer = cv2.face.LBPHFaceRecognizer_create()

# define the path to the dataset
data_path = os.path.join(os.path.dirname(__file__), '..', 'student_data/photoes')


# define the list of labels
labels = []

# define the list of face images
faces = []

# create a dictionary that maps each name to a unique integer
name_to_int = {}
int_to_name = {}
current_int = 0

# loop through each folder in the dataset
for name in os.listdir(data_path):
    # get the path to the folder
    folder_path = os.path.join(data_path, name)

    # check if the folder contains images
    if os.path.isdir(folder_path):
        # add the name to the dictionary
        name_to_int[name] = current_int
        int_to_name[current_int] = name
        current_int += 1

# loop through each folder in the dataset again
for name in os.listdir(data_path):
    # get the path to the folder
    folder_path = os.path.join(data_path, name)

    # check if the folder contains images
    if os.path.isdir(folder_path):
        # loop through each image in the folder
        for img_name in os.listdir(folder_path):
            # get the path to the image
            img_path = os.path.join(folder_path, img_name)

            # convert the image to grayscale
            gray_img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

            # add the grayscale image to the list of faces
            faces.append(gray_img)

            # add the integer label to the list of labels
            labels.append(name_to_int[name])

# train the face recognizer model
recognizer.train(faces, np.array(labels, dtype=np.int32))

# save the trained model to a file
recognizer.save('face_recognizer_model.yml')
