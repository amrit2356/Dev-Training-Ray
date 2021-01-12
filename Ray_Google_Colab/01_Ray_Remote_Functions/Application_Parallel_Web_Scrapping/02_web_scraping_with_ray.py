"""
Implementation of Github Web Scrapping with Ray.
Goal: 
We break up the process into multiple steps. We first grab the raw HTML of the website using Python's requests package. 
Then, we use BeautifulSoup to parse the HTML to find the relevant information. Finally, we populate a pandas DataFrames 
so that we are able to work with the data.

To demonstrate this, we scrape GitHub commits to see the latest commits on several repositories.

"""
import ray
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup


ray.init()

@ray.remote
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
    df = fetch_commits.remote(repo)
    results.append(df)

results = ray.get(results)    
df = pd.concat(results, sort=False)
duration = time.time() - start
print("Constructing the dataframe took {:.3f} seconds.".format(duration))

print(df)

ray.shutdown()