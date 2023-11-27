from enum import Enum
from config import *
from current_affairs import CurrentAffairs
from email_builder import EmailBuilder
from datetime import datetime
import logging


def get_days():
    start_date = datetime(2019, 12, 25)
    current_date = datetime.now()
    return (current_date - start_date).days


gpt = get_chat_client(GPTModels.GPT3.value)

mail = EmailBuilder.get_instance()
news = CurrentAffairs()


def add_greeting():
    """
    Function to add a greeting to the mail.
    """
    greeting = gpt(
        """
        Create a greeting for the mail for my Sweetheart. It's daily mail, keep it short and sweet
        Tone: Conversational, Friendly, Human
        DO NOT USE any placeholders. Do not use new lines.
        My Name is Manash.
        """
    )
    mail.append_paragraph(greeting)


def add_summary(prompt):
    mail.append_subheading("Summary")
    summary = gpt(prompt, max_tokens=None)
    mail.append_paragraph(summary)


def store_recent_affairs():
    """
    Function to store the recent affairs in the mail.
    """
    response = news.get_recent_current_affairs()
    if not response:
        return
    mail.append_heading("Recent Current Affairs")
    mail.append_list(response)
    prompt = f"""
Create a Interesting, Informative, Brief and Creative Summary of the above Recent Current Affairs from India
Keep it within 100 words.
This will be an HTML Message, use <br> for break lines.
    {response}
    """
    add_summary(prompt)


def store_international_affairs():
    """
    Function to store the international affairs in the mail.
    """
    response = news.get_international_current_affairs()
    if response:
        mail.append_heading("International Current Affairs")
        mail.append_list(response)

        prompt = f"""
Create a Interesting, Informative, Brief and Creative Summary of the above International Current Affairs.
Keep it within 100 words.
This will be an HTML Message, use <br> for break lines.
        {response}
        """

        add_summary(prompt)


def store_history():
    """
    Function to store the history in the mail.
    """
    items = news.get_history_of_today()
    if items is not None and len(items) > 0:
        mail.append_heading("History")
        content = []
        for item in items:
            info = f"{str(item['date']).strip()}: {str(item['description']).strip()}"
            content.append(info)
        mail.append_list(content)


def store_quiz():
    """
    Function to store the quiz in the mail.
    """
    items = news.get_today_quiz()
    if items is not None and len(items) > 0:
        mail.append_heading("Quiz")
        content = [str(item["question"]).strip() for item in items]
        mail.append_list(content)


def add_conclusion():
    """
    Function to add a conclusion to the mail.
    """
    prompt = f"""Create a conclusion paragraph for a mail for my Sweetheart.
My Name is Manash. DO NOT USE any placeholders, DO NOT USE new lines. DO NOT Introduce
It's daily mail, keep it short and sweet, we met on 25 December 2019, i.e {get_days()} we've met.
Tone: Conversational, Friendly, Human
    """
    conclusion = (
        gpt(prompt)
        + "<br><br> <b>P.S</b>: AI Can be Dumb. Ignore if it's stupid. I still love you. <br>"
    )
    mail.append_paragraph(conclusion)


def main():
    """
    Main function to run the program.
    """
    add_greeting()
    store_recent_affairs()
    store_international_affairs()
    store_history()
    store_quiz()
    add_conclusion()
    mail.send_email()


if __name__ == "__main__":
    main()
