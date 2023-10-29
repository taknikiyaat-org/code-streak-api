from flask import render_template

from src.libstreak import sample_data
from src.libstreak.database.files import Database as db
from src.libstreak.database.files import Files as file


class GlobalStats:
    def render_global_stats(self):
        """
        fetch from file SUBMISSIONS_FILE, compute stats and save in STATS_FILE
        user
        total_solved
        total_solved_streak
        :return:
        """
        users_submissions = db.fetch_from_file(file.SUBMISSIONS_FILE)

        users_submissions = dict(list(users_submissions.items())[:10])  # select first 2

        for user in users_submissions:
            a, b = self.compute_total_solved(users_submissions[user]["submissions"], after="2022-12-29")
            (
                users_submissions[user]["total_solved"],
                users_submissions[user]["total_solved_streak"],
            ) = (a, b)

            # print("users_submissions", user, a, b)

        # sort by total_solved
        users_submissions = dict(
            sorted(
                users_submissions.items(),
                key=lambda x: x[1]["total_solved_streak"],
                reverse=True,
            )
        )
        db.save_to_file(users_submissions, file.STATS_FILE)

        return render_template(  # picks .html file from the folder appstreak/templates
            "homepage.html", users_data="users_data", size="size", show_dates=False
        )  # todo just retyrn data not the template

    @staticmethod
    def compute_total_solved(submissions, after=None):
        total_solved, total_solved_streak = 0, 0
        for day in submissions:
            total_solved = total_solved + 1 if submissions[day] > 0 else total_solved
            if after and after < day:
                total_solved_streak = total_solved_streak + 1 if submissions[day] > 0 else total_solved_streak
        return total_solved, total_solved_streak
