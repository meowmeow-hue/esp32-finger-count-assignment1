# Assignment 1: Finger Count Detection Using ESP32-CAM

## Objective

Use an AI Thinker ESP32-CAM module to capture live video and a Python program to recognize a hand and count raised fingers (0–5).

## Hardware and software

- AI Thinker ESP32-CAM, USB-to-serial adapter or ESP32-CAM-MB programmer, and a data-capable USB cable
- Computer and Wi-Fi network shared with the ESP32-CAM
- Arduino IDE 2.3.5 (as specified by the course)
- Espressif ESP32 boards package 2.0.17 (as specified by the course)
- Python 3.10 or 3.11 recommended, OpenCV, MediaPipe

## Step 1: Configure Arduino IDE

1. Download Arduino IDE 2.3.5 from https://github.com/arduino/arduino-ide/releases/tag/2.3.5 .
2. Open **File → Preferences** and add the following under **Additional Boards Manager URLs**:
   `https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json`
3. Open **Tools → Board → Boards Manager**, search for `esp32`, and install **esp32 by Espressif Systems** version **2.0.17**.
4. Select **AI Thinker ESP32-CAM** in the board selector. Select the serial COM port corresponding to your programming adapter.

## Step 2: Flash the ESP32-CAM camera server

1. Arduino IDE → **File → Examples → ESP32 → Camera → CameraWebServer** (after installing the board package).
2. In the sketch, uncomment `#define CAMERA_MODEL_AI_THINKER` and ensure the other `CAMERA_MODEL_...` lines are commented out.
3. Enter your own Wi-Fi SSID and password in the sketch; **do not commit the Wi-Fi password to GitHub**.
4. If using a basic USB-to-serial adapter, connect **5V→5V, GND→GND, TX(adapter)→U0R, RX(adapter)→U0T**; pull **GPIO0 to GND while flashing**. Use a reliable 5V supply and confirm the adapter's logic level is safe for ESP32 pins. An ESP32-CAM-MB programmer may manage flashing automatically.
5. Click **Upload**. With a manual adapter, remove GPIO0–GND and reset after upload. Open **Serial Monitor** at **115200 baud** and locate the camera's IP address.
6. On the same Wi-Fi network, open `http://YOUR_ESP32_IP` in a browser, then select **Start Stream**. The example serves MJPEG on port **81**.

## Step 3: Install Python dependencies

In the `Assignment_1` folder, run:

```bash
python -m pip install -r requirements.txt
```

## Step 4: Run finger detection

Replace the sample IP with the one shown in Arduino Serial Monitor:

```bash
python finger_count.py --ip 192.168.1.100
```

Hold your hand in front of the ESP32-CAM. A window displays the video, hand landmarks, and a finger count. Press **q** to close it.

The program reads the ESP32-CAM MJPEG stream using `cv2.VideoCapture("http://ESP32_IP:81/stream")`; it does **not** use the laptop's built-in webcam. MediaPipe identifies 21 hand landmarks, and the script estimates which fingers are extended by comparing fingertip positions with finger-joint positions (and thumb-tip position with the thumb joint). This simple technique may miscount when the hand is rotated, partially hidden, or poorly lit.

## Video Demonstration

This video demonstrates the finger-counting detection system for Assignment 1 using Python, OpenCV, and MediaPipe.

### Finger Counting Video

**[▶ Watch Finger Counting Demo](videos/finger_count_demo.mp4)**

The project uses MediaPipe to detect 21 hand landmarks and count raised fingers.

### Results

The finger-counting demonstration is provided in the video above. The system processes camera frames, detects hand landmarks, and displays the finger count in real time.

### Technologies Used

- Python 3.11
- OpenCV
- MediaPipe 0.10.11
- ESP32-CAM (camera hardware for the assignment)

## Troubleshooting

- **No COM port:** use a data-capable USB cable, install the programmer's driver, and reconnect.
- **Upload fails:** check GPIO0-to-GND during flashing; verify wiring, reset and 5V power.
- **No IP address:** verify SSID, password, Wi-Fi signal and network type (ESP32 typically uses 2.4 GHz Wi-Fi).
- **Cannot open stream:** confirm the browser camera view works, the IP is correct, and your computer is on the same network.
- **Python error:** use Python 3.10/3.11 in a clean virtual environment and reinstall requirements.
- **Poor counting accuracy:** use good lighting, show the full hand and spread your fingers clearly.

## References

- Arduino IDE releases: https://github.com/arduino/arduino-ide/releases
- Espressif Arduino-ESP32: https://github.com/espressif/arduino-esp32
- MediaPipe Hands documentation: https://github.com/google-ai-edge/mediapipe/blob/master/docs/solutions/hands.md
