from config import *
import yagmail


class EmailBuilder:
    @staticmethod
    def get_instance():
        return EmailBuilder("Happy Mail")

    def __init__(self, subject):
        self.subject = subject
        self.contents = []
        self.yag = yagmail.SMTP(USER, PASSWORD)

    def append_paragraph(self, text):
        text = str(text).strip()
        self.contents.append(f"<p>{text}</p>")

    def append_heading(self, text, level=2):
        text = str(text).strip()
        self.contents.append(f"<h{level}>{text}</h{level}>")

    def append_subheading(self, text):
        self.append_heading(text, level=3)

    def append_list(self, items):
        items = [str(item).strip() for item in items]
        list_items = "".join([f"<li>{item}</li>" for item in items])
        self.contents.append(f"<ul>{list_items}</ul>")

    def send_email(self):
        recipient = Emails.ME.value if DEBUG else RECIPIENT
        cc = None if DEBUG else CC
        self.yag.send(
            to=recipient, subject=self.subject, contents="".join(self.contents), cc=cc
        )
