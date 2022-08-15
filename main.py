from datetime import datetime
import json

import requests
from bs4 import BeautifulSoup
from time import sleep
import random


class Bible:

    def __init__(self):
        self.char = 20

    @staticmethod
    def url():
        url = 'https://bible.knowing-jesus.com/popular'
        return url

    def save_data(self, user=False, number=1000):
        result = requests.get(self.url())
        print(f"Parsing data from {self.url()}...")
        doc = BeautifulSoup(result.text, "html.parser")
        verses = doc.find_all('div', {'class': 'item_text'})
        doc.encode('utf-8')
        data = []

        if user:
            if number <= 1000:
                number = int(number)
            else:
                number = 1000

        print(f"Downloading {number} verses...")
        with open("verses.json", "w") as file:
            for item in range(number):
                verse = verses[item].text
                data.append(verse)
            json.dump(data, file)
            print(f"Data Saved to \"{file.name}\".")
            print()

    @staticmethod
    def get_data():
        with open("verses.json", "r") as file:
            print(f"Getting data from \"{file.name}\"")
            data = json.load(file)
            return data

    @staticmethod
    def user(question):
        user_input = input(question)
        while not len(user_input) > 0:
            user_input = input(question)
        return user_input

    def bible(self):
        minutes = float(self.user('Enter the frequency of verses in minutes: '))
        self.beautify(self.char)

        data = self.get_data()
        if self.user("Do do you want to shuffle data? (y/n) ").casefold() == "y":
            print("Shuffling data...")
            for i in range(50):
                random.shuffle(data)

        count = 0
        while True:
            count += 1
            print(f"Verse number {count} – {datetime.now().strftime('%I:%M %p')}")
            self.beautify(self.char)
            print(data[count - 1])
            self.beautify(self.char)
            data.pop(count - 1)
            if count == len(data):
                if self.user("Another round? (y/n) ").casefold() == "y":
                    self.bible()
                return "Script Over"
            sleep(minutes * 60)

    def beautify(self, char):
        self.char = char
        print((char*'–')*2)

    def main(self):
        print("Starting Script")
        customised = self.user("Do you want the download the default 1000 verses? (y/n) ").casefold()
        if customised == "y":
            self.save_data()
        else:
            print("1000 verses are available.")
            verses = self.user("How many verses do you want to download? (>100 Recommended) ")
            self.save_data(user=True, number=int(verses))
        self.bible()


if __name__ == "__main__":
    bible = Bible()
    bible.main()
