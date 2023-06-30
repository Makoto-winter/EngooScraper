import smtplib


def send_email(my_email, password, user_email, tutors_list):
    email_text = ""
    for tutor_dict in tutors_list:
        email_text += tutor_dict['tutorName'] + "\n" + tutor_dict['slots'] + "\n\n"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=user_email,
            msg=f"Subject:More slots of your favorite tutor(s) on DMM/Engoo\n\n "
                f"New slots of your favorite tutor\n\n{email_text}"
        )
