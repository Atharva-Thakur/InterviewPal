import cv2
from tensorflow.keras.models import load_model
import numpy as np
import os
import time
import random

# Load pre-trained models
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
emotion_model = load_model('C:\\Users\\shrut\\OneDrive\\Desktop\\SHRUTI\\VIT\\SEM-5\\EDI\\New folder\\model_1.h5')  # Replace 'path_to_emotion_model.h5' with your actual model path

# Define emotions
EMOTIONS = ["Angry", "Disgust", "Fear", "Happy", "Sad", "Surprise", "Neutral"]

# Function to detect and predict emotion
def detect_emotion(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    emotions = []
    
    for (x, y, w, h) in faces:
        face_roi = gray[y:y + h, x:x + w]
        resized = cv2.resize(face_roi, (48, 48))
        normalized = resized / 255.0
        reshaped = np.reshape(normalized, (1, 48, 48, 1))
        result = emotion_model.predict(reshaped)

        # Emotion prediction
        label = EMOTIONS[np.argmax(result)]
        emotions.append(label)

        # Draw rectangle around the face and put label
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(frame, label, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    return frame, emotions

# Create a directory to save the analyzed frames
output_dir = 'analyzed_frames'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Video capture
cap = cv2.VideoCapture(0)  # Change to the appropriate video source if needed

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Perform emotion detection
    detected_frame, emotions = detect_emotion(frame)

    # Display the resulting frame
    cv2.imshow('Facial Emotion Detection', detected_frame)

    # Save analyzed frames with emotions
    if len(emotions) > 0:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        output_filename = f"{output_dir}/frame_{timestamp}.jpg"
        cv2.imwrite(output_filename, detected_frame)
        print(f"Frame saved: {output_filename}")

    # Wait for a random interval before capturing the next frame
    random_interval = random.randint(5, 15)  # Random interval between 5 and 15 seconds
    key = cv2.waitKey(random_interval * 1000)  # Convert to milliseconds
    if key == ord('q'):
        break

# Release the capture and destroy windows
cap.release()
cv2.destroyAllWindows()