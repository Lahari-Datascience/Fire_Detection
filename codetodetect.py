import cv2
import numpy as np
import pygame
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

# ====== Email Setup ======
sender_email = "devinaidu2006@gmail.com"
receiver_email = "23nn1a4441preethi@gmail.com"
password = "jmrj ovnv ucug wyge"  # App password

def send_email(message, image_path=None):
    subject = "🔥 Fire Alert"
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    if image_path:
        with open(image_path, 'rb') as f:
            img = MIMEImage(f.read())
            img.add_header('Content-Disposition', 'attachment', filename="fire.jpg")
            msg.attach(img)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("📧 Email with image sent successfully!")
    except Exception as e:
        print("❌ Failed to send email:", e)

# ====== Alarm Setup ======
pygame.mixer.init()
pygame.mixer.music.load("orey aajamu (2).mp3")  # Make sure this file exists

# ====== Fire Detection Setup ======
cap = cv2.VideoCapture(0)

# HSV range for detecting fire
lower_fire = np.array([10, 150, 150])
upper_fire = np.array([35, 255, 255])
min_fire_area = 3000

alert_triggered = False
email_sent = False
no_fire_message_printed = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (800, 600))
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower_fire, upper_fire)
    mask = cv2.dilate(mask, None, iterations=2)
    mask = cv2.erode(mask, None, iterations=2)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    fire_detected = False

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > min_fire_area:
            fire_detected = True
            cv2.drawContours(frame, [contour], -1, (0, 0, 255), 2)

    if fire_detected:
        if not alert_triggered:
            print("🔥 Fire Detected! Alarm ringing!")
            pygame.mixer.music.play()
            alert_triggered = True
            no_fire_message_printed = False

    # === Draw "Fire Detected" text ===
        text = "🔥 FIRE DETECTED"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.2
        thickness = 3
        color = (0, 255, 0)  # Green text

        (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, thickness)
        frame_height, frame_width = frame.shape[:2]
        x = int((frame_width - text_width) / 2)
        y = int((frame_height + text_height) / 2)

        # Put text on the current frame
        
        cv2.putText(frame, text, (x, y), font, font_scale, color, thickness)

    if not email_sent:
        fire_image_path = "fire_image.jpg"
        cv2.imwrite(fire_image_path, frame)  # Save AFTER drawing "Fire Detected"
        send_email("🔥 Fire has been detected by your system.", fire_image_path)
        email_sent = True

        fire_image_path = "fire_detected.jpg"
        cv2.imwrite(fire_image_path, frame)

        if not email_sent:
            send_email("🔥 Fire has been detected by your system.", fire_image_path)
            email_sent = True

    else:
        cv2.putText(frame, "No Fire Detected", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)
        if not no_fire_message_printed:
            print("✅ No Fire Detected.")
            no_fire_message_printed = True
        alert_triggered = False
        email_sent = False

    cv2.imshow("🔥 Fire Detection System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
