import neo4j
import requests
from neo4j import GraphDatabase
from bs4 import BeautifulSoup

URI = "neo4j+s://b35e138c.databases.neo4j.io"
AUTH = ("neo4j", "VGfvQTk0VCkEzne79CGPXTKA_Eykhx0OwudLZUKG7sQ")


def add_group(driver, ID):
    try:
        driver.execute_query(
        "Create (g:Group {ID: $name}) ",
        name=ID,database_="neo4j",
    )
    except neo4j.exceptions.ConstraintError:
        print(f"grupa {ID} jest juz w bazie danych")

url = 'https://old.wcy.wat.edu.pl/pl/rozklad'
response = requests.get(url, verify=False)
soup = BeautifulSoup(response.text, 'html.parser')
options = soup.find('select', {"class": "ctools-jump-menu-select form-select"}).find_all('option')
with GraphDatabase.driver(URI, auth=AUTH) as driver:
    for option in options:
        try:
            add_group(driver, option.text.strip())
        except Exception as e:
            print(e)
        finally:
            driver.close()
print("pomyslnie zaaktualizowano nazwy grup")


