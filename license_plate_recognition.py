import cv2
import requests
import time
import subprocess

# Use 0 for the default webcam on your PC
video_source = 0  

def extract_license_plate(frame):
    """
    Extract license plate text using OpenALPR.
    """
    # Save the frame as an image
    frame_path = 'temp_frame.jpg'
    cv2.imwrite(frame_path, frame)

    # Run OpenALPR on the image
    result = subprocess.run(['alpr', '-c', 'us', frame_path], capture_output=True, text=True)

    # Process OpenALPR output and extract plate number
    for line in result.stdout.splitlines():
        if line.startswith(" plate: "):
            return line.split(': ')[1].strip()

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

def main():
    cap = cv2.VideoCapture(video_source)
    if not cap.isOpened():
        print("Failed to connect to the webcam.")
        return

    last_capture_time = time.time()  # Track the last time an image was captured

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to read frame from webcam.")
            break

        # Display the video feed
        cv2.imshow("Live Feed", frame)

        current_time = time.time()
        
        # Capture an image every 10 seconds
        if current_time - last_capture_time >= 10:
            last_capture_time = current_time
            
            # Extract text from the captured frame
            license_plate = extract_license_plate(frame)
            if license_plate:
                print(f"Detected License Plate: {license_plate}")

                # Check database
                result = check_plate_in_database(license_plate)
                if result.get("registered"):
                    print("Access Granted")
                else:
                    print("Access Denied")
            else:
                print("No license plate detected.")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
