import cv2
import time
import pandas as pd
import pytesseract
from datetime import datetime
from scipy.spatial import distance as dist

# --- CONFIGURATION (Tune these values) ---
CAR_WIDTH_FEET = 6
VIDEO_FPS = 30
SPEED_LIMIT_MPH = 10

# --- IMPORTANT: Set the path to your Tesseract installation ---
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# --- INTERNAL VARIABLES ---
FPS_TO_MPH = 0.681818
LOG_FILE_NAME = 'log.csv'
LOG_COOLDOWN_SECONDS = 5  # Don't log the same plate within this time
last_log_time = 0

# Load models
car_cascade = cv2.CascadeClassifier('cars.xml')
plate_cascade = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')

# --- NEW IP CAMERA CONFIGURATION ---
# Replace these with your actual camera details
username = "admin"
password = "admin"
ip_address = "10.164.140.195" # The camera's IP address
# You MUST find the correct path for your camera model!
stream_path = "/cam/realmonitor?channel=1&subtype=0"  # Adjust this path as needed

# Assembled RTSP URL
url = f"rtsp://{username}:{password}@{ip_address}{stream_path}"

cap = cv2.VideoCapture(url)
previous_centroids = []

print("System running... Press 'q' to quit.")

# Initialize the log file with headers if it doesn't exist
try:
    pd.read_csv(LOG_FILE_NAME)
except FileNotFoundError:
    df = pd.DataFrame(columns=['Timestamp', 'Speed (MPH)', 'License Plate'])
    df.to_csv(LOG_FILE_NAME, index=False)


def log_vehicle(speed, plate_text):
    global last_log_time
    # Check if enough time has passed since the last log
    if time.time() - last_log_time < LOG_COOLDOWN_SECONDS:
        return # Exit if it's too soon

    # Log the data
    new_log = pd.DataFrame({
        'Timestamp': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
        'Speed (MPH)': [f"{speed:.1f}"],
        'License Plate': [plate_text]
    })
    new_log.to_csv(LOG_FILE_NAME, mode='a', header=False, index=False)
    print(f"LOGGED: Speed={speed:.1f} MPH, Plate={plate_text}")
    last_log_time = time.time()


while True:
    ret, frame = cap.read()
    if not ret:
        break

    current_centroids = []
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cars = car_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    for (x, y, w, h) in cars:
        centroid = (int(x + w / 2), int(y + h / 2))
        current_centroids.append(centroid)

        speed_mph = 0
        box_color = (0, 255, 0) # Green

        if previous_centroids:
            previous_match = min(previous_centroids, key=lambda c: dist.euclidean(centroid, c))
            pixel_distance = dist.euclidean(centroid, previous_match)
            pixels_per_foot = w / CAR_WIDTH_FEET
            feet_distance = pixel_distance / pixels_per_foot
            speed_fps = feet_distance * VIDEO_FPS
            speed_mph = speed_fps * FPS_TO_MPH

            if speed_mph > SPEED_LIMIT_MPH:
                box_color = (0, 0, 255) # Red

                # --- PLATE DETECTION AND OCR ---
                # 1. Create a region of interest (ROI) for the car
                car_roi = gray[y:y+h, x:x+w]
                
                # 2. Detect plates within the car's ROI
                plates = plate_cascade.detectMultiScale(car_roi, scaleFactor=1.2, minNeighbors=5)
                
                for (px, py, pw, ph) in plates:
                    # 3. Extract the license plate ROI
                    plate_roi = car_roi[py:py+ph, px:px+pw]
                    
                    # Draw a blue box around the detected plate
                    cv2.rectangle(frame, (x+px, y+py), (x+px+pw, y+py+ph), (255, 0, 0), 2)
                    
                    try:
                        # 4. Use Tesseract to read the text
                        plate_text = pytesseract.image_to_string(plate_roi, config='--psm 8 --oem 3').strip()
                        
                        # Only log if text is found and has a reasonable length
                        if 2 < len(plate_text) < 10:
                            log_vehicle(speed_mph, plate_text)
                            
                    except Exception as e:
                        # print(f"OCR Error: {e}") # Uncomment for debugging
                        pass


        cv2.rectangle(frame, (x, y), (x+w, y+h), box_color, 2)
        cv2.putText(frame, f"{speed_mph:.1f} MPH", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, box_color, 2)

    previous_centroids = current_centroids.copy()
    cv2.imshow("Car Speed Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print(f"Program stopped. Data saved to {LOG_FILE_NAME}")