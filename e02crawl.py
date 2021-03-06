#!/usr/bin/env python3

"""
./e02crawl.py http://camlistore.org 2
Found 37 urls
Depth  0  http://camlistore.org/                                   3681 bytes
Depth  1  http://camlistore.org/code                               4237 bytes
Depth  1  http://camlistore.org/community                          2180 bytes
...
"""

from sys import argv

from e01extract import canonicalize, extract


def extract_multi(to_fetch, seen_urls):
    results = []
    for url in to_fetch:
        if url in seen_urls: continue
        seen_urls.add(url)
        try:
            results.append(extract(url))
        except Exception:
            continue
    return results


def crawl(start_url, max_depth):
    seen_urls = set()
    to_fetch = [canonicalize(start_url)]
    results = []
    for depth in range(max_depth + 1):
        batch = extract_multi(to_fetch, seen_urls)
        to_fetch = []
        for url, data, found_urls in batch:
            results.append((depth, url, data))
            to_fetch.extend(found_urls)

    return results


def print_crawl(result):
    result.sort()
    print('Found %d urls' % len(result))
    for depth, url, data in result:
        print('Depth %2d  %-50s %10d bytes' % (depth, url, len(data)))


def main():
    result = crawl(argv[1], int(argv[2]))
    print_crawl(result)


if __name__ == '__main__':
    main()
