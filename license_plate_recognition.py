import cv2
import requests
import time
import subprocess
import numpy as np
import easyocr

# IP Webcam URL (use your actual IP address)
ip_camera_url = "http://10.9.154.42:8080/video"

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

def extract_license_plate(frame, max_attempts=7):
    """
    Extract license plate text using EasyOCR. Retry up to max_attempts times.
    """
    attempt = 0
    while attempt < max_attempts:
        # Save the frame as an image
        frame_path = 'temp_frame.jpg'
        cv2.imwrite(frame_path, frame)

        # Use EasyOCR to extract text
        result = reader.readtext(frame_path)

        # Check if any text is detected and return the first detected text (assumed to be the license plate)
        for detection in result:
            text = detection[1]
            # Optionally filter the text based on patterns (e.g., numbers and letters for license plates)
            if len(text) > 5:  # Assuming license plates are at least 6 characters long
                return text.strip()

        attempt += 1
        print(f"Attempt {attempt} failed to detect a license plate.")

    return None

def check_plate_in_database(plate):
    """
    Check if the license plate exists in the database by sending a request to the API.
    """
    try:
        response = requests.get(f"http://localhost:5000/check_plate?plate={plate}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error checking plate in database: {e}")
        return {"registered": False}

def motion_detected(prev_frame, current_frame, min_area=500):
    """
    Detect motion by comparing consecutive frames.
    """
    # Convert both frames to grayscale
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    current_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    
    # Compute the absolute difference between the current and previous frames
    frame_diff = cv2.absdiff(prev_gray, current_gray)
    
    # Threshold the difference image to highlight changes
    _, thresh = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)
    
    # Find contours of the moving objects
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        if cv2.contourArea(contour) > min_area:
            return True
    return False

def main():
    # Open the video feed from the IP Webcam
    cap = cv2.VideoCapture(ip_camera_url)
    if not cap.isOpened():
        print("Failed to connect to IP Webcam.")
        return

    last_capture_time = time.time()  # Track the last time an image was captured
    prev_frame = None  # Store the previous frame for motion detection

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to read frame from IP Webcam.")
            break

        # Display the video feed
        cv2.imshow("Live Feed", frame)

        current_time = time.time()

        # Perform motion detection if there is a previous frame
        if prev_frame is not None:
            if motion_detected(prev_frame, frame):
                print("Motion detected!")

                # Try extracting the license plate up to 7 times using EasyOCR
                license_plate = extract_license_plate(frame, max_attempts=7)
                if license_plate:
                    print(f"Detected License Plate: {license_plate}")
                    # Check database
                    result = check_plate_in_database(license_plate)
                    if result.get("registered"):
                        print("Access Granted")
                    else:
                        print("Access Denied")
                else:
                    print("Failed to detect a license plate after 7 attempts.")

        # Update previous frame
        prev_frame = frame

        # Exit when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
