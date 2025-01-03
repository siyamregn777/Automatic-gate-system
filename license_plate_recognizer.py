# import cv2
# import pytesseract
# import requests
# import time

# # Replace with your IP webcam URL
# url = "http://10.6.156.58:8080/video"  

# def extract_license_plate(frame):
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     blur = cv2.GaussianBlur(gray, (5, 5), 0)
#     thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#                                    cv2.THRESH_BINARY_INV, 11, 2)
#     license_plate_text = pytesseract.image_to_string(thresh, config='--psm 8')
#     return license_plate_text.strip()

# def check_plate_in_database(plate):
#     response = requests.get(f"http://localhost:5000/check_plate?plate={plate}")
#     return response.json()

# def connect_to_webcam(max_retries=5):
#     cap = None
#     for attempt in range(max_retries):
#         cap = cv2.VideoCapture(url)
#         if cap.isOpened():
#             print("Successfully connected to the webcam.")
#             return cap
#         print(f"Attempt {attempt + 1} failed, retrying...")
#         time.sleep(2)  # Wait before retrying
#     print("Failed to connect to the webcam after multiple attempts.")
#     return None

# def main():
#     cap = connect_to_webcam()
#     if not cap:
#         return

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             print("Frame read failed. Attempting to reconnect...")
#             cap.release()
#             cap = connect_to_webcam()
#             if not cap:
#                 break
#             continue  # Retry the frame capture with the new connection

#         # Extract license plate from the current frame
#         license_plate = extract_license_plate(frame)
#         print(f"Detected License Plate: {license_plate}")

#         if license_plate:
#             result = check_plate_in_database(license_plate)
#             if result.get("registered"):
#                 print("Access Granted")
#             else:
#                 print("Access Denied")

#         time.sleep(1)  # Adjust delay as needed

#     cap.release()
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     main()


























import cv2
import pytesseract
import requests
import time
# Replace with your IP webcam URL
url = "http://10.6.156.17:8080/video"  
def extract_license_plate(frame):
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Apply Gaussian blur to reduce noise
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # Apply adaptive thresholding
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 11, 2)
    # Use Tesseract to extract text
    license_plate_text = pytesseract.image_to_string(thresh, config='--psm 8')
    return license_plate_text.strip()
def check_plate_in_database(plate):
    response = requests.get(f"http://localhost:5000/check_plate?plate={plate}")
    return response.json()
def main():
    max_retries = 5
    cap = None
    # Attempt to connect to the webcam
    for attempt in range(max_retries):
        cap = cv2.VideoCapture(url)
        if cap.isOpened():
            print("Successfully connected to the webcam.")
            break
        print(f"Attempt {attempt + 1} failed, retrying...")
        time.sleep(2)  # Wait before retrying

    if not cap or not cap.isOpened():
        print("Failed to connect to the webcam after multiple attempts.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to read frame from webcam.")
            break

        # Extract license plate from the current frame
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





























# # import cv2
# # import pytesseract
# # import requests
# # import time

# # # Replace with your IP webcam URL
# # url = "http://10.6.156.17:8080/video"  

# # def extract_license_plate(frame):
# #     # Convert the frame to grayscale
# #     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
# #     # Apply Gaussian blur to reduce noise
# #     blur = cv2.GaussianBlur(gray, (5, 5), 0)
    
# #     # Apply adaptive thresholding
# #     thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
# #                                    cv2.THRESH_BINARY_INV, 11, 2)
    
# #     # Use Tesseract to extract text
# #     license_plate_text = pytesseract.image_to_string(thresh, config='--psm 8')
# #     return license_plate_text.strip()

# # def check_plate_in_database(plate):
# #     response = requests.get(f"http://localhost:5000/check_plate?plate={plate}")
# #     return response.json()

# # def main():
# #     cap = cv2.VideoCapture(url)

# #     while True:
# #         ret, frame = cap.read()
# #         if not ret:
# #             break

# #         # Extract license plate from the current frame
# #         license_plate = extract_license_plate(frame)
# #         print(f"Detected License Plate: {license_plate}")

# #         if license_plate:
# #             result = check_plate_in_database(license_plate)
# #             if result.get("registered"):
# #                 print("Access Granted")
# #             else:
# #                 print("Access Denied")

# #         time.sleep(1)  # Adjust delay as needed

# #     cap.release()
# #     cv2.destroyAllWindows()

# # if __name__ == "__main__":
# #     main()























# # # #license_plate_recognizer.py

# # # import cv2
# # # import pytesseract
# # # import requests
# # # import time

# # # url = "http://10.9.220.32:8080/video"  # Replace with your phone's IP

# # # def extract_license_plate(frame):
# # #     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# # #     _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
# # #     license_plate_text = pytesseract.image_to_string(thresh)
# # #     return license_plate_text.strip()

# # # def check_plate_in_database(plate):
# # #     response = requests.get(f"http://localhost:5000/check_plate?plate={plate}")
# # #     return response.json()

# # # def main():
# # #     cap = cv2.VideoCapture(url)

# # #     while True:
# # #         ret, frame = cap.read()
# # #         if not ret:
# # #             break

# # #         license_plate = extract_license_plate(frame)
# # #         print(f"Detected License Plate: {license_plate}")

# # #         if license_plate:
# # #             result = check_plate_in_database(license_plate)
# # #             if result.get("registered"):
# # #                 print("Access Granted")
# # #             else:
# # #                 print("Access Denied")

# # #         time.sleep(1)  # Adjust delay as needed

# # #     cap.release()
# # #     cv2.destroyAllWindows()

# # # if __name__ == "__main__":
# # #     main()