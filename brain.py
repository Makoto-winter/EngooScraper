from pymongo import MongoClient
import atexit, scrape, emailing, os, datetime
from dotenv import load_dotenv
load_dotenv()
import connectToMongo
from apscheduler.schedulers.background import BackgroundScheduler

intervalMinute = 2

test_client = MongoClient(os.getenv('ATLAS_URI'))

tutor_db = test_client['tutorDB']
data = connectToMongo.ConnectToMongo()

def brain():
    print(datetime.datetime.now(), " Brain initiated")
    # 👇collection for one user(collection name = user_email)
    for user_email in tutor_db.list_collection_names():
        slot_increased_tutor_list = []

        # 👇Scraping each tutor for this user(uer_email)
        tutors_col = tutor_db[user_email]
        if user_email != "col_login":
            for tutor in tutors_col.find():
                slots = scrape.get_all_slots(tutor['tutorID'])
                # comparing the number of slots now with the previous one. And return True or False
                if data.IsIncreased(slots, tutor['tutorID'], user_email):
                    slot_increased_tutor_list.append({"tutorName": tutor["tutorName"], "slots": tutor["slots"]})
                else:
                    pass
                    # print(f"For the user: {user_email}. No increased slots: {tutor['tutorName']}")

            if slot_increased_tutor_list:
                print(f"For the user: {user_email}. Some slots increase!! {slot_increased_tutor_list}\n"
                      f"Sending an email.")
                # Email sending
                emailing.send_email(os.getenv("MY_EMAIL"), os.getenv("MY_EMAIL_PASSWORD"), user_email,
                                    slot_increased_tutor_list)


def executeEveryXminute():
    scheduler = BackgroundScheduler()
    # scheduler.add_job(brain, 'cron', minute="*")
    scheduler.add_job(brain, 'interval', minutes=intervalMinute)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown(wait=False))
