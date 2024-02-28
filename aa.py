import time
import subprocess

def main():
    while True:
        print("Forrit 1 er í gangi...")
        time.sleep(1)
        
        # Ræsa forrit1.py
        subprocess.Popen(["python3", "bb.py"])
        print("Forrit 1 hefur verið kveikt.")

        time.sleep(600)  # Bíða í 600 sekúndur

        # Stöðva forrit1.py
        subprocess.run(["pkill", "-f", "bb.py"])
        print("Forrit 1 hefur verið stöðvað.")

if __name__ == "__main__":
    main()
