import random
from string import ascii_lowercase, digits
import requests
from bs4 import BeautifulSoup


def valid_email(email):
    """The function checks if the email is legal."""
    if len(email.split("@")) == 2:
        if email.split("@")[0] != "" and email.split("@")[1] != "" and "." in email.split("@")[1]:
            if len(email.split("@")[1].split(".")) == 2 and email.split("@")[1].split(".")[1] != "":
                print(email.split("@")[1].split("."))
                return True
    return False


def get_random_string(length):
    """The function gets number of letters and return random string include numbers and chars"""
    return ''.join(random.choice(ascii_lowercase + digits) for _ in range(length))


def get_app_details(app_url):
    """The function gets app url and return his details from play store."""
    try:
        app_page = requests.get(app_url)
        # Provide the app page content to BeautifulSoup parser
        soup = BeautifulSoup(app_page.content, 'html.parser')
        # Get value from meta tag rating
        ratings_value = soup.find("meta", {"itemprop": "ratingValue"})['content']
        ratings_count = soup.find("meta", {"itemprop": "ratingCount"})['content']
        # Get value by attribute
        num_downloads = soup.find("div", {"itemprop": "numDownloads"}).text
        num_downloads_abs = num_downloads.split("-")[1]
        app_details = {'rating': float(ratings_value), 'rated_by': int(ratings_count),
                       'downloads': int(num_downloads_abs.replace(" ", "").replace(",", "")),
                       'downloads_range': num_downloads}
        return app_details
    except AttributeError:
        return None
    except TypeError:
        return None
