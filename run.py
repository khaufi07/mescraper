# module
import requests
from bs4 import BeautifulSoup
import csv
import time
import random

# Fungsi untuk mendapatkan konten halaman
def get_page_content(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Failed to retrieve page: {url}")
        return None

# Fungsi untuk mem-parse konten halaman dan mengambil data yang diinginkan
def parse_page_content(content):
    soup = BeautifulSoup(content, 'html.parser')
    data = []
    items = soup.find_all('div', class_='item')  # Sesuaikan dengan struktur HTML target
    for item in items:
        title = item.find('h2').text.strip() if item.find('h2') else 'N/A'
        price = item.find('span', class_='price').text.strip() if item.find('span', class_='price') else 'N/A'
        data.append({
            'title': title,
            'price': price
        })
    return data

# Fungsi untuk menyimpan data ke file CSV
def save_to_csv(data, filename):
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

# Fungsi utama untuk scraping beberapa halaman
def scrape_multiple_pages(base_url, num_pages, output_file):
    all_data = []
    for page in range(1, num_pages + 1):
        url = f"{base_url}?page={page}"
        print(f"Scraping page {page}: {url}")
        content = get_page_content(url)
        if content:
            page_data = parse_page_content(content)
            all_data.extend(page_data)
        time.sleep(random.uniform(1, 3))  # Random delay between requests to avoid being blocked
    save_to_csv(all_data, output_file)
    print(f"Scraping completed. Data saved to {output_file}")

if __name__ == "__main__":
    BASE_URL = 'https://example.com/products'  # Ganti dengan URL target
    NUM_PAGES = 5  # Tentukan berapa banyak halaman yang ingin di-scrape
    OUTPUT_FILE = 'scraped_data.csv'
    scrape_multiple_pages(BASE_URL, NUM_PAGES, OUTPUT_FILE)
