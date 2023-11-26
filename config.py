from enum import Enum
from azure.appconfiguration import AzureAppConfigurationClient


def get_client():
    connection_string = "Endpoint=https://mailer-config.azconfig.io;Id=3SvS;Secret=QYEZZBWH9lOjbDwAOkoL9/G2VnKndhSQMI4kXDEd0lU="
    return AzureAppConfigurationClient.from_connection_string(connection_string)


client = get_client()


def get(key: str) -> str:
    return client.get_configuration_setting(key=key).value


class Emails(Enum):
    ME = "mximpaid@gmail.com"
    GAMAKSHI = "gamakshigama2001@gmail.com"
    MAILER = "gamakshi.mail@gmail.com"


RECIPIENT = Emails.GAMAKSHI.value
USER = Emails.MAILER.value
CC = Emails.ME.value
DEBUG = False if get("DEBUG") == "false" else True


RAPID_API_KEY = get("RAPID-API-KEY")
RAPID_API_HOST = get("RAPID-API-HOST")

PASSWORD = get("PASSWORD")
OPENAI_API_KEY = get("OPEN-API-KEY")
