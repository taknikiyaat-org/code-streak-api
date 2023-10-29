import json
import re
from datetime import date, datetime, timedelta

import requests
from bs4 import BeautifulSoup

from src.libstreak.database.files import Database as db
from src.libstreak.database.files import Files as file


class ScrapScrap:
    def scrap_user_profile(self, scrap_from: str):
        if scrap_from == "file":
            users = db.fetch_from_file(file.USERS)
            users = dict(list(users.items())[:])
            print(users)
            all_dates: list = self.generate_one_year_dates(year=date.today().year)  # ['2022-04-08', '2022-04-09', ...]

            users_submissions = {}
            for username in users:
                # print(username, users[username]["profiles"])
                if "codeforces" in users[username]["profiles"]:
                    users_submissions[str(username) + "-codeforces"] = self.scrap_codeforces_profile(
                        username, all_dates
                    )
                if "leetcode" in users[username]["profiles"]:
                    users_submissions[str(username) + "-leetcode"] = self.scrap_leetcode_profile(username, all_dates)
            for key in users_submissions:
                print(key)
            # save in json file
            db.save_to_file(users_submissions, file.SUBMISSIONS_FILE)

    def scrap_codeforces_profile(self, username, all_dates):
        # print(username, users[username]["profiles"][0])
        user_file = open(f"libstreak/data/codeforces_profiles/{username}__2023-04-20.txt")  # Opening JSON file
        # profile_content = json.load(user_file)  # returns JSON object as a dictionary
        profile_content = user_file.read()
        user_file.close()
        # print(profile_content)
        user_submissions = self.scrap_submissions_codeforces(
            profile_content=profile_content, all_dates=all_dates
        )  # {"2022-03-18": 2, ...}
        return {"submissions": user_submissions}

    def scrap_leetcode_profile(self, username, all_dates):
        # print(username, users[username]["profiles"][0])
        user_file = open(f"libstreak/data/leetcode_profiles/{username}__2023-04-20.txt")  # Opening JSON file
        # profile_content = json.load(user_file)  # returns JSON object as a dictionary
        profile_content = user_file.read()
        user_file.close()
        # print(profile_content)
        user_submissions = self.scrap_submissions_leetcode(
            profile_content=profile_content, all_dates=all_dates
        )  # {"2022-03-18": 2, ...}
        return {"submissions": user_submissions}

    def scrap_user_submissions(self, username: list, profile_type="codeforces"):
        """
        :return:
            {"submissions": {"2022-03-18": 2, "2022-03-19": 3}}
        """

        page = self.get_page_content(username, profile_type)  # "b'\r\n<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML "
        page_content = str(page.content)
        # generate all dates for past 365 days (past year)
        all_dates: list = self.generate_one_year_dates(year=date.today().year)  # ['2022-04-08', '2022-04-09', ...]

        user_submissions = {}
        if profile_type == "codeforces":
            user_submissions = self.scrap_submissions_codeforces(
                profile_content=page_content, all_dates=all_dates
            )  # {"2022-03-18": 2, ...}
        elif profile_type == "leetcode":
            soup = BeautifulSoup(page.content, "html.parser")
            user_submissions = self.scrap_submissions_leetcode(
                profile_content=page_content, all_dates=all_dates, soup=soup
            )  # {"2022-03-18": 2, ...}

        # print("submissions", user_submissions)
        return {"submissions": user_submissions}

    @staticmethod
    def get_page_content(username, profile_type):
        url = f"https://codeforces.com/profile/{username}"
        if profile_type == "leetcode":
            url = f"https://leetcode.com/{username}"
        page = requests.get(url)
        # print(page.content)
        return page

    @staticmethod
    def scrap_submissions_codeforces(profile_content, all_dates):
        pattern = r"\w+\-\w+\-\w+\"\: \{\\n                        items: \[\\n                            \w+\\n                        ]\\n"
        matches = re.findall(pattern, profile_content)

        data = []
        for match in matches:
            submissions = int([a.strip() for a in match.split("\\n")][2])
            date = [a.strip() for a in match.split("\\n")][0].split('"')[0]
            data.append([date, submissions])

        data.sort(key=lambda x: datetime.strptime(x[0], "%Y-%m-%d"))

        submissions = {}
        for item in data:
            submissions[item[0]] = item[1]

        all_submissions = {}
        for item in all_dates:
            all_submissions[item] = submissions[item] if item in submissions else 0

        return all_submissions  # {"2022-03-18": 2, ...}

    @staticmethod
    def scrap_submissions_leetcode(profile_content, all_dates, soup=None):
        if soup:
            element = soup.find(
                "div",
                attrs={"class": "hidden h-auto w-full flex-1 items-center justify-center lc-md:flex"},
            )
        else:
            pattern = r'<div class="hidden h-auto w-full flex-1 items-center justify-center lc-md:flex">.*</div>'
            # pattern = r'hidden h-auto w-full flex-1 items-center justify-center lc-md:flex.*</div>'
            matches = re.findall(pattern, profile_content)
            # print("profile_content=", profile_content)
            # print("matches=", matches)
            element = matches[0].split("</div>")[0]
            # print("element=", element)
        profile_content = str(element)

        pattern = r"<rect.*</rect>"
        matches = re.findall(pattern, profile_content)
        matches = matches[0].split("</rect>")[:-1]  # last [, '']
        # print("len(matches)", len(matches), len(all_dates))

        i = 0
        # days_colors = ["#6BCF8E", "#2CBB5D", "#4CC575", "rgba(44, 181, 93, 0.5)"]
        matches = list(reversed(matches))
        all_dates = list(reversed(all_dates))
        submissions = {}
        for match in matches:
            if "transparent" in match:
                continue
            if "rgba(255, 255, 255, 0.1)" in match:
                submissions[all_dates[i]] = 0
            elif "#6BCF8E" in match or "rgba(44, 181, 93, 0.5)" in match:
                submissions[all_dates[i]] = 1
            elif "#4CC575" in match:
                submissions[all_dates[i]] = 4
            else:
                submissions[all_dates[i]] = 4
            i += 1

        from collections import OrderedDict

        submissions = OrderedDict(reversed(list(submissions.items())))

        return submissions

    @staticmethod
    def generate_one_year_dates(year):
        # d1 = date(year, 1, 1)
        # d2 = date(year, 12, 31)
        d1 = datetime.now() - timedelta(days=365)
        d2 = datetime.now()
        days = [d1 + timedelta(days=x) for x in range((d2 - d1).days + 1)]
        days = [day.strftime("%Y-%m-%d") for day in days]
        return days
