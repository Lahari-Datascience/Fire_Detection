# 🔥 Fire Detection System using Live Camera & Email Alerts

A real-time fire safety application that monitors a live camera feed, detects fire using computer vision, and automatically sends an email alert — complete with a captured image — to a registered recipient the moment fire is detected.

## 📌 Project Overview

The Fire Detection System continuously watches a live video feed for fire-like patterns. As soon as fire is detected, it:
1. Captures a snapshot of the frame
2. Saves the image locally
3. Sends an instant email alert with the image attached and a **"Fire Detected"** warning message

This enables early fire detection and faster response, helping prevent damage, loss, and potential harm in homes, offices, industries, and public spaces.

## ⚙️ How the System Works

1. **Live Monitoring** — A connected camera continuously streams video frames.
2. **Frame Analysis** — Each frame is processed using computer vision techniques to identify fire-like characteristics such as color, intensity, and motion patterns.
3. **Detection & Capture** — When fire is detected in a frame:
   - The frame is captured and saved locally as an image.
4. **Email Alert** — An automated email is sent to the configured recipient:
   - **Attachment:** the captured fire image
   - **Body:** warning message — *"Fire Detected"*
   - Sent via the sender's email credentials (configured in code) using SMTP.

## 🚨 Key Features

- 🔴 **Real-time fire detection** using a live camera feed
- 📸 **Automatic image capture** the moment fire is detected
- 📧 **Instant email alerts** with the captured image attached
- ⚡ **Fast response** for early warning and quick action
- 🏠 **Versatile use cases** — homes, offices, industrial sites, and public places

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| **Python** | Core programming language |
| **OpenCV** | Live camera feed capture & image processing |
| **SMTP** | Sending email alerts |
| **MIME** | Attaching images to email alerts |

## 🚀 Getting Started

### Prerequisites
- Python 3.x
- A working webcam / live camera feed
- An email account with SMTP access enabled (e.g., Gmail with an App Password)

### Installation
```bash
git clone https://github.com/<your-username>/fire-detection-system.git
cd fire-detection-system
pip install opencv-python
```

### Configuration
Update the email credentials and recipient address in the script:
```python
SENDER_EMAIL = "your_email@example.com"
SENDER_PASSWORD = "your_app_password"
RECEIVER_EMAIL = "recipient_email@example.com"
```
> ⚠️ **Do not hardcode real credentials in code you push to GitHub.** Use environment variables or a `.env` file (see below).

### Run
```bash
python fire_detection.py
```

## 🔒 Security Note

Avoid committing email credentials directly into your source code. Recommended approach:
- Store credentials in a `.env` file
- Add `.env` to `.gitignore`
- Load credentials using `python-dotenv`

## 📂 Project Structure

```
.
├── fire_detection.py     # Main script — camera feed, fire detection, email alert
├── captured_images/      # Locally saved snapshots of detected fires
├── requirements.txt
└── README.md
```

## 🔮 Future Improvements

- Integrate a trained deep learning model (CNN) for more accurate fire detection instead of purely color/intensity-based rules
- Add SMS/WhatsApp alerts alongside email
- Add a live dashboard to monitor camera feed and detection history
- Support multiple camera feeds simultaneously
