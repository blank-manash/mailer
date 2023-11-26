# Daily Mailer Project

This Python application automatically generates and sends a daily email. It leverages OpenAI's GPT-3.5 model to create personalized content, encompassing various sections like current affairs, international news, historical facts, and quizzes.

## Features

- Personalized Greetings: Generates a daily greeting using OpenAI's GPT-3.5.
- Current Affairs: Includes both recent and international current affairs.
- Historical Facts: Adds interesting historical facts of the day.
- Daily Quiz: Incorporates a quiz section.
- Customized Conclusion: Concludes with a personalized message.
- Email Integration: Builds and sends the email automatically.

## Setup

To get started with this project, follow these steps:

1. Install Dependencies:
   Ensure Python is installed, then install required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. OpenAI API Key:
   Obtain an API key from OpenAI. Place this key in the config.py file:
   ```python
   OPENAI_API_KEY = "your_api_key_here"
   ```

3. Email Configuration:
   Configure the email settings in email_builder.py to specify sender and recipient details.

4. Logging Setup:
   The application uses Python's logging framework. Configure this as needed for your application.

## Usage

Execute the main script to generate and send the email:

python main.py

## Components

- main.py: Main script that orchestrates the email building and sending process.
- config.py: Contains configuration settings, including the OpenAI API key.
- current_affairs.py: Fetches current affairs data.
- email_builder.py: Module for building and sending the email.
- openai.py: Wrapper for OpenAI's API.

## Customization

You can modify the content generation by changing the prompts in main.py. Adjust the sections according to your preferences.

## Notes

- Ensure that your usage of the OpenAI API is within your subscription plan limits.
- Test the email functionality thoroughly to ensure proper and responsible usage.

## Disclaimer

This project is intended for personal use and as a demonstration. Be mindful of ethical considerations when sending automated emails.

## Author

Manash
