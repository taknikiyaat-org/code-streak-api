from datetime import date, datetime, timedelta

from flask import render_template

from src.libstreak.database.files import Database as db
from src.libstreak.database.files import Files as file
from src.libstreak.scrap_user_profile import ScrapScrap


class ActivityFrame:
    def render_activity_frames_for_all_users(
        self,
        usernames: list,
        scrap_profile: bool = False,
        profile_type: str = "codeforces",
    ):
        """
        :param:
            users: list = ["Um_nik", "theayeshasiddiqa"]

        :return:
            users_submissions: dict = {
                "theayeshasiddiqa": {
                    "submissions": {'2022-04-08': [0, 40, 275, ''], '2022-04-09': [0, 40, 330, '']},
                }
            }
        """

        from collections import OrderedDict

        # users_submissions = OrderedDict()
        bubble_size, gap = 40, 15

        # scrap from http and save in SUBMISSIONS_FILE
        # OR
        # fetch from STATS_FILE with stats
        if scrap_profile:
            users_submissions = self.scrap_user_submissions(usernames, profile_type)
        else:
            users_submissions = self.fetch_user_submissions(usernames)

        # users_submissions = dict(list(users_submissions.items())[:20])  # select first 2

        # generate starting coordinates for each month in the activity frame
        first_user = list(users_submissions.keys())[0]
        coordinates = self.get_date_bubbles_coordinates(
            dates=users_submissions[first_user]["submissions"],
            date_bubble_size=bubble_size + gap,
        )

        # show activity frame on FE
        return render_template(
            "rating.html",
            users_submissions=users_submissions,
            coordinates=coordinates,
            bubble_size=bubble_size,
            show_dates=True,
        )

    @staticmethod
    def scrap_user_submissions(usernames, profile_type):
        users_submissions = {}
        for username in usernames:
            # for each username, scrap his/her profile from codeforces
            users_submissions[username] = ScrapScrap().scrap_user_submissions(
                username=username, profile_type=profile_type
            )

        # save in json file
        db.save_to_file(users_submissions, file.SUBMISSIONS_FILE)
        return users_submissions

    @staticmethod
    def fetch_user_submissions(usernames):
        rows = db.fetch_from_file(file.STATS_FILE)
        # users_submissions = {}
        # for key in rows:
        #     # if key in usernames:
        #     users_submissions[key] = rows[key]
        # return users_submissions
        return rows

    @staticmethod
    def get_date_bubbles_coordinates(dates: dict, date_bubble_size: int):
        """
        :param:
            dates: dict = { '2022-04-08': 2, '2022-04-09': 3}
            date_bubble_size: int = 55
        :return:
            coordinates = {
                '2022-05-01': {'x': 287.5, 'y': 385, 'month_name': 'May'}
            }
        """
        if not dates:
            return {}

        month_index = int(list(dates)[0].split("-")[1])
        weekday_index = datetime.strptime(list(dates)[0], "%Y-%m-%d").weekday() + 1
        x, y = 40, 0
        coordinates = {}

        for coding_date in dates:
            month_name = ""

            if int(coding_date.split("-")[1]) != month_index:  # if next month
                x += date_bubble_size * 1.5  # month gap
                month_index = int(coding_date.split("-")[1])  # next month index range([1, 12])
                month_name = datetime.strptime(coding_date, "%Y-%m-%d").strftime("%B")  # next month name (June)

            if weekday_index == 7:  # next week (column completed)
                x += date_bubble_size

            weekday_index = datetime.strptime(coding_date, "%Y-%m-%d").weekday() + 1  # range([1, 7])
            y = weekday_index * date_bubble_size  # next day gap

            coordinates[coding_date] = {"x": x, "y": y, "month_name": month_name}

        return coordinates
