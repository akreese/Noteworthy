import requests
from bs4 import BeautifulSoup
from pprint import pprint
import time

SCRAPE = True
FILTER = True

def parse_genres():
    r = requests.get("https://www.webtoons.com/en/genre#")
    soup = BeautifulSoup(r.content, "html.parser")
    cards = soup.find("div", class_= "card_wrap genre").find_all("ul", class_="card_lst")
    return [li.get("href") for c in cards for li in c.find_all("a")]

def parse_webtoons(batch):
    f = open("./webtoons.json", "a")
    for url in batch:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        genre = soup.find("div", class_="info").find("h2").text
        title = soup.find("meta", property="og:title")['content'].strip()
        author = soup.find("meta", property="com-linewebtoon:webtoon:author")['content'].strip()
        desc = soup.find("meta", property="og:description")['content'].strip()
        data = dict(title=title, genre=genre, author=author, description=desc)
        f.write(f"\n\t{data},")
    f.close()

if SCRAPE:
    BATCH_SIZE = 50
    OFFSET = open("./webtoons.json", "r").read().count("{")
    WEBTOONS = parse_genres()
    BATCHES = [WEBTOONS[i:i+BATCH_SIZE] for i in range(OFFSET, len(WEBTOONS), BATCH_SIZE)]

    if BATCHES:
        print(f"TOTAL BATCHES: {len(BATCHES)}")

        if OFFSET == 0:
            f = open("./webtoons.json", "w")
            f.write("DATA = [")
            f.close()

        for i, BATCH in enumerate(BATCHES):
            parse_webtoons(BATCH)
            print(f"BATCH {i+1} OF {len(BATCHES)} COMPLETED")
            time.sleep(20)
        # close list after all data parsed
        open("./webtoons.json", "a").write("\n]")

if FILTER: # filters out duplicates
    from webtoons import DATA
    INDEX = set()
    RESULT = list()
    for i, d in enumerate(DATA):
        meta = (d['title'], d['genre'], d['author'], d['description'])

        if meta not in INDEX:
            INDEX.add(meta)
            RESULT += [d]
    open("webtoons.json", "w").write(f"{RESULT}")




# BLOB = []


# def parse_genre_list():
#     # Making a GET request
#     r = requests.get("https://www.webtoons.com/en/genre#")

#     # Parsing the HTML
#     soup = BeautifulSoup(r.content, "html.parser")

#     # Finding by id
#     s = soup.find("div", class_= "card_wrap genre")

#     # Getting the card_lst
#     cardlst = s.find_all("ul", class_="card_lst")

#     # All the li under the above ul
#     # for cl in cardlst:
#     #     for li in cl.find_all("a"):
#     #         print(li.get("href"))

#     return [li.get("href") for cl in cardlst for li in cl.find_all("a")]


# def parse_webtoon(url):
#     # Making a GET request
#     r = requests.get(url)
#     soup = BeautifulSoup(r.content, "html.parser")

#     webtoon = {}

#     genre = soup.find("div", class_="info")
#     webtoon["genre"] = [g.text for g in genre.find_all("h2")][0]

#     title = soup.find("meta", property="og:title")
#     webtoon["title"] = title["content"]

#     author = soup.find("meta", property="com-linewebtoon:webtoon:author")
#     webtoon["author"] = author["content"]

#     description = soup.find("meta", property="og:description")
#     webtoon["description"] = description["content"]

#     BLOB.append(webtoon)
#     return


# webtoons = parse_genre_list()

# for url in webtoons[:100]:
#     parse_webtoon(url)

# print(BLOB)

# Run below in terminal to print stdout to a file called webtoons.json
# To append use ' >> ', to overwrite use ' > '
# python webscraper.py > webtoons.json