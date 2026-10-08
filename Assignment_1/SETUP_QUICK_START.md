# Quick start for the day you borrow the ESP32-CAM

1. Connect the ESP32-CAM with a compatible USB programmer and data USB cable.
2. In Arduino IDE 2.3.5, select AI Thinker ESP32-CAM (Espressif core 2.0.17) and the detected COM port.
3. Open **File > Examples > ESP32 > Camera > CameraWebServer**, select `CAMERA_MODEL_AI_THINKER` and enter your own **2.4 GHz** Wi-Fi credentials. Do not upload Wi-Fi passwords to GitHub.
4. Flash the sketch. For manual USB-serial programming: GPIO0 to GND during flashing, disconnect GPIO0-GND after uploading, then reset.
5. Open Serial Monitor at 115200 baud; note the actual IP address. Confirm `http://YOUR_IP` shows a working camera stream.
6. On a Windows computer on the same Wi-Fi, open Command Prompt inside `Assignment_1` and run:

   ```bat
   py -3.11 -m venv myenv
   myenv\Scripts\activate.bat
   python -m pip install -r requirements.txt
   python finger_count.py --ip YOUR_IP
   ```

7. Take screenshots with one, three and five fingers. Put them in `screenshots/`; update the status and observations in `README.md`.
8. Push the updates to GitHub and submit the repository link.
