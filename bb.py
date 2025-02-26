#!/usr/bin/python
import json
import multiprocessing
import time
import math
import requests
import RPi.GPIO as GPIO

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    segments = (11, 4, 23, 8, 7, 10, 18, 25)
    for segment in segments:
        GPIO.setup(segment, GPIO.OUT)
        GPIO.output(segment, 0)

    digits = (22, 27, 17, 24)
    for digit in digits:
        GPIO.setup(digit, GPIO.OUT)
        GPIO.output(digit, 1)

    return segments, digits

def save_to_json(filepath, data, pretty=False):
    if pretty:
        data_text = json.dumps(data, indent=4, ensure_ascii=False, sort_keys=True)
    else:
        data_text = json.dumps(data, separators=(',', ':'), ensure_ascii=False, sort_keys=True)
    with open(filepath, mode='w', encoding='utf-8') as json_file:
        json_file.write(data_text)

def fetch_landsnet_data(segments, digits):
    url = 'https://amper.landsnet.is/MapData/api/measurements'
    next_fetch_time = time.time()

    while True:
        # Sækja gögn ef næsti sækja tími hefur náðst
        if time.time() >= next_fetch_time:
            res = requests.get(url)
            if res.status_code == 200:
                data = res.json()
                better_data = {}
                for measurement in data:
                    better_data[measurement['key']] = measurement
                save_to_json('better_data.json', better_data, pretty=True)
                gogn1 = better_data['BV2']['MW']
                gogn2 = better_data['BV2]['time']
                print("hallo heimur")
                print(gogn1, "MW")
                print("Tálknafjarðarlína 1")
                print(gogn2)

                num = {' ': (0, 0, 0, 0, 0, 0, 0),
                       '0': (1, 1, 1, 1, 1, 1, 0),
                       '1': (0, 1, 1, 0, 0, 0, 0),
                       '2': (1, 1, 0, 1, 1, 0, 1),
                       '3': (1, 1, 1, 1, 0, 0, 1),
                       '4': (0, 1, 1, 0, 0, 1, 1),
                       '5': (1, 0, 1, 1, 0, 1, 1),
                       '6': (1, 0, 1, 1, 1, 1, 1),
                       '7': (1, 1, 1, 0, 0, 0, 0),
                       '8': (1, 1, 1, 1, 1, 1, 1),
                       '9': (1, 1, 1, 1, 0, 1, 1)}

                if gogn1 == 0:
                    staerdargrada_gogn1 = 0
                else:
                    staerdargrada_gogn1 = int(math.floor(math.log10(abs(gogn1))))
                if gogn1 < 0:
                    gogn1_formatted = gogn1
                else:
                    gogn1_formatted = gogn1 / pow(10, staerdargrada_gogn1) * 1000

                try:
                    while True:
                        if gogn1_formatted == 0:
                            a = 0
                        else:
                            a = int(gogn1_formatted)
                        s = str(a)
                        if staerdargrada_gogn1 > 3:
                            s = '9999'
                        elif staerdargrada_gogn1 == -1:
                            s = '0' + s
                        elif staerdargrada_gogn1 == -2:
                            s = '0' + '0' + s
                        elif staerdargrada_gogn1 == -3:
                            s = '0' + '0' + '0' + s
                        elif staerdargrada_gogn1 < -3:
                            s = '0000'
                        # Setja inn umferðarsamstillt stopp áður en næstu uppfærslu á stöðum lýsandi er gerð
                        for digit in range(4):
                            for loop in range(0, 7):
                                GPIO.output(segments[loop], num[s[digit]][loop])
                                if -3 <= staerdargrada_gogn1 < 1 and digit == 0:
                                    GPIO.output(25, 1)
                                elif staerdargrada_gogn1 == 1 and digit == 1:
                                    GPIO.output(25, 1)
                                elif staerdargrada_gogn1 == 2 and digit == 2:
                                    GPIO.output(25, 1)
                            GPIO.output(digits[digit], 0)
                            time.sleep(0.002)
                            GPIO.output(digits[digit], 1)
                            GPIO.output(25, 0)
                            time.sleep(0.0001)
                finally:
                    GPIO.cleanup()
def main():
    segments, digits = setup_gpio()
    fetch_landsnet_data(segments, digits)

if __name__ == '__main__':
    try:
        main()
    finally:
        GPIO.cleanup()
