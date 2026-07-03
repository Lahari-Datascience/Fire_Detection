🔥 Fire Detection System using Live Camera & Email Alerts
📌 Project Overview
The Fire Detection System is a real-time safety application designed to detect fire using a live camera feed. When fire is detected, the system automatically captures an image and sends an email alert to the concerned recipient (home owner, organization, or authority) with the captured image and a warning message stating "Fire Detected". This system helps in early fire detection and quick response to prevent damage and loss.

⚙️ How the System Works
A live camera continuously monitors the environment.
Each video frame is analyzed using computer vision techniques to detect fire-like patterns such as color, intensity, and motion.
When fire is detected:
The system captures the image from the live feed.
The captured image is saved locally.
An email alert is sent to the registered recipient:
The email contains the captured image as an attachment.
The email body includes a warning message: "Fire Detected".
The email is sent using the sender’s email credentials configured in the code (developer/system email).
🚨 Key Features
🔴 Real-time fire detection using a live camera
📸 Automatic image capture on fire detection
📧 Email alert with image attachment
⚡ Fast response for early warning
🏠 Useful for homes, offices, industries, and public places
🛠️ Technologies Used
Python
OpenCV (for live camera and image processing)
SMTP (for sending emails)
MIME (for email attachments)
