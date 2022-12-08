import requests
from bs4 import BeautifulSoup
from csv import writer

start_url="https://shop.marketorganics.com.au/search?page=1&q=&utf8=%E2%9C%93"
list_url=[start_url]
list_items=[]
for url in list_url:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    lists = soup.find_all('div', class_="TalkerGrid__Item")
    print('Page: ', url)

    with open('marketorganics_com_au.csv', 'w', encoding='utf8', newline='') as f:
        thewriter = writer(f)
        header = ['Title', 'Weak', 'Price', 'Origin of the product']
        thewriter.writerow(header)
        try:
            for list in lists:
                title = list.find('div', class_="talker__name").text.replace('\n', '').replace(" ", '')
                weak = list.find('span', class_="weak size")
                price = list.find('span', class_="talker__prices__sell").text.replace('\n', '').replace(" ",'')
                label=list.find('div', class_="talker__banner")

                if weak != None:
                    weak=weak.text.replace('\n', '').replace(" ",'')
                else:weak=0

                if label!=None:
                    label=label.text.replace('\n', '').replace(" ",'')
                else:label='Unknown origin.'

                item=[title,weak,price[1:-4],label]
                list_items.append(item)
                print(item)
            for row in list_items:
                thewriter.writerow(row)
            print("---------------------------------------------------------------------------------------------")
            try:
                a_href = soup.find("a", {"class": "next_page"}).get("href")
                next_url = "https://shop.marketorganics.com.au" + a_href
                list_url.append(next_url)
            except:print("There are no more pages at website.")
        except:print("Web Scraper can not access data")
