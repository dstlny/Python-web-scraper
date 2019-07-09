import requests
import requests.exceptions
from bs4 import BeautifulSoup
import re
from money_parser import price_str

headers={"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3829.0 Safari/537.36 Edg/77.0.197.1'}

def get_names_and_prices_of_products_on_given_page(page_url, header, write_to_file, element_for_name, name_class, element_for_price, price_class, postage_element="", postage_element_two=""):

    try:
        page = requests.get(page_url, headers=headers)
        soup = BeautifulSoup(page.content, 'lxml')

        strings_from_site = set()

        if not postage_element and not postage_element_two:
            for product_name, product_price in zip(soup.find_all(element_for_name, name_class, recursive=True), soup.find_all(element_for_price, price_class, recursive=True)):
                if product_name and product_price:
                    strings_from_site.add("{} - \"{}\" has a price of £{}".format(page_url,' '.join(product_name.get_text().strip().split()), float(price_str(product_price.get_text()))))
                    print("{} - \"{}\" has a price of £{}".format(page_url,' '.join(product_name.get_text().strip().split()), float(price_str(product_price.get_text()))))
                elif not product_name or not product_price:
                    print("Soup was unable to find the specified tag '<{}>' with an ID or Class of '.{}' and '<{}>' with an ID or Class of '.{}'".format(element_for_name,name_class,element_for_price,price_class))
        else:
            print("got there")
            for product_name, product_price, postage_price in zip(soup.find_all(element_for_name, name_class, recursive=True), soup.find_all(element_for_price, price_class, recursive=True), soup.find_all(postage_element, postage_element_two, recursive=True)):
                if product_name and product_price:
                    strings_from_site.add("{} - \"{}\" has a price of £{} with {}".format(page_url,' '.join(product_name.get_text().strip().split()), float(price_str(product_price.get_text())),postage_price.get_text()))
                    print("{} - \"{}\" has a price of £{} with {}".format(page_url,' '.join(product_name.get_text().strip().split()), float(price_str(product_price.get_text())),postage_price.get_text().strip().replace("\n","").replace("\t","").replace("\r","")))
                elif not product_name or not product_price:
                    print("Soup was unable to find the specified tag '<{}>' with an ID or Class of '.{}' and '<{}>' with an ID or Class of '.{}' and '<{}>' with an ID or Class of '.{}'".format(element_for_name,name_class,element_for_price,price_class, postage_element, postage_element_two))

        if write_to_file:
            for thing in strings_from_site:
                with open("NameAndPriceContent.txt", "a+", encoding="utf8") as f:
                    f.write(thing+"\n")
                    f.close()

    except Exception as exception:
        print("{} has been thrown".format(exception))

def parse_given_xml_for_urls(xml_file, write_to_file, element_for_name, name_class, element_for_price, price_class, postage_element="null", postage_element_two="null"):
    
    try:
        with open(xml_file) as fp:
            soup = BeautifulSoup(fp, 'lxml-xml')

        for url in soup.find_all("loc"):
            get_names_and_prices_of_products_on_given_page(url.get_text(), headers, write_to_file,element_for_name, name_class, element_for_price, price_class,postage_element,postage_element_two)
    
    except Exception as exception:
        print("{} thrown".format(exception))

def do_actions(user_boolean, option, url="null"):

    if int(option) == 1:
        
        try:
            element_name_one = input("Please enter the HTML element that contains the Products Name (e.g: p):\n")
            element_name_two = input("Please enter the class or ID this element has:\n")
            price_element = input("Please enter the HTML element that contains the Products Price (e.g: price):\n")
            price_element_two = input("Please enter the class or ID this element has:\n")
            postage = input("Does this site have postage price: Y or N\n")

            if postage == 'Y':
                postage_element = input("Please enter the HTML element that contains the Products Postage Price (e.g: postage):\n")
                postage_element_two = input("Please enter the class or ID this element has:\n")
            else:
                postage_element = ""
                postage_element_two = ""

            parse_given_xml_for_urls(url, user_boolean, element_name_one, element_name_two, price_element, price_element_two, postage_element, postage_element_two)

        except Exception as exception:
            print("{} has been thrown".format(exception))

    elif int(option) == 2:
        
        try:

            element_name_one = input("Please enter the HTML element that contains the Products Name (e.g: p):\n")
            element_name_two = input("Please enter the class or ID this element has:\n")
            price_element = input("Please enter the HTML element that contains the Products Price (e.g: price):\n")
            price_element_two = input("Please enter the class or ID this element has:\n")
            postage = input("Does this site have postage price: Y or N\n")

            if postage == 'Y':
                postage_element = input("Please enter the HTML element that contains the Products Postage Price (e.g: postage):\n")
                postage_element_two = input("Please enter the class or ID this element has:\n")
            else:
                postage_element = ""
                postage_element_two = ""
            
            get_names_and_prices_of_products_on_given_page(url, headers, user_boolean, element_name_one, element_name_two, price_element, price_element_two, postage_element, postage_element_two)

        except Exception as exception:
            print("{} has been thrown".format(exception))

    else:
        print("{} is an incorrect option".format(option)) 

print("If the script exits without warning after picking website etc, this means one of two things:\n1. The site uses Javascript to dynamically build it's pages, which means we cannot request that page unless you know the specific URL it uses to do so.\n2. The tags/classes you entered do not exist on the page you specified, thus crashing the script..")
option = input("Choose an option:\n1: Import from XML\n2. Import from single URL\n")

if int(option) == 1:
    print('You have chosen to import based on a generated XML file.\n------------------')
    XML = input('Input the name of the XML file produced by https://www.xml-sitemaps.com/: ')

    user_confirm = input("Would you like to output this to a file, or not? Y or N\n")
    
    if user_confirm == 'Y':
        do_actions(True, 1, XML)
    elif user_confirm == 'N':
        do_actions(False, 1, XML)  
    else:
        print("{} is an incorrect option".format(user_confirm))  

elif int(option) == 2:
    print('You have chosen to import pased on a single URL.\n----------------------')

    user_URL = input("What is the URL you would like to import the Products/Prices of?\n")

    user_confirm = input("Is this URL correct?: \"{}\"\nY or N\n".format(user_URL))

    if user_confirm == 'Y':

        user_confirm = input("Would you like to output this to a file, or not?\nY or N\n")
        
        if user_confirm == 'Y':
           do_actions(True, 2, user_URL)
        elif user_confirm == 'N':
           do_actions(False, 2, user_URL)
        else:
            print("{} is an incorrect option".format(user_confirm))

    else:
        confirm = input("Please type the correct URL:\n")
        user_confirm = input("Would you like to output this to a file, or not?\nY or N\n")
        
        if user_confirm == 'Y':
            do_actions(True, 2, user_URL)
        elif user_confirm == 'N':
            do_actions(False, 2, user_URL)
        else:
            print("{} is an incorrect option".format(user_confirm))
else:
    print("{} is an incorrect option".format(option))