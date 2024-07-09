
from bs4 import BeautifulSoup
import requests
import csv

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.action_chains import ActionChains




class PlayerDetails():
    def __init__(self):
        self.driver = webdriver.Firefox()

    def get_each_team_url(self):
        self.driver.get("https://www.espncricinfo.com/series/icc-men-s-t20-world-cup-2024-1411166/squads")
        time.sleep(5)
        wait = WebDriverWait(self.driver, 2)

        # Wait for elements to load
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, " div  a span.ds-text-comfortable-m")))

        num_elements = len(self.driver.find_elements(By.CSS_SELECTOR, " div  a span.ds-text-comfortable-m"))

        for i in range(num_elements):

            # Wait until elements are clickable
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, " div  a span.ds-text-comfortable-m")))
            # Get all elements and select only the i-th one
            element = self.driver.find_elements(By.CSS_SELECTOR, " div  a span.ds-text-comfortable-m")[i]
            time.sleep(5)
            self.driver.execute_script("document.body.style.transform='scale(0.9)';")
            try:
                element.click()
            except ElementClickInterceptedException:
                time.sleep(10)
                element.click()
            time.sleep(10)


            try:
                cancel_button = self.driver.find_element(By.ID, value='wzrk-cancel')
                cancel_button.click()
            except NoSuchElementException:
                pass

            # Here do whatever has to be done on a specific webpage
            MATCH_URL = self.driver.current_url
            response = requests.get(url=MATCH_URL)
            match_response = response.text

            soup = BeautifulSoup(match_response, "html.parser")
            print(soup.title.text.split("-")[0].split(" ")[0])
            country = soup.title.text.replace(" Squad", "").split("-")[0]

            players = soup.select(".ds-flex-1 a span")
            player_names = []
            for player in players:
                name = player.getText()
                player_names.append(name)

            print(player_names)

            roles = soup.select(".ds-flex-1 p ")
            role_names = []
            for role in roles:
                name = role.getText()
                role_names.append(name)

            print(role_names)

            team = []
            for i in range(len(player_names)):
                member = [country, player_names[i], role_names[i]]
                team.append(member)

            print(team)

            fields = ["country", "player_name", "role"]
            with open("PlayerData.csv", "a") as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow(fields)
                csv_writer.writerows(team)
            time.sleep(5)
            # Go back to the previous page
            self.driver.execute_script("window.history.go(-1)")
        self.driver.quit()
    def get_match_list(self):
        MATCH_URL = "https://www.espncricinfo.com/series/icc-men-s-t20-world-cup-2024-1411166/match-schedule-fixtures-and-results"

        response = requests.get(url=MATCH_URL)
        match_response = response.text

        soup = BeautifulSoup(match_response, "html.parser")
        print(soup.title.text.split("|")[0])
        country = soup.title.text.split("-")[0].split(" ")[0]

        players = soup.select(".ds-grow .ci-team-score div  p")
        player_names = []
        for player in players:
            name = player.getText()
            player_names.append(name)

        # print(player_names)

        listOdd = player_names[1::2]  # Elements from list1 starting from 1 iterating by 2
        listEven = player_names[::2]  # Elements from list1 starting from 0 iterating by 2
        # print (listOdd)
        # print (listEven)
        team = []
        for i in range(len(listOdd)):
            member = [listEven[i], listOdd[i]]
            team.append(member)
        print(team)

        fields = ["country-1", "country-2", ]
        with open("MatchListData.csv", "w") as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(fields)
            csv_writer.writerows(team)

        self.driver.quit()

    def get_each_team_fan_ratings(self):
        self.driver.get("https://www.espncricinfo.com/series/icc-men-s-t20-world-cup-2024-1411166/squads")
        time.sleep(5)
        wait = WebDriverWait(self.driver, 2)

        # Wait for elements to load
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, " div  a span.ds-text-comfortable-m")))

        num_elements = len(self.driver.find_elements(By.CSS_SELECTOR, " div  a span.ds-text-comfortable-m"))

        for i in range(num_elements):

            # Wait until elements are clickable
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, " div  a span.ds-text-comfortable-m")))
            time.sleep(7)
            # Get all elements and select only the i-th one
            element = self.driver.find_elements(By.CSS_SELECTOR, " div  a span.ds-text-comfortable-m")[i]
            time.sleep(5)
            self.driver.execute_script("document.body.style.transform='scale(0.9)';")
            try:
                try:
                    cancel_button = self.driver.find_element(By.ID, value='wzrk-cancel')
                    cancel_button.click()
                except NoSuchElementException:
                    pass
                element.click()
            except ElementClickInterceptedException:
                time.sleep(10)
                element.click()
            time.sleep(10)

            try:
                cancel_button = self.driver.find_element(By.ID, value='wzrk-cancel')
                cancel_button.click()
            except NoSuchElementException:
                pass

            view_team = self.driver.find_element(By.CSS_SELECTOR, ".ds-pl-2  a ")
            view_team.click()
            time.sleep(5)

            # Here do whatever has to be done on a specific webpage

            view_full_team = self.driver.find_element(By.CSS_SELECTOR, ".widget-container .ds-py-2 a span")
            view_full_team.click()
            time.sleep(5)

            MATCH_URL = self.driver.current_url
            response = requests.get(url=MATCH_URL)
            match_response = response.text

            soup = BeautifulSoup(match_response, "html.parser")

            country = soup.title.text.replace(" Fan Ratings", "").split("-")[0]
            print(country)

            players = soup.select(".ds-sticky div a span")
            player_names = []
            for player in players:
                name = player.getText()
                player_names.append(name)
            player_names = player_names[1::2]

            print(player_names)

            ratings = soup.select(".ds-w-0 .ds-rounded-full span ")
            rating_names = []
            for role in ratings:
                name = role.getText()
                rating_names.append(name)

            print(rating_names)

            time.sleep(3)
            self.driver.execute_script("window.history.go(-1)")
            time.sleep(3)
            self.driver.execute_script("window.history.go(-1)")


            team = []
            for i in range(len(player_names)):
                member = [country, player_names[i], rating_names[i]]
                team.append(member)

            print(team)
            #
            fields = ["country", "player_name", "fan-ratings"]
            with open("FanRatingData.csv", "a") as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow(fields)
                csv_writer.writerows(team)
            # Go back to the previous page

            time.sleep(5)
            # Go back to the previous page
            self.driver.execute_script("window.history.go(-1)")
            time.sleep(5)
        self.driver.quit()

bot = PlayerDetails()
# bot.get_each_team_url()
# bot.get_match_list()
bot.get_each_team_fan_ratings()



