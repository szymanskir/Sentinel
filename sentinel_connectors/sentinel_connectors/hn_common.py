from bs4 import BeautifulSoup


def clean_html(text: str):
    soup = BeautifulSoup(text, features="html.parser")
    return soup.get_text()
