import requests
from bs4 import BeautifulSoup
import pandas as pd


def flipkart_search_product(search_term,gender):
    # Use requests library instead of urllib

    #url2 = "https://www.flipkart.com/search?q="+search_term+"+for+"+gender+"&as=on&as-show=on&otracker=AS_Query_OrganicAutoSuggest_3_6_na_na_na&otracker1=AS_Query_OrganicAutoSuggest_3_6_na_na_na&as-pos=3&as-type=RECENT&suggestionId="+search_term+"+for+"+gender+"&requestId=d64fcf70-081c-4be8-a9bc-7e1c1e1090ad&as-searchtext="+search_term+"%20"
    url = "https://www.flipkart.com/search?q="+search_term+"+for+"+gender+"&as=on&as-show=on&otracker=AS_Query_OrganicAutoSuggest_3_6_na_na_na&otracker1=AS_Query_OrganicAutoSuggest_3_6_na_na_na&as-pos=3&as-type=RECENT&suggestionId="+search_term+"+for+"+gender+"&requestId=d64fcf70-081c-4be8-a9bc-7e1c1e1090ad&as-searchtext="+search_term+"%20"

    # Set user-agent header to avoid being blocked by the website
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

    # Send request with headers
    response = requests.get(url, headers=headers)
    webdata = response.content

    # Use 'html.parser' as the parser
    soupdata = BeautifulSoup(webdata, 'html.parser')

    containers = soupdata.findAll('div', {'class':'_1xHGtK _373qXS'})
    print(len(containers))

    filename = search_term +"_"+ gender+"_"+"flipkart.csv"
    f= open(filename,'wb')
    f.write('productName,currentprice,mrp,imageurl\n'.encode())
    for container in containers:
        # finding product name
        product = container.findAll('div', {'class':'_2WkVRV'})
        if product:
            productName = product[0].text.strip()
        else:
            productName = 'N/A'

        # finding current price
        current = container.find('div', {'class':'_30jeq3'}).text.replace(',','')
        currentprice  = current.replace('₹','')


        # finding mrp
        mrp = container.find('div', {'class':'_3I9_wc'})
        try:
            old = mrp.text.replace(',','')
            MRP = old.replace('₹','')

        except:
            MRP = 0

        

        # finding image url
        image = container.img
        imageurl = image.get('src')

        print(productName, currentprice, MRP, imageurl)
        f.write(f"{productName},{currentprice},{MRP},{imageurl}\n".encode())
        print('\n')
    f.close()
