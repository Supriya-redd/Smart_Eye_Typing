# Smart_Eye_Typing
 👁️ EyeType — Accessible Gaze Typing

EyeType is an accessibility-focused eye-gaze typing application that allows users to type using their eye movements instead of a traditional keyboard.

The application uses a webcam to track facial and eye landmarks with MediaPipe, estimates the user's gaze direction, and maps the gaze position to an on-screen virtual keyboard. A key is selected when the user maintains their gaze on it for 1.3 seconds.

 ✨ Features

* 👁️ Real-time eye-gaze tracking using a webcam
* 🎯 Four-direction gaze calibration
* ⌨️ On-screen QWERTY virtual keyboard
* ⏱️ 1.3-second gaze dwell selection
* 🔤 Text input using eye movements
* 🔊 Text-to-speech functionality
* ⌫ Backspace, Space, Enter, and Clear controls
* 📷 Live camera preview
* 💻 Desktop GUI built with Tkinter
* ♿ Designed with accessible communication in mind

🛠️ Technologies Used

* **Python**
* **Tkinter** — Graphical User Interface
* **OpenCV** — Webcam and image processing
* **MediaPipe Tasks** — Face and eye landmark detection
* **Pillow (PIL)** — Camera frame display
* **pyttsx3** — Text-to-speech
* **NumPy / Python standard libraries** — Supporting processing and utilities

 🧠 How It Works

The application follows these steps:

1. Start the Camera

   * The webcam captures the user's face in real time.
   * MediaPipe Face Landmarker detects facial landmarks.

2. Calibrate Gaze

   * The user looks:

     * Left
     * Right
     * Up
     * Down
   * The application records the corresponding eye positions.

3. Estimate Gaze

   * Eye landmark positions are converted into normalized horizontal and vertical gaze coordinates.

4. Map Gaze to Keyboard

   * The normalized gaze coordinates are mapped onto the virtual keyboard.

5. Dwell Selection

   * A keyboard key is highlighted when the user's gaze points toward it.
   * Keeping the gaze on the key for 1.3 seconds activates it.

6. Create a Message

   * Selected letters are added to the message box.
   * The user can also use Space, Backspace, Clear, and Enter.

7. Text-to-Speech

   * The completed message can be spoken aloud using the Speak Message feature.

 📋 Requirements

* Python 3.9+
* Working webcam
* Good and reasonably even lighting
* Windows/macOS/Linux desktop environment

 📦 Installation

 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/EyeType.git
cd EyeType
```

 2. Install dependencies

```bash
pip install opencv-python mediapipe pillow pyttsx3
```

 3. Run the application

```bash
python eye_typing.py
```

The application automatically downloads the required MediaPipe Face Landmarker model the first time the camera is started.

 🎮 How to Use

 Step 1 — Start Camera

Click:

Start / Stop Camera

Make sure your face is clearly visible to the webcam.

 Step 2 — Calibrate

Click:

Calibrate Gaze

Follow the instructions and look in the requested directions while keeping your head relatively still.

 Step 3 — Start Typing

Look at a key on the virtual keyboard.

The key will become highlighted.

Hold your gaze on the key for approximately 1.3 seconds to select it.

Step 4 — Continue Typing

After a key is selected, look away and then look at the next key.

 Step 5 — Speak the Message

After creating your message, click:

Speak Message

The application will attempt to read the message aloud.

 📁 Project Structure

```text
EyeType/
│
├── eye_typing.py
├── face_landmarker.task     # downloaded automatically
└── README.md
```

🎯 Project Objective

The main objective of EyeType is to explore an alternative communication method for people who may have difficulty using a conventional keyboard or mouse.

By combining computer vision, eye-gaze estimation, and a virtual keyboard, the project demonstrates how human-computer interaction can be made more accessible.

 🚀 Future Improvements

Possible future improvements include:

* More accurate gaze estimation
* Personalized calibration
* Blink-based selection
* Adjustable dwell time
* Word prediction and autocomplete
* Multiple keyboard layouts
* Improved noise and head-movement handling
* Custom accessibility settings
* Better speech controls
* Support for additional languages
* More advanced gaze tracking using machine-learning models

⚠️ Limitations

The accuracy of gaze selection can depend on:

* Webcam quality
* Lighting conditions
* Distance from the camera
* Face position
* Head movement
* Individual eye characteristics

The current implementation uses a relatively simple four-direction calibration approach, so it is intended primarily as a prototype / accessibility project rather than a clinical-grade eye-tracking system.

 👩‍💻 Author

Alla Supriya

B.Tech — Computer Science Engineering
GITAM University, Bengaluru

📌 Project

Smart Eye Typing Application Using Eye Gaze Recognition and Virtual Keyboard


⭐ If you find this project interesting, consider giving the repository a star!
