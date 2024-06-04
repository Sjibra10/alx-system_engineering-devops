#!/usr/bin/python3
"""main functoin"""

import requests


def count_words(subreddit, word_list, after=None, word_count={}):
    """
    Queries the Reddit API, parses the titles of hot articles, and prints
    a sorted count of given keywords (case-insensitive, delimited by spaces).
    """

    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {'User-Agent': 'python:count_words:v1.0 (by /u/yourusername)'}
    params = {'limit': 100, 'after': after}

    try:
        response = requests.get(url, headers=headers, params=params, allow_redirects=False)
        if response.status_code != 200:
            return

        data = response.json().get('data', {})
        children = data.get('children', [])
        after = data.get('after', None)

        for child in children:
            title = child.get('data', {}).get('title', "").lower().split()
            for word in word_list:
                word = word.lower()
                count = title.count(word)
                if count > 0:
                    if word in word_count:
                        word_count[word] += count
                    else:
                        word_count[word] = count

        if after is not None:
            return count_words(subreddit, word_list, after, word_count)
        else:
            sorted_words = sorted(word_count.items(), key=lambda x: (-x[1], x[0]))
            for word, count in sorted_words:
                print(f"{word}: {count}")

    except Exception as e:
        return
