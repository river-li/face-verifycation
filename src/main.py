import sys
from home import Ui_home
from choose_function import Ui_cam_Dialog
from PyQt5.QtWidgets import QApplication,QMainWindow,QDialog,QMessageBox
from PyQt5 import QtGui
import cv2
import numpy as np
from PIL import Image
import os
import hashlib
import WDT
import RandomWork

cam_number = 0
# 0 stands for the camera on laptop
username = []
user_id = []
flag = 0

class home_face_verify(QMainWindow,Ui_home):
    def __init__(self):
        super(home_face_verify,self).__init__()
        self.setupUi(self)

class cam_face_verify(QDialog,Ui_cam_Dialog):

    def __init__(self):
        super(cam_face_verify,self).__init__()
        self.setupUi(self)
        with open('local.log','r') as f:
            l = f.readlines()
            for i in l:
                username.append(i.replace('\n',''))
                user_id.append(str(l.index(i)))
        self.comboBox_id.addItems(user_id)
        self.comboBox_id.addItem(str(len(user_id)))
        self.comboBox_username.addItems(username)
        self.record_button.clicked.connect(self.build_and_train)
        self.verify_button.clicked.connect(self.verify)



    def build_and_train(self):
        add_string = "是否确认添加用户" + self.LineEdit_username.text()+ "\n用户ID："+ str(self.comboBox_id.currentIndex())

        Message = QMessageBox()
        reply = Message.question(self,"确认",str(add_string),QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
        if reply==QMessageBox.Yes:
            self.train(self.LineEdit_username.text(),self.comboBox_id.currentIndex())



    def train(self,user,id):
        if id <= len(user_id):
            if id==len(user_id):
                user_id.append(len(user_id))
                username.append(user)
                self.comboBox_id.addItem(str(len(user_id)))
                self.comboBox_username.addItem(user)

            wd = WDT.Watch_Dog(5)

            rw = RandomWork.RandomWork()
            rw.start()
            username[id]=user
            cam = cv2.VideoCapture(cam_number)
            cam.set(3, 640)  # set video width
            cam.set(4, 480)  # set video height

            face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            recognizer = cv2.face.LBPHFaceRecognizer_create()

            count = 0
            while True:
                if wd.time_out():
                    break


                ret, img = cam.read()
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                self.image = img

                showImage = QtGui.QImage(img.data, img.shape[1], img.shape[0], QtGui.QImage.Format_RGB888)
                self.cam_label.setPixmap(QtGui.QPixmap.fromImage(showImage))

                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_detector.detectMultiScale(gray,1.3,1)

                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    count += 1
                    wd.set_time()
                    cv2.imwrite("dataset/User." + str(id) + '.' + str(count) + ".jpg", gray[y:y + h, x:x + w])

                if count>=30:
                    break

            faces,ids = getImagesAndLabels('dataset',face_detector)
            recognizer.train(faces, np.array(ids))
            recognizer.write('trainer/trainer.yml')
            with open('local.conf','w') as f:
                m = hashlib.md5()
                with open('trainer/trainer.yml','r') as fp:
                    fp_list = fp.readlines()
                    for fpp in fp_list:
                        m.update(fpp.encode('utf8'))
                f.write(m.hexdigest())

            with open('local.log','w') as f:
                for i in username:
                    f.write(i+'\n')

            recognizer = np.random.random(256)
            rw.end()



    def verify(self):
        self.comboBox_username.addItems(username)

        recognizer = cv2.face.LBPHFaceRecognizer_create()
        with open('trainer/trainer.yml','r') as f:
            m1 = hashlib.md5()
            l = f.readlines()
            for i in l:
                m1.update(i.encode('utf8'))
            m1 = m1.hexdigest()

        with open('trainer.yml.bak','r') as f:
            m2 = hashlib.md5()
            l = f.readlines()
            for i in l:
                m2.update(i.encode('utf8'))
            m2 = m2.hexdigest()

        with open('local.conf','r') as f:
            hs=f.readlines()[0]

        if m1==hs:
            recognizer.read('trainer/trainer.yml')
            if m1==m2:
                pass
            else:
                recognizer.write('trainer.yml.bak')
        elif m2==hs:
            recognizer.read('trainer.bak.yml')
            recognizer.write('trainer/trainer.yml')

        else:
            return -1


        cascadePath = "haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(cascadePath);

        font = cv2.FONT_HERSHEY_SIMPLEX

        # Initialize and start realtime video capture
        cam = cv2.VideoCapture(cam_number)
        cam.set(3, 640)  # set video widht
        cam.set(4, 480)  # set video height

        # Define min window size to be recognized as a face
        minW = 0.1 * cam.get(3)
        minH = 0.1 * cam.get(4)

        wd = WDT.Watch_Dog(5)
        rw = RandomWork.RandomWork()
        rw.start()

        while True:

            if wd.time_out()==True:
               break

            ret, img = cam.read()

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(int(minW), int(minH)),
            )

            for (x, y, w, h) in faces:

                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

                wd.set_time()

                id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

                # Check if confidence is less them 100 ==> "0" is perfect match
                if (confidence < 100):
                    id = username[id]
                    confidence = "  {0}%".format(round(100 - confidence))
                else:
                    id = "unknown"
                    confidence = "  {0}%".format(round(100 - confidence))

                cv2.putText(img, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
                cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

            #cv2.imshow('camera', img)
            img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            showImage = QtGui.QImage(img.data, img.shape[1], img.shape[0], QtGui.QImage.Format_RGB888)
            self.cam_label.setPixmap(QtGui.QPixmap.fromImage(showImage))

            k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video
            if k == 27:
                self.closeEvent()
                break
        rw.end()
        self.close()




'''
    def test_cam(self):
        self.reset_button()
        cam = cv2.VideoCapture(cam_number)
        cam.set(3, 640)  # set video width
        cam.set(4, 480)  # set video height

        while True:
            ret,img = cam.read()
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            self.image = img

            showImage = QtGui.QImage(img.data, img.shape[1], img.shape[0], QtGui.QImage.Format_RGB888)
            self.label.setPixmap(QtGui.QPixmap.fromImage(showImage))

            k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video
            if k == 27:
                break

        cam.release()

'''

def getImagesAndLabels(path,detector):

    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
    faceSamples=[]
    ids = []

    for imagePath in imagePaths:

        PIL_img = Image.open(imagePath).convert('L') # convert it to grayscale
        img_numpy = np.array(PIL_img,'uint8')

        id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = detector.detectMultiScale(img_numpy)

        for (x,y,w,h) in faces:
            faceSamples.append(img_numpy[y:y+h,x:x+w])
            ids.append(id)

    return faceSamples,ids

def main():
    app = QApplication(sys.argv)
    widget = home_face_verify()
    dialog = cam_face_verify()
    btn = widget.pushButton
    btn.clicked.connect(dialog.show)
    widget.show()
    app.exec_()


main()
