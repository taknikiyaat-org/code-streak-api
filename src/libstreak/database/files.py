import json

# black --line-length 120 src/libstreak/database/files.py


class Files:
    ROOT = "/Users/ayeshasmacbookpro/Documents/IDEs/PyCharm/tak-streak-api/"
    SUBMISSIONS_FILE = ROOT + "src/libstreak/data/users_submissions.json"  # /
    STATS_FILE = ROOT + "src/libstreak/data/users_stats.json"
    TEMP_FILE = ROOT + "src/libstreak/data/temp.json"
    USERS = ROOT + "src/libstreak/data/users.json"
    STREAK_365_DAYS_OF_CODE = f"{ROOT}src/libstreak/data/365_days_of_code.xlsx"


class Database:
    @staticmethod
    def fetch_from_file(file_path):
        file = open(file_path)  # Opening JSON file
        content = json.load(file)  # returns JSON object as a dictionary
        file.close()
        return content

    @staticmethod
    def save_to_file(content, file_path):
        json_object = json.dumps(content, indent=4)  # Serializing json
        with open(file_path, "w") as file:  # Writing to sample.json
            file.write(json_object)
        file.close()


if __name__ == "__main__":
    pass
