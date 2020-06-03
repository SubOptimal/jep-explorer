#!/usr/bin/env python3

import json
import re
import requests
import sys
from bs4 import BeautifulSoup
from operator import itemgetter


def get_numeric_version(event):
    result = re.search(r"(\d+)(\D*)(\d*)", event)
    if result is None:
        value = 999
    else:
        if result.group(3) != '':
            value = int(result.group(1)) + int(result.group(3))/100.0
        else:
            value = int(result.group(1))
    return value


def main():
    jeps = _jep_info()
    possible_statuses = list(set([p['Status'] for p in jeps]))
    possible_releases = list(set([p['Release'] for p in jeps if 'Release' in p]))
    possible_types = list(set([p['Type'] for p in jeps]))

    possible_statuses.sort()
    possible_releases.sort(key=get_numeric_version, reverse=True)
    possible_types.sort()

    out = {
       'possible_statuses': possible_statuses,
       'possible_releases': possible_releases,
       'possible_types': possible_types,
       'jeps': jeps
    }

    with open('index.json', 'w+') as index_json:
        index_json.write(json.dumps(out, indent=4, separators=(',', ': ')))


def _jep_info():
    page = requests.get('http://openjdk.java.net/jeps/0')
    if page.status_code != 200:
        print(f"failed to get JEP index: HTTP status code {page.status_code}")
        sys.exit(1)

    soup = BeautifulSoup(page.content, 'html.parser')
    table_jeps = soup.find(class_="jeps")
    jeps = []
    for row in table_jeps.find_all('tr'):
        jep_number = row.find(class_='jep').text.strip()
        if len(jep_number) != 3:
            print(f"skip JEP: {jep_number}")
            continue
        jep = {'Number': jep_number}
        for span in row.find_all('span'):
            key, value = span.attrs['title'].split(':')
            jep[key] = value.strip()
        link = row.find('a')
        jep_link = link.attrs['href']
        jep['URL'] = jep_link
        jep_title = link.text.strip()
        jep['Title'] = jep_title
        jeps.append(jep)
    jeps = sorted(jeps, key=itemgetter('Number'), reverse=True)
    return jeps


if __name__ == "__main__":
    main()
