from icecream import ic
from bs4 import BeautifulSoup
from get_html import get_html

myip = '92.241.246.187'


def url_to_csv() -> BeautifulSoup:
    url = "https://www.whatismybrowser.com/detect/what-http-headers-is-my-browser-sending"
    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    return soup


soup = url_to_csv()
print(soup.get_text())