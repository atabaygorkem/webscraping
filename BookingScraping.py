from bs4 import BeautifulSoup
import requests

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}

user_hotel = input("Enter a destination/property: ")
if user_hotel.strip() == "":
    exit()


filename = "comments.csv"
filename2 = "scores.csv"
f = open(filename, "w", encoding='utf-8')
h = open(filename2, "w", encoding='utf-8')
f.write("Hotel Names" + ";" + "Comments" + "\n")
h.write("Hotel Names" + ";" + "Staff" + ";" + "Facilities" + ";" + "Cleanliness" + ";" + "Comfort" + ";" + "Value for money" + ";" + "Location" + ";" + "Free WiFi" + "\n")

my_url = "https://www.booking.com/searchresults.html?ss=search=" + user_hotel + "&rows=25&offset="

cont = requests.get(my_url + "0").text
contsp = BeautifulSoup(cont, "html.parser")

hotel_title = contsp.find("h1", "sorth1").text.strip()

htlcnt = hotel_title.split(":")[1]
htlnm = hotel_title.split(":")[0]
hotelcnt = int("".join(filter(str.isdigit, htlcnt)))

dest_check = input(f"The destination is {htlnm}, do you want to proceed? (Y/N): ")
if dest_check.lower() != "y":
    exit()
page_input = input(f"How many pages do you want to fetch from {int(hotelcnt/25) + 1} pages? (press Enter for all): ")
if page_input.strip() != "" and page_input.isnumeric():
    hotelcnt = int(page_input)*25
print(hotelcnt)
print("Fetching...")


for p in range(0, hotelcnt, 25):
    url_temp = my_url + str(p)
    r = requests.get(url_temp).text
    soup = BeautifulSoup(r, "html.parser")
    containers = soup.findAll("div", {"class":"sr_property_block"})

    for container in containers:
        hotellink = container.find("a", "sr-review-score__link")["href"].strip()
        t_url = "https://www.booking.com" + hotellink

        rr = requests.get(t_url).text
        comsoup = BeautifulSoup(rr, "html.parser")

        hotelname = comsoup.find("a", attrs = {"id":"hp_hotel_name_reviews"}).text.strip()
        barScores = comsoup.findAll("span", "c-score-bar__score")
        staff =" " +  barScores[0].text.strip().replace(".",",")
        facilities =" " + barScores[1].text.strip().replace(".",",")
        cleanliness =" " +  barScores[2].text.strip().replace(".",",")
        comfort =" " +  barScores[3].text.strip().replace(".",",")
        valueForMoney =" " +  barScores[4].text.strip().replace(".",",")
        location =" " +  barScores[5].text.strip().replace(".",",")

        if len(barScores) == 7:
            freeWiFi =" " +  barScores[6].text.strip().replace(".",",")
        else:
            freeWiFi = "N/A"


        h.write(hotelname + ";" + staff + ";" + facilities + ";" + cleanliness + ";" + comfort + ";" + valueForMoney + ";" + location + ";" + freeWiFi + "\n")

        urlelems = comsoup.find("option", attrs = {"value":"total"})
        cc1 = urlelems["data-cc"]
        dist = urlelems["data-dist"]
        pagename = urlelems["data-pagename"]
        typee = urlelems["data-customer-type"]
        commentQuantity = int(urlelems["data-quantity"])

        tt_url = "https://www.booking.com/reviewlist.tr.html?"
        tt_url += "cc1=" +cc1 + ";dist=" + dist + ";pagename=" + pagename + ";type=" + typee
        tt_url += "&;rows=25;offset="

        lastUrl = tt_url
        for x in range(0, commentQuantity-25, 25):
            temp_url = lastUrl + str(x)
            rss = requests.get(temp_url, headers = headers).text
            tempsoup = BeautifulSoup(rss, "html.parser")

            comments = tempsoup.findAll("span", "c-review__body--original")
            for comment in comments:
                cc = comment.text.strip()
                cc = cc.replace("\n", " ")
                cc = cc.replace("\r", " ")
                cc = cc.replace(";", " ")
                f.write(hotelname + ";" + cc + "###" + "\n")
f.close()
h.close()
