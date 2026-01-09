import cv2
import dlib
import mediapipe as mp

import numpy as np
import math 

import pygame
import time

# Constants
font=cv2.FONT_HERSHEY_PLAIN
cap = cv2.VideoCapture(0) #captures video from webcam

# Audio Setup
pygame.mixer.init()
select = pygame.mixer.Sound("sounds/select.wav")
lsound = pygame.mixer.Sound("sounds/left.wav")
rsound = pygame.mixer.Sound("sounds/right.wav")
csound = pygame.mixer.Sound("sounds/centre.wav")

# Writing Board (white background)
board = np.zeros((270, 1800), dtype=np.uint8)
board[:] = 255

# Using the dlib library to use the 68 facial landmarks
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("model/shape_predictor_68_face_landmarks.dat")

# Virtual Keyboard
keyboard = np.zeros((600, 1050, 3), dtype=np.uint8) # height, width, color-channels    150, 210
# LEFT keyboard keys
keySet1 = {
     0:"A",  1:"B",  2:"C",  3:"D",  4:"E",
     5:"F",  6:"G",  7:"H",  8:"I",  9:"<",
    10:"J", 11:"K", 12:"L", 13:"M", 14:"_",
    15:".", 16:",", 17:"?", 18:"!", 19:"<-"
}

# RIGHT keyboard keys
keySet2 = {
     0:"N",  1:"O",  2:"P",  3:"Q",  4:"R",
     5:"S",  6:"T",  7:"U",  8:"V",  9:"<",
    10:"W", 11:"X", 12:"Y", 13:"Z", 14:"_",
    15:"(", 16:")", 17:"'", 18:"#", 19:"<-"
}

#CENTRE keyboard keys
keySet3 = {
     0:"0",  1:"1",  2:"2",  3:"3",  4:"[x]",
     5:"4",  6:"5",  7:"6",  8:"7",  9:"<",
    10:"8", 11:"9", 12:".", 13:"=", 14:"_",
    15:"+", 16:"-", 17:"/", 18:"*", 19:"<-"
}

# Menu Board
def draw_menu():
    keyboard[:] = (0, 0, 0)   # black background

    color = (58, 125, 6)
    thickness = 3

    height = 600
    width = 1050
    regions = 3
    region_width = width // regions

    labels = ["LEFT", "CENTRE", "RIGHT"]

    # Outer border
    cv2.rectangle(
        keyboard,
        (0, 0),
        (width - 1, height - 1),
        color,
        thickness
    )

    # Vertical separators
    for i in range(1, regions):
        x = i * region_width
        cv2.line(
            keyboard,
            (x, 0),
            (x, height),
            color,
            thickness
        )

    # Text settings
    fontScale = 3
    fontThickness = 3
    for i in range(regions):
        text = labels[i]

        textSize = cv2.getTextSize(text, font, fontScale, fontThickness)[0]
        textWidth, textHeight = textSize

        textx = i * region_width + int((region_width - textWidth) / 2)
        texty = int((height + textHeight) / 2)

        cv2.putText(
            keyboard,
            text,
            (textx, texty),
            font,
            fontScale,
            color,
            fontThickness
        )

# Function for drawing borders and texts on the keyboard
def drawLetters(letterIndex, letter, gaze):
    cols = 5
    keyWidth = 210      
    keyHeight = 150
    thickness = 3

    row = letterIndex // cols
    col = letterIndex % cols

    x = col * keyWidth
    y = row * keyHeight

    if gaze:
        cv2.rectangle(
            keyboard,
            (x + thickness, y + thickness),
            (x + keyWidth - thickness, y + keyHeight - thickness),
            (255, 255, 255),
            -1
        )
    else:
        cv2.rectangle(
            keyboard,
            (x + thickness, y + thickness),
            (x + keyWidth - thickness, y + keyHeight - thickness),
            (0, 0, 0),
            -1
        )

    cv2.rectangle(
        keyboard,
        (x, y),
        (x + keyWidth, y + keyHeight),
        (255, 255, 255),
        thickness
    )

    font = cv2.FONT_HERSHEY_PLAIN
    fontScale = 10
    fontThickness = 4

    textSize = cv2.getTextSize(letter, font, fontScale, fontThickness)[0]
    textx = int((keyWidth - textSize[0]) / 2) + x
    texty = int((keyHeight + textSize[1]) / 2) + y

    cv2.putText(
        keyboard,
        letter,
        (textx, texty),
        font,
        fontScale,
        (58, 125, 6),
        fontThickness
    )

# Function to find midpoint
def midpoint(p1, p2):
    return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)

# Function to calculate eye blink ratio
def getEyeBlinkRatio(ep, facial_landmarks): #ep is the landmark points of eye
    
    # horizontal line on eye
    leftPoint = (facial_landmarks.part(ep[0]).x, facial_landmarks.part(ep[0]).y)
    rightPoint = (facial_landmarks.part(ep[3]).x, facial_landmarks.part(ep[3]).y)
    # horizontalLine = cv2.line(frame, leftPoint, rightPoint, (0, 255, 0), 1)

    # vertical line on eye
    topPoint = midpoint(facial_landmarks.part(ep[1]), facial_landmarks.part(ep[2]))
    bottomPoint = midpoint(facial_landmarks.part(ep[4]), facial_landmarks.part(ep[5]))
    # verticalLine = cv2.line(frame, topPoint, bottomPoint, (0, 255, 0), 1)

    verticalLinelength = math.hypot(topPoint[0]-bottomPoint[0], topPoint[1]-bottomPoint[1])
    horizontalLinelength = math.hypot(leftPoint[0]-rightPoint[0], leftPoint[1]-rightPoint[1])

    ratio = horizontalLinelength/verticalLinelength
    return ratio

#function to calculate the get the gaze ration
def getGazeRatio(eyePoints, facialLandmarks):
    eyeRegion = np.array([(facialLandmarks.part(eyePoints[0]).x, facialLandmarks.part(eyePoints[0]).y),
                            (facialLandmarks.part(eyePoints[1]).x, facialLandmarks.part(eyePoints[1]).y),
                            (facialLandmarks.part(eyePoints[2]).x, facialLandmarks.part(eyePoints[2]).y),
                            (facialLandmarks.part(eyePoints[3]).x, facialLandmarks.part(eyePoints[3]).y),
                            (facialLandmarks.part(eyePoints[4]).x, facialLandmarks.part(eyePoints[4]).y),
                            (facialLandmarks.part(eyePoints[5]).x, facialLandmarks.part(eyePoints[5]).y)
                            ], np.int32)
        
    # Eye region border
    cv2.polylines(frame, [eyeRegion], True, (0,0,255), 1)

    # Eye region Frame
    minX = np.min(eyeRegion[:, 0])
    maxX = np.max(eyeRegion[:, 0])
    minY = np.min(eyeRegion[:, 1])
    maxY = np.max(eyeRegion[:, 1])
    eye = frame[minY: maxY, minX: maxX]
    
    # mask frame
    ht, wdt, _ = frame.shape
    mask = np.zeros((ht, wdt), np.uint8)
    cv2.polylines(mask, [eyeRegion], True, 255, 2)
    cv2.fillPoly(mask, [eyeRegion], 255)
    eye=cv2.bitwise_and(gray, gray, mask=mask)
    
    gray_eye = eye[minY: maxY, minX: maxX]
    _, thresholdEye = cv2.threshold(gray_eye, 70, 255, cv2.THRESH_BINARY)
    
    height, width = thresholdEye.shape
    
    leftSideThreshold = thresholdEye[0: height, 0: int(width/2)]
    leftSideWhitePixelCOunt = cv2.countNonZero(leftSideThreshold)
    
    rightSideThreshold = thresholdEye[0: height, int(width/2): width]
    rightSidePixelCOunt= cv2.countNonZero(rightSideThreshold)

    if rightSidePixelCOunt == 0:
        rightSidePixelCOunt = 1
    gaze_ratio = leftSideWhitePixelCOunt / rightSidePixelCOunt
    
    return gaze_ratio



# Iterators and Counters
framesCount = 0
blinkingFramesCount = 0

letterSelectorCount = 5 #frames_active_letter
framesToBlink = 5

letterIndex = 0

text = ""
selectedKeyboard = "left"
lastSelectedKeyboard = "left"
menuSelected = True
keyboardSelectionFramesCount = 0

exitToBoard = False
while True:
    if exitToBoard:
        cv2.imshow("Board", board)
        key = cv2.waitKey(1)
        if key == 27:   # ESC to fully exit
            break
        continue
    
    _, frame = cap.read()
    # _, frame = cap.read()

    SCALE = 0.75   # 75% of original size
    frame = cv2.resize(frame, None, fx=SCALE, fy=SCALE)

    rows, cols, _ = frame.shape
    framesCount+=1
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # White space for loading bar
    BAR_HEIGHT = 8
    BAR_MARGIN = 12        # distance from bottom
    BAR_COLOR = (0, 165, 255)   # orange (BGR)
    BAR_BG_COLOR = (230, 230, 230)  # light background
    BORDER_COLOR = (0, 0, 0)
    BORDER_THICKNESS = 1
    y1 = rows - BAR_MARGIN - BAR_HEIGHT
    y2 = rows - BAR_MARGIN
    frame[y1:y2, 0:cols] = BAR_BG_COLOR
    
    if menuSelected == True:
        draw_menu()
        
    # Keyboard selection
    if selectedKeyboard == "left":
        keySet = keySet1
    elif selectedKeyboard == "centre":
        keySet = keySet3
    else:
        keySet = keySet2

    selectedLetter = keySet[letterIndex]
    
    # Face detection
    faces = detector(gray) #detects face
    for face in faces:
        landmarks = predictor(gray, face) #detects unique 68 trained points on face
        
        # Gaze-Ratio marking on face frame
        leftEyeGazeRatio = getGazeRatio([36, 37, 38, 39, 40, 41], landmarks)
        rightEyeGazeRatio = getGazeRatio([42, 43, 44, 45, 46, 47], landmarks)
        gazeRatio = (rightEyeGazeRatio + leftEyeGazeRatio) / 2
        cv2.putText(frame, "GR: " + str(round(gazeRatio, 5)), (20, 40), cv2.FONT_HERSHEY_TRIPLEX, 1.3, (60,20,220), 2)

        
        # Direction marking on face frame
        if(3.5<=gazeRatio and gazeRatio<=150):
            cv2.putText(frame, "Left", (20, 180), cv2.FONT_HERSHEY_TRIPLEX, 1.3, (255, 0, 255),2)
        elif gazeRatio<1:
            cv2.putText(frame, "Right", (20, 180), cv2.FONT_HERSHEY_TRIPLEX, 1.3, (0, 255, 255), 2)
        else:
            cv2.putText(frame, "Center", (20, 180), cv2.FONT_HERSHEY_TRIPLEX, 1.3, (255, 255, 0), 2)

        # Blink detection
        leftEyeBlinkRatio = getEyeBlinkRatio([36, 37, 38, 39, 40, 41], landmarks) # left eye
        rightEyeBlinkRatio = getEyeBlinkRatio([42, 43, 44, 45, 46, 47], landmarks) # right eye
        blinkRatio = (leftEyeBlinkRatio + rightEyeBlinkRatio) / 2
        if(blinkRatio > 4.7):
            cv2.putText(frame, "Blinking...", (20, 310), cv2.FONT_HERSHEY_TRIPLEX, 1.3, (0, 128, 255), 2)
        
        
        
        # Eye region landmarks
        facialLandmarks = predictor(gray, face)
        leftEyeRegion = np.array([(facialLandmarks.part(36).x, facialLandmarks.part(36).y),
                                    (facialLandmarks.part(37).x, facialLandmarks.part(37).y),
                                    (facialLandmarks.part(38).x, facialLandmarks.part(38).y),
                                    (facialLandmarks.part(39).x, facialLandmarks.part(39).y),
                                    (facialLandmarks.part(40).x, facialLandmarks.part(40).y),
                                    (facialLandmarks.part(41).x, facialLandmarks.part(41).y)
                                    ], np.int32)
        rightEyeRegion = np.array([(facialLandmarks.part(42).x, facialLandmarks.part(42).y),
                                    (facialLandmarks.part(43).x, facialLandmarks.part(43).y),
                                    (facialLandmarks.part(44).x, facialLandmarks.part(44).y),
                                    (facialLandmarks.part(45).x, facialLandmarks.part(45).y),
                                    (facialLandmarks.part(46).x, facialLandmarks.part(46).y),
                                    (facialLandmarks.part(47).x, facialLandmarks.part(47).y)
                                    ], np.int32)
        cv2.polylines(frame, [leftEyeRegion], True, (43,214,43), 1)
        cv2.polylines(frame, [rightEyeRegion], True, (43,214,43), 1)
        
        if menuSelected is True:
            # Blink detection for menu selection
            if(3.5<=gazeRatio and gazeRatio<=150):
                # cv2.putText(frame, "Left", (50, 250), cv2.FONT_HERSHEY_TRIPLEX, 2, (255,0,255), 2)
                selectedKeyboard = "left"
                keyboardSelectionFramesCount += 1
                
                if keyboardSelectionFramesCount == 25:
                    menuSelected = False
                    lsound.play()
                    time.sleep(1)
                    framesCount = 0
                    keyboardSelectionFramesCount = 0

                if lastSelectedKeyboard != selectedKeyboard:
                    lastSelectedKeyboard = selectedKeyboard
                    keyboardSelectionFramesCount = 0
                    
            elif gazeRatio<1:
                # cv2.putText(frame, "Right", (50, 250), cv2.FONT_HERSHEY_TRIPLEX, 2, (0, 255, 255), 2) 
                selectedKeyboard="right"
                keyboardSelectionFramesCount += 1
                
                if keyboardSelectionFramesCount == 25: #limmit to select kb
                    menuSelected = False
                    rsound.play()
                    time.sleep(1)
                    framesCount = 0
                    keyboardSelectionFramesCount = 0
                    
                if lastSelectedKeyboard != selectedKeyboard:
                    lastSelectedKeyboard = selectedKeyboard
                    keyboardSelectionFramesCount = 0
                    
            else:
                # cv2.putText(frame, "Center", (50, 250), cv2.FONT_HERSHEY_TRIPLEX, 2, (255, 255, 0), 2)
                selectedKeyboard="centre"
                keyboardSelectionFramesCount += 1
                
                if keyboardSelectionFramesCount == 25: #limmit to select kb
                    menuSelected = False
                    csound.play()
                    time.sleep(1)
                    framesCount = 0
                    keyboardSelectionFramesCount = 0
                    
                if lastSelectedKeyboard != selectedKeyboard:
                    lastSelectedKeyboard = selectedKeyboard
                    keyboardSelectionFramesCount = 0
            
        else:
            if(blinkRatio > 4.7):
                cv2.putText(frame, "Blinking...", (20, 310), cv2.FONT_HERSHEY_TRIPLEX, 1.3, (0, 128, 255), 2)

                cv2.polylines(frame, [leftEyeRegion], True, (0,0,240), 1)
                cv2.polylines(frame, [rightEyeRegion], True, (0,0,240), 1)
                # print(selectedLetter)
                blinkingFramesCount += 1
                framesCount -= 1

                # Typing on board
                if blinkingFramesCount == framesToBlink:
                    if(selectedLetter != "<" and selectedLetter != "<-" and selectedLetter != "_" and selectedLetter != "[x]"):
                        text += selectedLetter

                    elif selectedLetter == "<-":
                        draw_menu()
                        menuSelected = True
                        
                    elif selectedLetter == "<":
                        board[:] = 255          # clear board (white)
                        text = text[:-1]
                        
                    elif selectedLetter == "_":
                        text += " "
                    elif selectedLetter == "[x]":
                        cap.release()
                        cv2.destroyWindow("Frame")
                        cv2.destroyWindow("Virtual Keyboard")
                        exitToBoard = True

                    select.play()
                    
            else:
                blinkingFramesCount = 0
                    
    # Display letters on the keyboard   
    TOTAL_KEYS = 20   # 5 columns × 4 rows
    if menuSelected == False:
        if framesCount == letterSelectorCount:
            letterIndex += 1
            framesCount = 0
        if letterIndex == TOTAL_KEYS:
            letterIndex = 0
        for i in range(TOTAL_KEYS):
            if i == letterIndex:
                gaze = True
            else:
                gaze = False
            drawLetters(i, keySet[i], gaze)
    cv2.putText(board, text, (10, 50), font, 3, 0, 3)

    
    # Blinking loading bar
    percentageBlinking = blinkingFramesCount / framesToBlink
    percentageBlinking = min(percentageBlinking, 1.0)  # safety clamp
    loadingX = int(cols * percentageBlinking)
    cv2.rectangle(frame,(0, y1),(loadingX, y2),BAR_COLOR,-1)

    # --- Optional border ---
    # cv2.rectangle(frame,(0, y1),(cols, y2),BORDER_COLOR,BORDER_THICKNESS)
        
    if not exitToBoard:
        cv2.imshow("Frame", frame)
        cv2.imshow("Virtual Keyboard", keyboard)
        # Position windows (once)
        cv2.moveWindow("Frame", 1450, 0)
        cv2.moveWindow("Virtual Keyboard", 380, 0)
        

    cv2.imshow("Board", board)
    cv2.moveWindow("Board", 0, 820)
    
    key = cv2.waitKey(1)
    if key == 27:
        break
    
cap.release()
cv2.destroyWindow("Board")