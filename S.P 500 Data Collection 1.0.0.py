import os
import pandas as pd
import yfinance as yf
import requests
import csv
import time

def main():
    print("S&P 500 Data Collection.")
    print("Version 1.0.0\n")
    copyright_fun()
    data_collection()
    input('Press ENTER to exit the program')

def copyright_fun():
        print("Copyright (c) 2025, Nicholas R Pettit")
        print("nicholas.r.pettit@proton.me")
        print("All rights reserved.")
        print("This version of the software was producted 1 February 2025")
        print("\n")
        print("To view entire copyright information press Y for Yes or N for No.")
        print("Enter Y for yes")
        print("Enter N for no")
        view_copyright = str(input("Enter selection:"))
        print("\n")    


        #Validation loop of the anser given for view_copyright
        #Only accept a capital Y or N right now to move on
        while True:          
        
            if view_copyright == 'N' :
                return

            elif view_copyright == 'Y' :
                print("Redistribution and use in source and binary forms, with or without")
                print("modification, are permitted provided that the following conditions are met:")
                print("\n")
                print("1. Redistributions of source code must retain the above copyright notice, this")
                print("list of conditions and the following disclaimer.")
                print("2. Redistributions in binary form must reproduce the above copyright notice,")
                print("this list of conditions and the following disclaimer in the documentation")
                print("and/or other materials provided with the distribution.")
                print("\n")
                print("THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS ""AS IS"" AND")
                print("ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED")
                print("WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE")
                print("DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR")
                print("ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES")
                print("(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;")
                print("LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND")
                print("ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT")
                print("(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS")
                print("SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.")
                print("\n")
                print("The views and conclusions contained in the software and documentation are those")
                print("of the authors and should not be interpreted as representing official policies,")
                print("either expressed or implied, of the FreeBSD Project.")
                print("\n")
                print("\n")
                return

            elif view_copyright !="N" and view_copyright !="Y":
                print("Yes or No answer only: ")
                print("Enter Y for yes")
                print("Enter N for no")
                view_copyright = str(input("Enter selection:"))
                print("\n")

def fetch_sp500_companies():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    try:
        response = requests.get(url)
        response.raise_for_status()
        tables = pd.read_html(response.text)
        sp500_table = tables[0]
        sp500_companies = sp500_table[sp500_table['Symbol'].str.match(r'^[A-Z]+$')][['Symbol', 'Security']]
        return sp500_companies
    except Exception as e:
        print(f"Error fetching S&P 500 data: {e}")
        return None

def fetch_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="2d")
        if len(hist) < 2:
            return None, None, None, None, None
        prev_close = hist['Close'].iloc[-2]
        pe_ratio = stock.info.get("trailingPE", "N/A")
        gross_profit_margin = stock.info.get("grossMargins", "N/A")
        dividend_rate = stock.info.get("dividendRate", "N/A")
        price_to_book = stock.info.get("priceToBook", "N/A")
        return prev_close, pe_ratio, gross_profit_margin, dividend_rate, price_to_book
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None, None, None, None, None

def save_to_csv(companies, file_name):
    data = []
    for index, row in companies.iterrows():
        ticker = row['Symbol']
        company_name = row['Security']
        prev_close, pe_ratio, gross_profit_margin, dividend_rate, price_to_book = fetch_stock_data(ticker)
        data.append([ticker, company_name, prev_close, pe_ratio, gross_profit_margin, dividend_rate, price_to_book])
        time.sleep(1)  # Avoid hitting API rate limits
    df = pd.DataFrame(data, columns=['Ticker', 'Company Name', 'Previous Close', 'P/E Ratio', 'Gross Profit Margin', 'Dividend Rate', 'Price to Book Ratio'])
    df.to_csv(file_name, index=False)
    print(f"Data saved to {file_name}")

def data_collection():
    companies = fetch_sp500_companies()
    if companies is not None:
        save_to_csv(companies, "S&P 500 Stock Data.csv")

if __name__ == "__main__":
    main()