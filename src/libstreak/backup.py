from sqlalchemy import text
from src.libstreak.database.models import engine

with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM user WHERE username = :name"), dict(name="Ashley"))
    print("result=", result.all())
    result = conn.execute(
        text(
            """
        INSERT INTO streak (title, start_date, end_date) 
        VALUES (:title, :start_date, :end_date)
        """
        ),
        {
            "title": "365 Days of Code2",
            "start_date": "2023-01-01 00:00:00",
            "end_date": "2023-12-31 00:00:00",
        },
    )
    print("result1=", result.lastrowid)
    result = conn.execute(
        text(
            """
        INSERT INTO streak (title, start_date, end_date) 
        VALUES (:title, :start_date, :end_date)
        """
        ),
        {
            "title": "365 Days of Code4",
            "start_date": "2023-01-01 00:00:00",
            "end_date": "2023-12-31 00:00:00",
        },
    )
    print("result1=", result.lastrowid)


# 0 Timestamp
# 1 Your beautiful name
# 2 University
# 3 Graduation year?
# 4 Degree title?
# 5 Whatsapp number (format +92300123456789)
# 6 linkedIn profile link
# 7 codeforces/leetcode profile link
# (create a one if you dont have or just sign in using google account https://codeforces.com/)
# 8 company if working + experience in years

# conn.execute(text("CREATE TABLE example (id INTEGER, name VARCHAR(20))"))
# conn.execute(text("INSERT INTO example (name) VALUES (:name)"), {"name": "Ashley"})
# conn.execute(text("INSERT INTO example (name) VALUES (:name)"),
# [{"name": "Barry"}, {"name": "Christina"}])
# conn.commit()

# with Session(engine) as session:
#     session.commit()
