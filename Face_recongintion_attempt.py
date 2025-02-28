import qi
import cv2

def on_face_detected(value):
    face_detected = value
    if face_detected:
        print("Hola, Como te llamas")
        nombre = raw_input()
        guardar_nombre(nombre)

def guardar_nombre(nombre):
    with open("nombres.txt", "a") as file:
        file.write(nombre + "\n")
    print("Nombre guardado con exito: ", nombre)

session = qi.Session()
try:
    session.connect("tcp://192.168.0.104:9559")
except Exception as e:
    print("No se pudo conectar con Pepper:", e)
    exit(1)

memory = session.service("ALMemory")
memory.subscribeToEvent("FaceDetected", "on_face_detected")

video_service = session.service("ALVideoDevice")
video_service.subscribe("python_client", 2, 11, 5)

try:
    while True:
        image = video_service.getImageRemote("python_client")
        img_width = image[0]
        img_height = image[1]
        array = image[6]
        
        frame = cv2.cv.CreateImageHeader((img_width, img_height), cv2.cv.IPL_DEPTH_8U, 3)
        cv2.cv.SetData(frame, array)
        
        cv2.imshow("Pepper's Camera", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    video_service.unsubscribe("python_client")
    session.close()
    cv2.destroyAllWindows()
