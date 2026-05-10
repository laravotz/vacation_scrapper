import urllib.request
import re
import ssl
import csv
import sys
import time
import datetime

# Hotel Settings
HOTELS = [
    {"name": "Beresheet", "hid": 1622},
    {"name": "Kedma", "hid": 2442},
    {"name": "Daroma", "hid": 194}
]

# Date Windows: 30.5-7.6, 14-18.6, 14-21.7
WINDOWS = [
    (datetime.date(2026, 5, 30), datetime.date(2026, 6, 7)),
    (datetime.date(2026, 6, 14), datetime.date(2026, 6, 18)),
    (datetime.date(2026, 6, 21), datetime.date(2026, 6, 30)),
    (datetime.date(2026, 7, 14), datetime.date(2026, 7, 21))
]

def get_all_dates(windows):
    all_dates = []
    for start, end in windows:
        curr = start
        while curr < end:
            all_dates.append((curr.strftime("%d/%m/%y"), (curr + datetime.timedelta(days=1)).strftime("%d/%m/%y")))
            curr += datetime.timedelta(days=1)
    return all_dates

# Bypass SSL issues
ctx = ssl._create_unverified_context()

def get_price(hid, f, t):
    # Query URL - 2 adults + 1 child (age 7)
    url = f"https://bynd.co.il/israel/details.aspx?fdate={f}&tdate={t}&isdomestic=true&hid={hid}&hotelrooms[0].adults=2&hotelrooms[0].children=1&hotelrooms[0].childages[0]=7"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept-Language': 'he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            prices = re.findall(r'data-price="([\d,]+(?:\.\d+)?)"', content)
            if prices:
                nums = [float(p.replace(',', '')) for p in prices if float(p.replace(',', '')) > 200]
                return int(min(nums)) if nums else "N/A"
            return "Blocked/Min Night"
    except Exception as e:
        return f"Error"

def main():
    print("Starting Comprehensive Hotel Scraper...")
    csv_path = "scraped_prices.csv"
    dates_to_check = get_all_dates(WINDOWS)
    
    with open(csv_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        for fdate, tdate in dates_to_check:
            print(f"\n--- Checking date: {fdate} ---")
            for h in HOTELS:
                print(f"  {h['name']:<15}...", end=" ", flush=True)
                price = get_price(h['hid'], fdate, tdate)
                print(f"Result: {price}")
                writer.writerow([fdate, h['name'], price])
                time.sleep(0.5) # Fast but safe
    
    print(f"\nDone! Results saved to {csv_path}")

if __name__ == "__main__":
    main()
