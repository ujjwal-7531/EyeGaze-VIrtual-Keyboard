# Eye Gaze Controlled Virtual Keyboard

A computer vision based virtual keyboard that allows users to type using eye gaze direction and blinking.  
This project is designed for hands-free interaction and accessibility focused applications.

---

## Features

- Eye gaze based navigation (Left, Centre, Right)
- Blink to confirm key selection
- Three virtual keyboards:
  - Left: A–M and symbols
  - Centre: Numbers and operators
  - Right: N–Z and symbols
- Live writing board for typed text
- Visual blink loading bar for feedback
- Audio feedback for key and keyboard selection
- Multiple windows:
  - Face frame
  - Virtual keyboard
  - Writing board

---

## How It Works

### Face and Eye Detection
Uses dlib’s 68 facial landmark predictor to detect facial features and accurately locate eye regions in real time.

### Gaze Estimation
Eye gaze direction is determined by comparing white pixel distribution between the left and right halves of the eye region.  
This allows classification into left, centre, or right gaze.

### Blink Detection
Blinking is detected using Eye Aspect Ratio (EAR).  
A sustained blink is used as a confirmation signal to select characters.

### Virtual Keyboard Logic
The keyboard automatically cycles through keys.  
The currently active key is highlighted, and a blink selects it.

---

## Tech Stack

- Python
- OpenCV
- dlib
- NumPy
- pygame (audio feedback)

---

## Use Cases

- Assistive typing for users with motor disabilities
- Hands-free human-computer interaction

---

## Setup Instructions

1. Clone the repository
2. Install dependencies
3. Download `shape_predictor_68_face_landmarks.dat`
4. Run the main Python script

Ensure your webcam is connected before running the program.

---

## Disclaimer

This project requires good lighting conditions for accurate eye tracking as the gaze ration are according to my camera.
