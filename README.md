### Eye Gaze Controlled Virtual Keyboard

A computer vision based virtual keyboard that allows users to **type using eye gaze direction and blinking**, designed to assist hands-free interaction and accessibility use cases.

This project uses **facial landmark detection**, **eye gaze estimation**, and **blink detection** to enable text input without any physical keyboard.

---

## 🚀 Features

- 👀 **Eye gaze based navigation**
  - Look **left**, **centre**, or **right** to select keyboard region.
- 👁️ **Blink to select**
  - Blink to confirm a character.
- ⌨️ **Three virtual keyboards**
  - Left (A–M + symbols)
  - Centre (Numbers & operators)
  - Right (N–Z + symbols)
- 🧾 **Live writing board**
  - Typed text appears on a white board
- 📊 **Blink loading bar**
  - Visual feedback while blinking
- 🔊 **Audio feedback**
  - Sounds on letter selection and keyboard switching
- 🪟 **Multiple windows**
  - Face frame
  - Virtual keyboard
  - Writing board

---

## 🧠 How It Works

### 1️⃣ Face & Eye Detection
- Uses **dlib’s 68 facial landmarks** to locate eyes
- Tracks eye regions in real time

### 2️⃣ Gaze Estimation
- Compares white pixel distribution in left vs right eye
- Determines gaze direction:
  - Left
  - Centre
  - Right

### 3️⃣ Blink Detection
- Eye Aspect Ratio (EAR) based blink detection
- Sustained blink confirms key selection

### 4️⃣ Virtual Keyboard Logic
- Keyboard auto-cycles through keys
- Current key is highlighted
- Blink selects the highlighted key

---

## 🛠️ Tech Stack

- **Python**
- **OpenCV**
- **dlib**
- **NumPy**
- **pygame** (for audio feedback)

---

