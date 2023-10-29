import json

import openpyxl
import toml
from sqlalchemy.orm import Session

from src.libstreak.database.models import Profile, Streak, StreakMember, User, UserProfile, engine
from src.libstreak.data import global_vars

# black --line-length 120 src/libstreak/database/files.py


def import_data():
    streak = import_streak()
    profiles = import_profiles()
    users = import_data_from_excel_sheet()
    with Session(engine) as session:
        session.add(streak)
        session.add_all(profiles)
        for row in users:
            user = row["user"]
            user_profiles = row["user_profiles"]
            session.add(user)
            session.flush()  # adds in db before committing
            for user_profile in user_profiles:
                user_profile.id_user = user.id_user
            session.add_all(user_profiles)
            session.add(
                StreakMember(
                    id_streak=streak.id_streak,
                    id_user=user.id_user,
                    joined_at=row["joined_at"],
                )
            )
        session.commit()


def import_data_from_excel_sheet():
    dataframe = openpyxl.load_workbook(filename=global_vars.STREAK_365_DAYS_OF_CODE).active
    users = []
    for i in range(2, dataframe.max_row - 0 + 1):  # - 335
        user, user_profiles = create_user(i, dataframe)
        users.append(
            {
                "user": user,
                "user_profiles": user_profiles,
                "joined_at": dataframe[i][0].value
            }
        )
    return users


def create_user(i, dataframe):
    name = dataframe[i][1].value.strip()
    graduation_year = "".join(x for x in str(dataframe[i][3].value) if x.isdigit())
    if graduation_year and int(graduation_year) > 9999:
        graduation_year = int(graduation_year) / 10
    user = User(
        username=name.replace(" ", "_") + "_" + str(i - 1),
        first_name=name.split(" ")[0],
        last_name=" ".join(name.split(" ")[1:]) if len(name.split(" ")) > 1 else "",
        university=dataframe[i][2].value,
        degree_title=dataframe[i][4].value,
        graduation_year=graduation_year if graduation_year else 1900,
        company=str(dataframe[i][8].value)[:50],
        email="",
        phone=dataframe[i][5].value,
        home_country="",
        city="",
    )
    user_profiles = [
        UserProfile(
            id_user=1,
            id_profile=1,
            url=dataframe[i][6].value or "N/A",
        ),
        UserProfile(
            id_user=1,
            id_profile=4 if "codeforces" in str(dataframe[i][7].value) else 3,
            url=dataframe[i][7].value or "N/A",
        )
    ]
    return user, user_profiles


def import_profiles():
    with open(global_vars.TOML_DATA, "rt") as fp:
        profiles = toml.load(fp)["profiles"]  # dict {'profiles': [{'id_profile': 1, 'name': 'linkedin', ...
        profiles = [Profile(**profile) for profile in profiles]
    return profiles


def import_streak():
    return Streak(
        title="365 Days of Code",
        start_date="2023-01-01 00:00:00",
        end_date="2023-12-31 00:00:00",
    )
