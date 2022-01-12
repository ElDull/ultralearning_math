import wget
import requests
from bs4 import BeautifulSoup

all_exams = {"Solutions": [], "Exams": []}
ids = ("35581", "35582", "35807", '35806')

def extract_exam_name(link):
    elements = link[8:].split("/")
    year = elements[3]
    month = elements[4]
    name = elements[5]
    return f"{year}-{month}-{name}"

def scrape_all_links(term, year):
    downloads = []
    base_url = f"https://www.geva.co.il/solution_term/math_{str(year)}_{term}/"
    response = requests.get(base_url).text
    html = BeautifulSoup(response, features="html.parser")
    pdf_items = html.find_all("li", {'class':'pdf-item'})

    for item in pdf_items:
        curr_item = item.find('span', {'class':"first-line"}).text
        for identifier in ids:
            if identifier in curr_item:
                links = [i['href'] for i in item.find_all('a')]
                all_exams["Solutions"].append((extract_exam_name(links[0]),links[0]))
                all_exams["Exams"].append((extract_exam_name(links[1]),links[1]))

def get_all_links():
    start_y, end_y = (2018,2022)
    terms = ('summer', 'winter')
    for y in range(start_y, end_y):
        for t in terms:
            result = scrape_all_links(t, y)

def download_file(filename, link, dest):
     r = requests.get(link)
     open(f"{dest}/{filename}", 'wb').write(r.content)
     
get_all_links()

for tup in all_exams["Solutions"]:
    download_file(tup[0],tup[1],"Solutions")
for tup in all_exams["Exams"]:
    download_file(tup[0],tup[1],"Exams")