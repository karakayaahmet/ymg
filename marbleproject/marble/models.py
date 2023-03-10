from django.db import models
from django.conf import settings
from PIL import Image
from tensorflow.keras.utils import img_to_array, load_img
from keras.preprocessing import image
from tensorflow.python import ops
from keras.models import load_model
import os
import numpy as np
import tensorflow as tf
import cv2
import math
import scipy.ndimage
import matplotlib.pyplot as plt
import random as rnd
import statistics
from django.dispatch import receiver
from django.db.models.signals import post_save




class Resimler(models.Model):
    image = models.ImageField(upload_to='media/')
    title = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    average_color = models.CharField(max_length=20, blank=True)
    crack = models.CharField(max_length=4, blank=True)
    dot = models.CharField(max_length=4, blank=True)
    good = models.CharField(max_length=4, blank=True)
    joint = models.CharField(max_length=4, blank=True)
    kalite_turu = models.CharField(max_length=5, blank=True)

    class Meta:
        get_latest_by = 'created_at'


    def save(self, *args, **kwargs):
        img = Image.open(self.image)
        

        classes_tur = ["AageanRose", "AfyonBal", "AfyonBeyaz", "AfyonBlack", "AfyonGrey", "AfyonSeker", "Bejmermer", "Blue", "Capuchino", "Diyabaz", "DolceVita", "EkvatorPijama", "ElazigVisne", "GoldGalaxy", "GulKurusu", "KaplanPostu", "Karacabeysiyah", "Konglomera", "KristalEmprador", "Leylakmermer", "MediBlack", "OliviaMarble", "Oniks", "RainGrey", "Traverten"]


        try:
            test_img = img.resize((224,224))
            test_img = img_to_array(test_img)
            test_img = np.expand_dims(test_img, axis = 0)
            interpreter = tf.lite.Interpreter(model_path="yeni-tur_model.tflite")
            interpreter.allocate_tensors()
            input_details = interpreter.get_input_details()
            output_details = interpreter.get_output_details()

            input_shape = input_details[0]['shape']
            interpreter.set_tensor(input_details[0]['index'], test_img)
            interpreter.invoke()

            output_data = interpreter.get_tensor(output_details[0]['index'])
            output_probs = tf.math.softmax(output_data)
            pred_label = tf.math.argmax(output_probs)

            predictions = output_probs
            print(predictions)

            max_index = np.argmax(predictions)
            classes = ["AageanRose", "AfyonBal", "AfyonBeyaz", "AfyonBlack", "AfyonGrey", "AfyonSeker", "Bejmermer",
                       "Blue", "Capuchino", "Diyabaz", "DolceVita", "EkvatorPijama", "ElazigVisne", "GoldGalaxy",
                       "GulKurusu", "KaplanPostu", "Karacabeysiyah", "Konglomera", "KristalEmprador", "Leylakmermer",
                       "MediBlack", "OliviaMarble", "Oniks", "RainGrey", "Traverten"]
            print(max_index)
            print(classes[max_index])
            self.title = str(classes[max_index])

            # Renk analizi

            img = Image.open(self.image)
        # Get the average color of the image
            width, height = img.size
            pixels = img.load()
            r, g, b = 0, 0, 0
            count = 0
            for x in range(width):
                for y in range(height):
                    r += pixels[x, y][0]
                    g += pixels[x, y][1]
                    b += pixels[x, y][2]
                    count += 1
            r_avg = r/count
            g_avg = g/count
            b_avg = b/count
        # Convert the color code to hex format
            color_code = '#{:02x}{:02x}{:02x}'.format(int(r_avg), int(g_avg), int(b_avg))
            self.average_color = color_code


            # file_model = os.path.join(settings.BASE_DIR, "yeni-tur_model.h5")
            # graph = tf.compat.v1.get_default_graph()
            #
            # with graph.as_default():
            #     model = load_model(file_model)
            #     pred = np.argmax(model.predict(test_img))
            #     self.title = str(classes_tur[pred])


            



        except:
            self.title = "S??n??fland??rma Ba??ar??s??z"
            self.average_color = "Renk Kodu Bulunamad??"

        try:
            # ??atlak t??r?? analizi:
            #image load with numpy
            img = Image.open(self.image)
            test_img = img.resize((256,256))
            test_img = img_to_array(test_img)
            test_img = np.expand_dims(test_img, axis = 0)

            """
            import cv2
            #image load with opencv
            img = cv2.imread("deneme/visne.png")
            img = cv2.resize(img, (224,224))
            img = np.array(img, dtype="float32")
            img = np.reshape(img, (1,224,224,3))
            """

            #Modelin y??klenmesi ve giri?? ????k???? tensorlerin haz??rlanmas??
            interpreter = tf.lite.Interpreter(model_path="yepyeni_catlak.tflite")
            interpreter.allocate_tensors()
            input_details = interpreter.get_input_details()
            output_details = interpreter.get_output_details()



            #Giri?? tensor?? olarak diziye d??n????t??r??lm???? imgenin verilmesi ve prediction i??lemi
            interpreter.set_tensor(input_details[0]['index'],test_img)
            interpreter.invoke()
            predictions = tf.math.softmax(interpreter.get_tensor(output_details[0]['index']))


            print(predictions)



            #olas??l??klar aras??ndan en b??y??????n??n se??ilmesi ve t??r e??le??tirilmesi
            max_index = np.argmax(predictions)

            sonuclar = []

            for i in predictions:
                sonuclar.append(i.numpy())

            print(classes[max_index])

            crack1 = "{:.2f}".format(sonuclar[0][0]*100)
            dot1 = "{:.2f}".format(sonuclar[0][1]*100)
            good1 = "{:.2f}".format(sonuclar[0][2]*100)
            joint1 = "{:.2f}".format(sonuclar[0][3]*100)
            # self.crack = str(sonuclar[0][0]*100)
            # self.dot = str(sonuclar[0][1]*100)
            # self.good = str(sonuclar[0][2]*100)
            # self.joint = str(sonuclar[0][3]*100)

            self.crack = crack1
            self.dot = dot1
            self.good = good1
            self.joint = joint1


        except:

            self.crack = "--"
            self.dot = "--"
            self.good = "--"
            self.joint = "--"

        try:
            # ??atlak t??r?? analizi:
            #image load with numpy
            img = Image.open(self.image)
            test_img = img.resize((256,256))
            test_img = img_to_array(test_img)
            test_img = np.expand_dims(test_img, axis = 0)

            """
            import cv2
            #image load with opencv
            img = cv2.imread("deneme/visne.png")
            img = cv2.resize(img, (224,224))
            img = np.array(img, dtype="float32")
            img = np.reshape(img, (1,224,224,3))
            """

            #Modelin y??klenmesi ve giri?? ????k???? tensorlerin haz??rlanmas??
            interpreter = tf.lite.Interpreter(model_path="yepyeni_kalite.tflite")
            interpreter.allocate_tensors()
            input_details = interpreter.get_input_details()
            output_details = interpreter.get_output_details()



            #Giri?? tensor?? olarak diziye d??n????t??r??lm???? imgenin verilmesi ve prediction i??lemi
            interpreter.set_tensor(input_details[0]['index'],test_img)
            interpreter.invoke()
            predictions = tf.math.softmax(interpreter.get_tensor(output_details[0]['index']))


            print(predictions)



            #olas??l??klar aras??ndan en b??y??????n??n se??ilmesi ve t??r e??le??tirilmesi
            max_index = np.argmax(predictions)

            classes_kalite = ['Q4A','Q4B','Q3C','Q3B','Q3A','Q4C']

            print(classes_kalite[max_index])

            self.kalite_turu = str(classes_kalite[max_index])


        except:

            self.kalite_turu = "Kalite T??r?? Bulunamad??."


        return super().save(*args, **kwargs)
