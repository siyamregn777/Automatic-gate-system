import cv2
import pytesseract
import requests
import time

url = "http://10.9.220.32:8080/video"  # Replace with your phone's IP

def extract_license_plate(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    license_plate_text = pytesseract.image_to_string(thresh)
    return license_plate_text.strip()

def check_plate_in_database(plate):
    response = requests.get(f"http://localhost:5000/check_plate?plate={plate}")
    return response.json()

def main():
    cap = cv2.VideoCapture(url)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        license_plate = extract_license_plate(frame)
        print(f"Detected License Plate: {license_plate}")

        if license_plate:
            result = check_plate_in_database(license_plate)
            if result.get("registered"):
                print("Access Granted")
            else:
                print("Access Denied")

        time.sleep(1)  # Adjust delay as needed

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()