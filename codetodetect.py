"""
Fire Detection System using Live Camera & Email Alerts
--------------------------------------------------------
Detects fire in a live webcam feed using HSV color thresholding,
plays an alarm, overlays a warning on-screen, and sends an email
alert with the captured frame attached.

SETUP:
1. pip install opencv-python numpy pygame python-dotenv
2. Create a .env file in this same folder with:
       SENDER_EMAIL=your_email@gmail.com
       SENDER_PASSWORD=your_app_password
       RECEIVER_EMAIL=recipient_email@gmail.com
3. Add .env to .gitignore so credentials never get pushed to GitHub.
4. Place an alarm sound file in this folder and update ALARM_SOUND_PATH below.
"""

import os
import time
import cv2
import numpy as np
import pygame
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from dotenv import load_dotenv

# ====== Load credentials from .env (never hardcode these) ======
load_dotenv()
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

if not all([SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL]):
    raise RuntimeError(
        "Missing email credentials. Create a .env file with SENDER_EMAIL, "
        "SENDER_PASSWORD, and RECEIVER_EMAIL before running this script."
    )

# ====== Config ======
ALARM_SOUND_PATH = "fire_alarm.mp3"          # update to your actual sound file
FIRE_IMAGE_PATH = "fire_detected.jpg"
MIN_FIRE_AREA = 3000
EMAIL_COOLDOWN_SECONDS = 60             # avoid spamming emails while fire persists

# HSV range for detecting fire-colored regions
LOWER_FIRE = np.array([10, 150, 150])
UPPER_FIRE = np.array([35, 255, 255])


def send_email(message: str, image_path: str | None = None) -> None:
    """Send an email alert, optionally attaching an image."""
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg["Subject"] = "🔥 Fire Alert"
    msg.attach(MIMEText(message, "plain"))

    if image_path and os.path.exists(image_path):
        with open(image_path, "rb") as f:
            img = MIMEImage(f.read())
            img.add_header("Content-Disposition", "attachment", filename="fire.jpg")
            msg.attach(img)

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        print("📧 Email with image sent successfully!")
    except Exception as e:
        print("❌ Failed to send email:", e)


def detect_fire(frame: np.ndarray) -> tuple[bool, np.ndarray]:
    """Return (fire_detected, frame_with_contours_drawn)."""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, LOWER_FIRE, UPPER_FIRE)
    mask = cv2.dilate(mask, None, iterations=2)
    mask = cv2.erode(mask, None, iterations=2)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    fire_detected = False
    for contour in contours:
        if cv2.contourArea(contour) > MIN_FIRE_AREA:
            fire_detected = True
            cv2.drawContours(frame, [contour], -1, (0, 0, 255), 2)

    return fire_detected, frame


def draw_status_text(frame: np.ndarray, fire_detected: bool) -> np.ndarray:
    font = cv2.FONT_HERSHEY_SIMPLEX
    if fire_detected:
        text = "🔥 FIRE DETECTED"
        color = (0, 0, 255)  # red
        (text_width, text_height), _ = cv2.getTextSize(text, font, 1.2, 3)
        h, w = frame.shape[:2]
        x, y = int((w - text_width) / 2), int((h + text_height) / 2)
        cv2.putText(frame, text, (x, y), font, 1.2, color, 3)
    else:
        cv2.putText(frame, "No Fire Detected", (20, 50), font, 1.0, (0, 255, 0), 2)
    return frame


def main():
    pygame.mixer.init()
    alarm_available = os.path.exists(ALARM_SOUND_PATH)
    if alarm_available:
        pygame.mixer.music.load(ALARM_SOUND_PATH)
    else:
        print(f"⚠️  Alarm sound '{ALARM_SOUND_PATH}' not found — running without audio alarm.")

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Could not open webcam. Check your camera connection/index.")

    alarm_playing = False
    last_email_time = 0.0

    print("🎥 Fire detection running — press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️  Failed to read frame from camera.")
            break

        frame = cv2.resize(frame, (800, 600))
        fire_detected, frame = detect_fire(frame)
        frame = draw_status_text(frame, fire_detected)

        if fire_detected:
            # Alarm: start once, don't restart every frame
            if not alarm_playing and alarm_available:
                pygame.mixer.music.play(-1)  # loop while fire persists
                alarm_playing = True
                print("🔥 Fire Detected! Alarm ringing!")

            # Email: only send, with a cooldown, while fire is actually present
            now = time.time()
            if now - last_email_time > EMAIL_COOLDOWN_SECONDS:
                cv2.imwrite(FIRE_IMAGE_PATH, frame)
                send_email("🔥 Fire has been detected by your system.", FIRE_IMAGE_PATH)
                last_email_time = now
        else:
            if alarm_playing:
                pygame.mixer.music.stop()
                alarm_playing = False

        cv2.imshow("🔥 Fire Detection System", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
