import requests
import bs4
import lxml
import pandas as pd


def snapdeal_search_product(search_term,gender):

    response=requests.get("https://www.snapdeal.com/search?clickSrc=top_searches&keyword="+search_term+"%20for%20"+gender+"&categoryId=0&vertical=p&noOfResults=20&SRPID=topsearch&sort=rlvncy")
    URL=("https://www.snapdeal.com/search?clickSrc=top_searches&keyword="+search_term+"%20for%20"+gender+"&categoryId=0&vertical=p&noOfResults=20&SRPID=topsearch&sort=rlvncy")
    # response= ("https://www.snapdeal.com/search?clickSrc=top_searches&keyword="+search+"%20for%20"+gender+"&categoryId=0&vertical=p&noOfResults=20&SRPID=topsearch&sort=rlvncy")
    print(URL)
    response=response.text
    data=bs4.BeautifulSoup(response, 'lxml')
    print(data)

    read=data.select('.product-desc-rating')
    print(len(read))

    name=[]
    op=[]
    dp=[]


    for i in read:
    #     product name
        product_name=i.select('.product-title ')
        product_name=product_name[0].getText()
        
    #     original price
        original_price=i.find_all('span','lfloat product-desc-price strike')
        original_price=original_price[0].getText()

    #     discounted price
        discounted_price=i.find_all('span','lfloat product-price')
        discounted_price=discounted_price[0].getText()

    #     append in the list
        name.append(product_name)
        op.append(original_price)
        dp.append(discounted_price)
        
    #picture    
    read1=data.select('.picture-elem')
    pi=[]
    for j in read1:
        img=j.find_all('img')
        for k in img:
    #         get image url
            image=k.get('data-src')
            pi.append(image)
            
    for k in range(len(read)):
        output=name[k]+"  "+op[k]+"  "+dp[k]+"  "+str(pi[k])
        print(output)
    
    dict = {'Product Name': name, 'Original Price': op, 'Discounted Price': dp,'Image Url':pi}
    df=pd.DataFrame(dict)
    df

    filename = search_term +"_"+ gender+"_"+"snapdeal.csv"
    df.to_csv(filename, index=False)