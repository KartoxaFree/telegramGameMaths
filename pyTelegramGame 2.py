import cv2
import os
import pytesseract
import pyscreenshot
import pyautogui
import re
import numexpr as ne
import mouse
import keyboard
import time


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

now_tz = ""
s = 0


def dop():
    image = pyautogui.screenshot('screenshot2.png', region=(670, 18, 550, 40))
    image.save("screenshot2.png")

    image = cv2.imread('screenshot2.png')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = 255 - cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Blur and perform text extraction
    thresh = cv2.GaussianBlur(thresh, (3, 3), 0)
    ad = pytesseract.image_to_string(thresh, lang='eng', config='--psm 6')
    ad = data.replace("\n", "")
    sad += "\n"
    f = open("1.txt", 'w')
    f.write(data)
    f.close()


def screen():
    image = pyautogui.screenshot('screenshot.png', region=(700, 520, 525, 80))
    image.save("screenshot.png")


def analiz():
    image = cv2.imread('screenshot.png')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = 255 - cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Blur and perform text extraction
    thresh = cv2.GaussianBlur(thresh, (3, 3), 0)
    data = pytesseract.image_to_string(thresh, lang='eng', config='--psm 6')
    print("example: " + data.replace("\n", ""))

    return data


def refract_tz(data):
    data = data.replace('?', '')
    data = data.replace('=', '')
    data = data.replace('\n', '')
    data = data.replace(' ', '')

    return data


def restart():
    mouse.move(970, 1030, absolute=True, duration=0.1)
    mouse.click('left')
    time.sleep(2)


def calculation(data):
    data_split_zn = re.split('|1|2|3|4|5|6|7|8|9|0', data)
    data_split_zn = list(filter(len, data_split_zn))

    st = ""
    data_split_num = []
    #формировка чисел
    try:
        for i in range(len(data)):
            if data[i] in ["+", "-", "/", "*"]:
                data_split_num.append(int(st))
                st = ""
            else:
                st += data[i]
            if i == len(data) - 1:
                data_split_num.append(int(st))

        for i in range(len(data_split_zn)):
            match data_split_zn[i]:
                case "+":
                    data_split_num = [int(data_split_num[0]) + int(data_split_num[1])] + data_split_num
                    data_split_num.pop(1)
                    data_split_num.pop(1)
                case "-":
                    data_split_num = [int(data_split_num[0]) - int(data_split_num[1])] + data_split_num
                    data_split_num.pop(1)
                    data_split_num.pop(1)
                case "*":
                    print("Пока что такое решать не умею")
                    exit(0)
                case "/":
                    print("Пока что такое решать не умею")
                    exit(0)
        print("answer: " + str(data_split_num[0]))

        return data_split_num[0]
    except Exception as e:
        return -1


def click_on_answer(answer):
    match answer:
        case 1:
            mouse.move(960, 660, absolute=True, duration=0.01)
            # mouse.move(960, 890, absolute=True, duration=0.1)
            mouse.click('left')
        case 2:
            mouse.move(960, 730, absolute=True, duration=0.01)
            # mouse.move(960, 990, absolute=True, duration=0.1)
            mouse.click('left')
        case 3:
            mouse.move(960, 800, absolute=True, duration=0.01)
            # mouse.move(960, 1075, absolute=True, duration=0.1)
            mouse.click('left')

    time.sleep(1)
    print("good\n")


def crutch(data):
    data_split_zn = re.split('|1|2|3|4|5|6|7|8|9|0', data)
    data_split_zn = list(filter(len, data_split_zn))

    st = ""
    data_split_num = []
    for i in range(len(data)):
        if data[i] in ["+", "-", "/", "*"]:
            data_split_num.append(int(st))
            st = ""
        else:
            st += data[i]
        if i == len(data) - 1:
            data_split_num.append(int(st))

    print(data_split_num)
    for i in range(len(data_split_num)):
        if len(str(data_split_num[i])) != 1:
            data_split_num[i] = str(data_split_num[i]).replace("4", "+")
            st2 = ""
            for j in range(len(data_split_num[i])):
                if data_split_num[i][j] == "+" and (j == 0 or j == len(data_split_num[i])-1):
                    continue
                else:
                    st2 += data_split_num[i][j]
            data_split_num[i] = st2

    print(data_split_num)

    st = ""
    for i in range(len(data_split_num)):
        st += str(data_split_num[i])
        if i != len(data_split_num)-1:
            st += str(data_split_zn[i])
    print(st)

    return st


keyboard.add_hotkey('Ctrl + 0', lambda: exit(0))

while True:
    if s == 0:
        #dop()
        time.sleep(0.5)
        screen()
        now_tz = analiz()
        now_tz = refract_tz(now_tz)
        if any(c.isalpha() for c in now_tz):
            restart()
            continue
    sc = calculation(now_tz)
    if sc in [1, 2, 3]:
        click_on_answer(sc)
        s = 0
    else:
        now_tz = crutch(now_tz)
        s = 1