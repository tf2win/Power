import time
import subprocess
import requests
import netifaces

def check_internet_connection(url='https://amper.landsnet.is/amper/'):
    try:
        requests.get(url, timeout=5)
        return True
    except requests.ConnectionError:
        return False

def main():
    while True:
        print("Forrit 1 er í gangi...")
        time.sleep(1)

        while not check_internet_connection():
            print("Bíð eftir að heimasíðan sé aðgengileg...")
            time.sleep(2)

        print("Heimasíðan er aðgengileg. Áfram í næstu athugun.")
        # Ræsa forrit1.py
        subprocess.Popen(["python3", "/home/r3/Desktop/lv/bb.py"])
        print("Forrit 1 hefur verið kveikt.")

        time.sleep(600)  # Bíða í 600 sekúndur

        # Stöðva forrit1.py
        subprocess.run(["pkill", "-f", "/home/r3/Desktop/lv/bb.py"])
        print("Forrit 1 hefur verið stöðvað.")

if __name__ == "__main__":
    main()
