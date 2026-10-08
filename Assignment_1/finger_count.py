"""Finger-count detection from an ESP32-CAM MJPEG stream.

Uses MediaPipe Hands to estimate the number of extended fingers.
Run with: python finger_count.py --ip 192.168.1.100
"""
import argparse
import math
import time

import cv2
import mediapipe as mp


def angle(a, b, c):
    """Return angle ABC in degrees for normalized MediaPipe landmarks."""
    ba = (a.x - b.x, a.y - b.y)
    bc = (c.x - b.x, c.y - b.y)
    magnitude = math.hypot(*ba) * math.hypot(*bc)
    if magnitude < 1e-8:
        return 0.0
    cosine = max(-1.0, min(1.0, (ba[0] * bc[0] + ba[1] * bc[1]) / magnitude))
    return math.degrees(math.acos(cosine))


def distance(a, b):
    return math.hypot(a.x - b.x, a.y - b.y)


def count_fingers(points):
    """Count visible, extended fingers on one hand (heuristic)."""
    finger_joints = [(5, 6, 8), (9, 10, 12), (13, 14, 16), (17, 18, 20)]
    total = sum(
        angle(points[mcp], points[pip], points[tip]) > 155
        and distance(points[tip], points[0]) > distance(points[pip], points[0])
        for mcp, pip, tip in finger_joints
    )
    thumb_extended = (
        angle(points[2], points[3], points[4]) > 150
        and distance(points[4], points[17]) > distance(points[3], points[17]) * 1.12
    )
    return total + int(thumb_extended)


def main():
    parser = argparse.ArgumentParser(description="Count fingers using ESP32-CAM video")
    parser.add_argument("--ip", required=True, help="ESP32-CAM IP address shown in Arduino Serial Monitor")
    args = parser.parse_args()
    stream_url = f"http://{args.ip}:81/stream"
    print(f"Opening {stream_url}")
    cap = cv2.VideoCapture(stream_url)
    if not cap.isOpened():
        raise SystemExit("Unable to connect. Check Wi-Fi, IP, camera server and port 81.")

    hands_api = mp.solutions.hands
    draw = mp.solutions.drawing_utils
    failed_frames = 0
    with hands_api.Hands(max_num_hands=1, min_detection_confidence=0.6,
                         min_tracking_confidence=0.5) as hands:
        while True:
            ok, frame = cap.read()
            if not ok:
                failed_frames += 1
                if failed_frames >= 30:
                    print("Camera stream stopped. Verify ESP32-CAM network and power.")
                    break
                time.sleep(0.1)
                continue
            failed_frames = 0
            frame = cv2.flip(frame, 1)
            result = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            finger_count = 0
            if result.multi_hand_landmarks:
                landmarks = result.multi_hand_landmarks[0]
                finger_count = count_fingers(landmarks.landmark)
                draw.draw_landmarks(frame, landmarks, hands_api.HAND_CONNECTIONS)
                label = f"Finger Count: {finger_count}"
            else:
                label = "No hand detected"
            cv2.putText(frame, label, (20, 45), cv2.FONT_HERSHEY_SIMPLEX,
                        0.9, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.imshow("Assignment 1 - ESP32-CAM Finger Count", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
