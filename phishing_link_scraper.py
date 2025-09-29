import requests
import csv

PHISHTANK_API_URL = "https://data.phishtank.com/data/online-valid.csv"

def fetch_phishtank_data():
    response = requests.get(PHISHTANK_API_URL)
    response.raise_for_status()
    return response.text.splitlines()

def parse_csv_lines(lines):
    reader = csv.DictReader(lines)
    records = []
    for row in reader:
        records.append({
            "url": row.get("url"),
            "submission_time": row.get("submission_time"),
            "verified": row.get("verified")
        })
    return records

def save_to_csv(records, filename="D:\\Work\DEPI\\Non-Technical\\Assignments\\phishing_urls.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)

def main():
    print("Fetching PhishTank data...")
    lines = fetch_phishtank_data()
    print(f"Fetched {len(lines)-1} records (including header).")
    records = parse_csv_lines(lines)
    save_to_csv(records)
    print(f"Saved {len(records)} records to phishing_urls.csv")

if __name__ == "__main__":
    main()