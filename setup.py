import subprocess
import sys

if __name__ == '__main__':
    subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium==4.22.0"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "webdriver_manager==4.0.1"])