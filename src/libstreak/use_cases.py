from src.libstreak import sample_data
from src.libstreak.activity_frame import ActivityFrame
from src.libstreak.global_stats import GlobalStats
from src.libstreak.scrap_user_profile import ScrapScrap

homepage_response = None
user_profile_response = None
rating_response = None


def homepage():
    print("/homepage")
    global homepage_response
    if not homepage_response:
        homepage_response = GlobalStats().render_global_stats()
    return homepage_response


def user_profile():
    print("/user_profile")
    global user_profile_response
    if not user_profile_response:
        user_profile_response = ActivityFrame().render_activity_frames_for_all_users(
            # usernames=sample_data.sample_streak_users[:1],
            # usernames=["maity_amit_2003"],  # ["theayeshasiddiqa"],
            usernames=sample_data.sample_streak_users_leetcode,
            scrap_profile=True,
            profile_type="leetcode",
        )
    return user_profile_response


def rating():
    print("/rating")
    global rating_response
    if not rating_response:
        rating_response = ActivityFrame().render_activity_frames_for_all_users(
            usernames=sample_data.sample_streak_users[:1], scrap_profile=False
        )
    return rating_response


def scrap_user_profile():
    print("/scrap_user_profile")
    ScrapScrap().scrap_user_profile(
        # scrap_from="url",
        scrap_from="file",
    )
    return "done"
