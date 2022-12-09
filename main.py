import re
from datetime import datetime
import json

import bs4
import requests
from bs4 import BeautifulSoup
from time import sleep
import random


class Bible:

    def __init__(self):
        self.char = 20
        self.FILE_NAME = "verses.json"
        self.num_verses = 0

    @staticmethod
    def url() -> str:
        return 'https://bible.knowing-jesus.com/popular'

    def save_requests(self, verses: bs4.element.ResultSet, number: int) -> None:
        data = []
        print(f"Downloading {number} verses...")
        with open(self.FILE_NAME, "w") as file:
            for item in range(number):
                verse = verses[item].text
                data.append(verse)
            json.dump(data, file)
            print(f"Data Saved to \"{file.name}\".")
            print()

    def set_user_length(self, user=False, number=1000) -> None:
        if user:
            if number <= 1000:
                number = int(number)
            elif number > 1000:
                number = random.randint(100, 1000)
            else:
                number = 1000
        self.num_verses = number

    @staticmethod
    def user(question) -> str:
        user_input = input(question)
        while not len(user_input) > 0:
            user_input = input(question)
        return user_input

    def user_delay(self, prompt="How long do you want to wait between verses? (minutes) ") -> int:
        while True:
            try:
                return int(self.user(prompt))
            except ValueError:
                print("Invalid input. Please enter a number.")

    def user_shuffle(self, prompt="Do do you want to shuffle data? (y/n) ") -> bool:
        while True:
            shuffle = self.user(prompt).casefold()
            if re.match(r"(y|yes|yeah)", shuffle):
                return True
            elif re.match(r"(n|no|nah)", shuffle):
                return False
            else:
                print("Invalid input. Please enter yes or no.")

    def make_requests(self, user=False, number=1000) -> None:
        result = requests.get(self.url())
        print(f"Parsing data from {self.url()}...")
        doc = BeautifulSoup(result.text, "html.parser")
        verses = doc.find_all('div', {'class': 'item_text'})
        doc.encode('utf-8')
        self.set_user_length(user, number)
        self.save_requests(verses, number)

    def get_data(self) -> list:
        with open(self.FILE_NAME, "r") as file:
            print(f"Getting data from \"{file.name}\"")
            return json.load(file)

    def bible(self):
        minutes = self.user_delay()
        data = self.get_data()
        if self.user_shuffle():
            print("Shuffling data...")
            random.shuffle(data)
        count = 0
        while True:
            count += 1
            print(f"Verse number {count} – {datetime.now().strftime('%I:%M %p')}")
            print(data[count - 1])
            data.pop(count - 1)
            if count == len(data):
                prompt = self.user("Another round? (y/n) ").casefold()
                if re.match(r"(y|yes|yeah)", prompt):
                    self.bible()
                return "Script Over"
            sleep(minutes * 60)

    def main(self):
        print("Starting Script")
        customised = self.user("Do you want the download the default 1000 verses? (y/n) ").casefold()
        if re.match(r"(y|yes|yeah)", customised):
            self.make_requests()
        elif re.match(r"(n|no|nah)", customised):
            print("1000 verses are available.")
            verses = self.user("How many verses do you want to download? (>100 Recommended) ")
            self.make_requests(user=True, number=int(verses))
        self.bible()


if __name__ == "__main__":
    bible = Bible()
    bible.main()
