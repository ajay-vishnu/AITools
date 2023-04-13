from modules.replymails import Replymails
from modules.service import Service
import random
import time

def main():

    # Create a Gmail API service instance
    service = Service(type="modify")

    while(True):
        response = Replymails(service=service)
        print(response)

        # Implement the sleep duration between replying to the mails.
        pause_time = random.randint(45, 120)
        print(f"Sleeping for {pause_time} secs.")
        time.sleep(pause_time)


if __name__ == '__main__':
    main()