import time
import requests
import pandas as pd
from bs4 import BeautifulSoup

def fetch_commits(repo):
    url = 'https://github.com/{}/commits/master'.format(repo)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    df = pd.DataFrame(columns=['title', 'link'])
    for g in soup.find_all(class_='commit-title'):
        entry = {}
        title = g.find_all(class_='message')[0]['aria-label']
        entry['title'] = title
        links = g.find_all(class_='issue-link')
        if len(links) >= 1:
            link = links[0]['data-url']
            entry['link'] = link
        df = df.append(pd.DataFrame(entry, index=[0]), sort=False)
    
    df['repository'] = repo
    return df

start = time.time()
repos = ["ray-project/ray", "modin-project/modin", "tensorflow/tensorflow", "apache/arrow"]
results = []
for repo in repos:
    df = fetch_commits(repo)
    results.append(df)
    
df = pd.concat(results, sort=False)
duration = time.time() - start
print("Constructing the dataframe took {:.3f} seconds.".format(duration))

print(df)