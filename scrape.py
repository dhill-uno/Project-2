import requests
from bs4 import BeautifulSoup
import pandas as pd

"""
extracts the indeed job listing by page numbers and returns the soup, the html webpage
Project inspired from https://www.youtube.com/watch?v=PPcgtx0sI2E&t=797s
"""

def extract(page):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'}
    url = f"https://www.indeed.com/jobs?q=data%20analyst&l=remote&start={page}"
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup


def transform(soup):
    job_div = soup.find_all('div', class_='slider_container')
    for item in job_div:
        title = item.find('h2').text.strip()
        company = item.find('span', class_='companyName').text.strip()
        location = item.find('div', class_='companyLocation').text.strip()
        try:
            salary = item.find('div', class_='attribute_snippet').text.strip()
        except:
            salary = "salary not provided"
        summary = item.find('div', class_='job-snippet').text.strip().replace('\n', '')

        job = {
            'title': title,
            'company': company,
            'location': location,
            'salary': salary,
            'summary': summary
        }
        joblist.append(job)
    return


joblist = []
for i in range(0, 40, 10):
    print(f'Getting page, {i}')
    page = extract(0)
    transform(page)

df = pd.DataFrame(joblist)
df.to_csv('jobs.csv')



