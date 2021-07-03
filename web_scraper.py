import requests  #installing/importing library to our code
from bs4 import BeautifulSoup
import pandas
import argparse
import connect #importing our connect.py as also a library

parser = argparse.ArgumentParser()                            #creating an object called parser to access web

parser.add_argument("--page_num_max", help="Enter the number of pages to parse", type=int)  #giving a parameter to get no.page to scrap data
parser.add_argument("--dbname", help="Enter the number of pages to parse", type=int)
args = parser.parse_args()

oyo_url = "https://www.oyorooms.com/hotels-in-bangalore/?page="        #url of the webpage to be scraped
page_num_max = args.page_num_max                                       #getting the max. page number
scraped_info_list = []                                                 #creating an empty list
connect.connect(args.dbname)

for page_num in range(1,page_num_max):                                #creating an for loop to access each of the following pages
  
    url = oyo_url + str(page_num)                                
    req = requests.get(url)
    content = req.content


    soup = BeautifulSoup(content, "html.parser")                      #creating an object to access BeautifulSoup

    all_hotels = soup.find_all("div", {"class": "hotelCardListing"})  #using inbuilt function 'find_all' to access every particulars in webpage


    for hotel in all_hotels:
        hotel_dict = {} #creating an empty dictionary
        hotel_dict["name"] = hotel.find("h3", {"class": "listingHotelDescription_hotelName"}).text #adding the necessaries according to their locations specified
        hotel_dict["address"] = hotel.find("span", {"itemprop": "streetAddress"}).text
        hotel_dict["price"] = hotel.find("span", {"class": "listingPrice_finalPrice"}).text
        # try and except
        try:
            hotel_dict["rating"] = hotel.find("span", {"class": "hotelRating_ratingSummary"}).text #this in case if some hotels doesn't have ratings
                                                                                                    #ignore!(but don't terminate)

        except AttributeError:
            pass

        parent_amenities_element = hotel.find("div", {"class": "amenityWrapper"})              #amenities as header

        amenities_list = []
        for amenity in parent_amenities_element.find_all("div", {"class": "amenityWrapper_amenity"}): #getting few amenities by for loop
            amenities_list.append(amenity.find("span", {"class": "d-body-sm"}).text.strip())

        hotel_dict["amenities"] = ', '.join(amenities_list[:-1])

        scraped_info_list.append(hotel_dict)
        connect.insert_info_table(args.dbname, tuple[hotel_dict.values()])

dataFrame = pandas.DataFrame(scraped_info_list)                                              #accessing pandas 
print("Creating csv file....")
dataFrame.to_csv("Oyo.csv")
connect.get_hotel_info(args.dbname)
