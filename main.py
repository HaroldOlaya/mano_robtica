import cv2
import numpy as np
import mediapipe as mp
import socket
import time
def contar(dedos):
    contador=0
    for dedo in dedos:
        contador=contador+dedo

    return contador
def enviar (valor):

    client_socket.send((valor+"\n").encode())

mp_drawing= mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
cap=cv2.VideoCapture(0)
esp32_ip = "192.168.137.157"
esp32_port = 80
# Valor que deseas enviar


# Crear un socket TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar al ESP32
client_socket.connect((esp32_ip, esp32_port))


with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5)as hands:
    while True:

        ret,frame=cap.read()
        if ret == False:
            break

        height,width,_=frame.shape
        frame=cv2.flip(frame,1)
        frame_rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        resultado=hands.process(frame_rgb)
        #print(resultado.multi_handedness)
        #print(resultado.multi_hand_landmarks)#ubicacion de los 21 puntos en la mano

        if resultado.multi_hand_landmarks is not None:

        #--- dibujar los puntos en la mano
            for hand_landmarks in resultado.multi_hand_landmarks:
                xpulgar = int(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x * width)
                xpulgar2 = int(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].x * width)
                yindice = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * height)
                yindice2 = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].y * height)
                ycorazon = int(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y * height)
                ycorazon2 = int(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP].y * height)
                yanular = int(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y * height)
                yanular2 = int(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP].y * height)
                ymeñique = int(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y * height)
                ymeñique2 = int(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_DIP].y * height)
                #print(puntox,xpulgar,xindice,xcorazon)
                #print(yindice,yindice2)
                dedos=[0,0,0,0,0]

                if yindice > yindice2:
                    dedos[3]=2
                if xpulgar > xpulgar2:
                    dedos[4] = 1

                if ycorazon > ycorazon2:
                    dedos[2] = 4

                if yanular > yanular2:
                    dedos[1] = 8

                if ymeñique > ymeñique2:
                    dedos[0] = 16
                valor=contar(dedos)
                valor=str(valor)
                for j in range(1, 5):
                    enviar(valor)
                print(valor)
                mp_drawing.draw_landmarks(

                    frame,hand_landmarks,mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec((255,0,0),thickness=2,circle_radius=3),
                    mp_drawing.DrawingSpec((0,0,0),thickness=2)
                )

        cv2.imshow("Camara activa", frame)
        if cv2.waitKey(1) == ord('q'):
            client_socket.close()
            break


cap.release()
cv2.destroyAllWindows()

