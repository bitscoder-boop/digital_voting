import sqlite3
import face_recognition
import cv2
from PIL import Image
from six import StringIO
import face_recognition
from datetime import datetime
import requests
import sys

url = 'http://127.0.0.1:8000/send_transcation'
while True:
    qr_file = input("Enter filename contaning qr code: ")
    receiver_id = input("Enter receiver_id: ")
    im = cv2.imread(qr_file)
    detector = cv2.QRCodeDetector()
    # detect and decode
    decoded_qr, _, _ = detector.detectAndDecode(im)


    face_sets = set()
    name_sets = []
    con = sqlite3.connect('./digital_voting.db')

    cur = con.cursor()
    record = [ i for i in cur.execute(f'SELECT * FROM voter_tbl where secret_key == "{decoded_qr}"')]
    check_qr = [f'{i[6]}' for i in record]
    photo = [f'{i[4]}' for i in record]
    print(check_qr)
    print(photo)
    if not check_qr[0] or not photo[0]:
        print("QR doesnot match")
        sys.exit()
    known_image = face_recognition.load_image_file('images/' + photo[0])
    known_encoding = face_recognition.face_encodings(known_image)[0]


    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()


    final = []


    while True:
        today = datetime.today()
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        img_small = cv2.resize(frame, (0,0), fx=0.25, fy=0.25)
        img_small = cv2.flip(img_small, 1)
        rgb_small_frame = img_small[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_small_frame)
        encodeCurFrame = face_recognition.face_encodings(rgb_small_frame, face_locations)
        
        for encodeFace, faceLoc in zip(encodeCurFrame, face_locations):
            matches = face_recognition.compare_faces([known_encoding], encodeFace, tolerance=0.4)
            print(matches)
            if matches[0] == True:
                name = 'current_image.png'
                current_frame = cv2.imwrite(name, rgb_small_frame)
                params = (
                        ('receiver_id', receiver_id),
                        )
                files = {'current_image': (f'{name}', open(f'{name}', 'rb')),
                        'qr_code': (f'{qr_file}', open(f'{qr_file}', 'rb'))}
                # start voting:
                x = requests.post(url, params=params, files=files)
                print(x.text)
                break
            
        cv2.imshow("WebCam", img_small)
        if cv2.waitKey(5) == ord('q'):
            break

cv2.destroyAllWindows()
