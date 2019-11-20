#   https://developer.github.com/v3/repos/commits/
import requests
import json
import pandas as pd
pd.set_option('display.max_columns', None)
username = 'haggarw3'
token = '624e7438f0e5eea7fac6bfe560bd5f029cd1e6c8'
gh_session = requests.Session()
gh_session.auth = (username, token)
url = 'https://api.github.com/repos/ironhack-datalabs/madrid-oct-2018/forks'
forks = json.loads(gh_session.get(url).text)
print(forks)

# Challenge 1: Fork Languages
import pandas as pd

# 1. Obtain the full list of forks created from the main lab repo via Github API.
url = 'https://api.github.com/repos/ironhack-datalabs/madrid-oct-2018/forks'
forks = json.loads(gh_session.get(url).text)

# 2. Loop the JSON response to find out the language attribute of each fork.
# Use an array to store the language attributes of each fork.
langs = []
for fork in forks:
    langs.append(fork['language'])

# langs = [fork['language'] for fork in forks]
# 3.Print the language array. It should be something like:
print(langs)
print(set(langs))


# Challenge 2: Count Commits

# 1. Obtain all the commits made in the past week via API,
# which is a JSON array that contains multiple commit objects.
# 2. Count how many commit objects are contained in the array.

# Get commits made this year, since no commits have been made in the last week
d = '2019-01-01'
total_commits = 0

for fork in forks:
    commit_url = (fork['commits_url'].replace("{/sha}", "") + '?since=' + d)
    commits = json.loads(gh_session.get(commit_url).text)
    for commit in commits:
        total_commits += 1

print(total_commits)

repo_url = 'https://api.github.com/repos/ironhack-datalabs/scavenger'
tree_sha = '9308ccc8a4c34c5e3a991ee815222a9691c32476'
condition = '?recursive=1'
url = repo_url + '/git/trees/' + tree_sha + condition
trees = json.loads(gh_session.get(url).text)
data = pd.DataFrame(trees)

from pandas.io.json import json_normalize
flattened_data_tree = json_normalize(data['tree'])
print(flattened_data_tree['path'])
scavenger_files = []
for file in flattened_data_tree['path']:
    if '.scavengerhunt' in file:
        scavenger_files.append(file)
print(scavenger_files)

#  Note that these files are not arranged in an order. First we need to arrange the files
#  from .0001 to later files and then extract the information in the files

import re
order = []
pattern = '\.\d+'
for file in scavenger_files:
    order.append(re.findall(pattern, file)[0])
files_df = pd.DataFrame(scavenger_files, columns=['FilePath'])
files_df['OrderNumbers'] = order
files_df = files_df.sort_values('OrderNumbers', ascending=True)
print(files_df.head())

content = []
import base64
for file in files_df['FilePath']:
    url = repo_url+'/contents/'+file
    message = json.loads(gh_session.get(url).text)
    message = base64.b64decode(message['content']).decode("utf-8").rstrip()
    content.append(message)
print(content)
print(" ".join(content))
