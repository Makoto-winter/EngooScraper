from bs4 import BeautifulSoup
import requests


def get_all_slots(tutor_number):
    tutors_url = "https://eikaiwa.dmm.com/teacher/index/" + str(tutor_number)
    response = requests.get(tutors_url)
    webpage = response.text

    soup = BeautifulSoup(webpage, "html.parser")

    slots = soup.find_all(name="a", string="予約可")
    all_slots = []

    for slot in slots:
        class_date = slot.parent.parent.findChild('li').getText().replace(' ', '').replace('\n', '') \
            .replace('(月)', ' ').replace('(火)', ' ').replace('(水)', ' ').replace('(木)', ' ').replace('(金)',
                                                                                                         ' ') \
            .replace('(土)', ' ').replace('(日)', ' ') \
            .replace('月', '/').replace('日', '')
        new_class_name = slot.parent['class'][0].replace('t', '').replace('-', '', 1).replace('-', ':')
        all_slots.append(class_date + new_class_name)

    # all_slots is a string
    all_slots = "\n".join(all_slots)

    return all_slots


def number_of_booked_classes_of(tutor_number):
    tutors_url = "https://eikaiwa.dmm.com/teacher/index/" + str(tutor_number)
    response = requests.get(tutors_url)
    webpage = response.text

    soup = BeautifulSoup(webpage, "html.parser")

    taken_slots = soup.find_all(name="span", string="予約済")
    number_of_booked_slots = len(taken_slots)

    return number_of_booked_slots

def get_tutor_name(tutor_number):
    tutors_url = "https://eikaiwa.dmm.com/teacher/index/" + str(tutor_number)
    response = requests.get(tutors_url)
    webpage = response.text

    soup = BeautifulSoup(webpage, "html.parser")
    tutor_name = soup.select_one('.area-detail h1').getText().split("（")[0]
    return tutor_name





