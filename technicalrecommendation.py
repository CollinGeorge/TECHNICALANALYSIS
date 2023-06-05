# Imports
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Set up chromedriver
options = Options()
options.add_argument("--headless")
webdriver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

# Declare list variable
analysis = []

# Error handling
try:
    # User input
    ticker = input("Enter the ticker symbol: ")

    # Open tradingview's site
    url = "https://www.tradingview.com/symbols/{0}/technicals/".format(ticker)
    webdriver.get(url)
    webdriver.refresh()
    time.sleep(1)

    # Summary
    summary_element = webdriver.find_element(By.CSS_SELECTOR, "span.speedometerTitle-kg4MJrFB")
    summary_text = summary_element.get_attribute('innerHTML')
    summary_text = summary_text.replace('Oscillators', 'Signals')  # Replace text
    analysis.append(summary_text)

    # Counters
    counter_elements = webdriver.find_elements(By.CLASS_NAME, "counterNumber-kg4MJrFB.large-kg4MJrFB")

    # Sell, Neutral, and Buy Signal Counts
    sell_signals = int(counter_elements[0].get_attribute('innerHTML'))
    neutral_signals = int(counter_elements[1].get_attribute('innerHTML'))
    buy_signals = int(counter_elements[2].get_attribute('innerHTML'))
    
    analysis.extend([sell_signals, neutral_signals, buy_signals])

    # Set up DataFrame
    df = pd.DataFrame.from_records([tuple(analysis)], columns=['Summary', '# of Sell Signals', '# of Neutral Signals', '# of Buy Signals'])
    df['Ticker'] = [ticker]

    # Determine overall recommendation based on signal counts
    recommendation = ""
    if sell_signals > buy_signals:
        recommendation = "Sell"
    elif buy_signals > sell_signals:
        recommendation = "Buy"
    else:
        recommendation = "Neutral"

    # Print formatted output
    print("-" * 30)
    print("Ticker\t\t\t", ticker)
    print("-" * 30)
    print(df.set_index('Ticker').T.to_string(index=True, header=False))
    print("-" * 30)
    print("Overall Recommendation:\t", recommendation)
    print("-" * 30)

except Exception as e:
    print(f'Could not get the summary due to {e}')
