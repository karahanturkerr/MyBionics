import cv2
import numpy as np

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)



while True:

    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    height, width, _ = frame.shape

    cx = int(width / 2)
    cy = int(height / 2)

    pixel_center = hsv_frame[cy, cx]
    hue_value = pixel_center[0]


    #blue
    lower_blue = np.array([100, 150, 0])
    upper_blue = np.array([140, 255, 255])
    blue_mask = cv2.inRange(hsv_frame, lower_blue, upper_blue)
    #blue = cv2.bitwise_and(frame, frame, mask = blue_mask)

    # Yesil renk maskesi
    lower_green = np.array([40, 50, 50])
    upper_green = np.array([80, 255, 255])
    green_mask = cv2.inRange(hsv_frame, lower_green, upper_green)
    #green = cv2.bitwise_and(frame, frame, mask = green_mask)

    # Kırmızı renk maskesi
    lower_red1 = np.array([0, 150, 0])
    upper_red1 = np.array([10, 255, 255])
    red_mask1 = cv2.inRange(hsv_frame, lower_red1, upper_red1)

    lower_red2 = np.array([170, 150, 0])
    upper_red2 = np.array([180, 255, 255])
    red_mask2 = cv2.inRange(hsv_frame, lower_red2, upper_red2)

    red_mask = cv2.bitwise_or(red_mask1, red_mask2)
    #red = cv2.bitwise_and(frame, frame, mask = red_mask)

    mask_combined = cv2.bitwise_or(blue_mask, green_mask)
    mask_combined = cv2.bitwise_or(mask_combined, red_mask1)
    mask_combined = cv2.bitwise_or(mask_combined, red_mask2)

    # Renkli bölgeleri görselleştirme
    blue = cv2.bitwise_and(frame, frame, mask=blue_mask)
    green = cv2.bitwise_and(frame, frame, mask=green_mask)
    red = cv2.bitwise_and(frame, frame, mask=red_mask1)
    red = cv2.bitwise_and(red, red, mask=red_mask2)
    combined = cv2.bitwise_and(frame, frame, mask=mask_combined)


    cv2.imshow("webcam", frame)
    cv2.imshow("Combined", combined)
    # cv2.imshow("blue", blue)
    # cv2.imshow("green", green)
    # cv2.imshow("red", red)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
