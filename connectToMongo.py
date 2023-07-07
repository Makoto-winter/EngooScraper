from pymongo import MongoClient
import scrape, os
from dotenv import load_dotenv
load_dotenv()

class ConnectToMongo:
    def __init__(self):
        # ########## setting MongoDB ############
        self.test_client = MongoClient(os.getenv('ATLAS_URI'))
        self.tutor_db = self.test_client['tutorDB']

    def Add(self, tutor_number, user_email):
        # collection for a user
        self.tutors_col = self.tutor_db[user_email]
        old_dict = {"tutorID": tutor_number}
        new_dict = {"$set": {"tutorID": tutor_number, "tutorName": scrape.get_tutor_name(tutor_number),
                             "slots": scrape.get_all_slots(tutor_number), "number_of_booked_slots": scrape.number_of_booked_classes_of(tutor_number)}}
        # adding the document for the user if the tutor ID does not exist in the collection.
        self.tutors_col.update_one(old_dict, new_dict, upsert=True)

    def Remove(self, tutor_number, user_email):
        # collection for a user
        self.tutors_col = self.tutor_db[user_email]
        self.tutors_col.delete_one({"tutorID": tutor_number})

    def IsIncreased(self, slots_now, tutor_number, user_email):
        # collection for a user
        self.tutors_col = self.tutor_db[user_email]
        try:
            # slots_now.count("\n") is the most recent slots.
            # self.tutors_col.find_one({"... is old because they were stored in DB with Add method.
            if slots_now.count("\n") > self.tutors_col.find_one({"tutorID": tutor_number})["slots"].count("\n"):
                return True
            else:
                return False
        except TypeError as e:  # when adding a tutor for the first time and previous number of slots is not on mongoDB
            print("IsIncreased set True because the tutor was not on the DB. Error message:")
            print(e)
            return True
        finally:
            # replace old slots with new ones on DB.
            self.Add(tutor_number, user_email)
