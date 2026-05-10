# Hotel Price Scraper

This Python script is designed to automatically scrape hotel prices from Bynd.co.il for specific hotels in Israel, tailored for a family configuration of 2 Adults and 1 Child (age 7). 

The script bypasses SSL inspection issues often triggered by automated scripts and continuously appends its results to a local CSV file for easy comparison.

## Requirements

*   **Python 3.x** must be installed on your machine.
*   No external libraries are required (the script only uses built-in standard Python modules such as `urllib.request`, `re`, `ssl`, and `csv`).

## How to Run

To start the scraper, simply run the script from your terminal:

```bash
python3 hotel_scraper.py
```

## Output

Once the script starts, it will sequentially query the specified dates for each hotel.
1. The terminal will print real-time updates as it checks each hotel and date.
2. The prices are immediately appended to `scraped_prices.csv` in the root directory. 

*Note: The `scraped_prices.csv` file is configured in the `.gitignore` to prevent you from accidentally committing live price data to your repository.*

## Modifying the Search Parameters

If you wish to edit the dates or the hotels being tracked, you will need to open `hotel_scraper.py` and modify the following constants at the top of the file:

**Changing Hotels:**
```python
HOTELS = [
    {"name": "Beresheet", "hid": 1622},
    {"name": "Kedma", "hid": 2442},
    {"name": "Daroma", "hid": 194}
]
```
Add any new hotel by giving it a friendly name and its exact system `hid`.

**Changing Target Dates:**
The script automatically builds a list of dates based on the `WINDOWS` array:
```python
WINDOWS = [
    (datetime.date(2026, 5, 30), datetime.date(2026, 6, 7)),
    (datetime.date(2026, 6, 14), datetime.date(2026, 6, 18)),
]
```
Modify the `datetime.date(YYYY, MM, DD)` entries to set your desired timeframes. The script will automatically scrape prices for every single consecutive night within your specified windows.
