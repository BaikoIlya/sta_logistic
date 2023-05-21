import os
import time
from datetime import datetime
from pathlib import Path


def main():
    start_time = int(datetime.now().timestamp())
    if not Path('data').exists():
        os.makedirs('data')
    while int(datetime.now().timestamp()) - start_time < 120:
        name = int(datetime.now().timestamp())
        text = str(name)
        with open(f'data/{name}.txt', 'w') as file:
            file.write(text)
        time.sleep(5)


if __name__ == '__main__':
    main()
