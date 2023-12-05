import streamlit as st 
import pandas as pd 
from pandas import Series, DataFrame
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot  as plt



@st.cache_data
#Using python function to scrape through CoinMarketCap
def load_data():
    #Scraping the CoinMarket Currencies
    html_text = requests.get('https://coinmarketcap.com/').text
    soup = BeautifulSoup(html_text, 'html.parser')
    #Identifying the Scrape Tags
    Crypto_name = soup.find_all('p', class_ = "sc-4984dd93-0 kKpPOn")
    parent_div = soup.find_all('div', class_="sc-a0353bbc-0 gDrtaY")
    Crypto_prices = []
    # Loop through each div element in parent_div
    for div in parent_div:
        # Find all span elements within the current div
        span_elements = div.find_all("span")
        # Extract and append text from each span element to Crypto_prices
        for span in span_elements:
            Crypto_prices.append(span.text)

    Market_cap = soup.find_all('span', class_ = "sc-7bc56c81-0 dCzASk")
    Crypto_volume24 = soup.find_all('p', class_ = "sc-4984dd93-0 jZrMxO font_weight_500")

    #Creating New Variables
    CryptoName = []
    MarketCap = []
    CryptoVolume24H = []
    CryptoPrice = []
    CirculatingSupply = []
    # Iterate over each element and extract its text
    for element in Crypto_name:
        CryptoName.append({'text': element.text})

  
    for element in Market_cap:
        MarketCap.append({ 'text': element.text})

    for element in Crypto_volume24:
        CryptoVolume24H.append({'text': element.text})

    for element in Crypto_prices:
        CryptoPrice.append(element)

    #New Variables for Values
    Name = []
    Price = []
    Volume = []
    Market = []

    # The Crypto Name

    #Looping all Crypto Names and appending
    for result in CryptoName:
        Name.append(result['text'])

    # The Crypto Market Cap
    #Looping all MarketCap and appending
    for result in MarketCap:
        Market.append(result['text'])

    # The Crypto Volume 24 hours
    #Looping all Crypto volume24 and appending
    for result in CryptoVolume24H:
        Volume.append(result['text'])

    #The Crypto Prices
    #Looping all Crypto prices and appending
    for result in CryptoPrice:
        Price.append(result)

    Crypto = {'Crypto Name':[], 'Crypto Price':[], 'Crypto 24Hour Volume': [], 'Crypto Market Cap': []}

    for data in Name:
        Crypto['Crypto Name'].append(data)
    
    for data in Price:
        Crypto['Crypto Price'].append(data)
    
    for data in Volume:
        Crypto['Crypto 24Hour Volume'].append(data)
    
    for data in Market:
        Crypto['Crypto Market Cap'].append(data)



    
    return Crypto

df = load_data()



col1, col2 = st.columns(2)

with col1:
    #The Page info page
    st.write("""
    # CoinMarketCap
    Shown are the info about each crypto
    ### This Data was Web Scraped From coinmarketcap.com
    """)

with col2:
    st.image("images.png")






st.dataframe(data=df,use_container_width=True)
    

col1, col2 = st.columns(2)


st.write("""
 
 ### CRYPTO CURRENCIES MARKET PRICE TREND
 """)
fig, ax = plt.subplots()
fig.set_size_inches(13, 10)
ax.bar(df["Crypto Name"], df["Crypto Market Cap"])
st.pyplot(fig)
    



