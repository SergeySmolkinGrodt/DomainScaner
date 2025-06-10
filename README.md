# Domain Scanner Bot

This project is a bot designed to find and register valuable domain names. It automates the process of searching for recently expired domains, generating potential domain names based on trends, and analyzing them for SEO value and availability.

## Features

- **Domain Parser:** Parses lists of expiring and deleted domains.
- **Name Generator:** Generates domain name ideas from various sources (trends, dictionaries, news).
- **Domain Analyzer:** Checks domain availability, SEO metrics (DA/PA), web archive history, and for trademarks.
- **Auto-Registrar:** Automatically registers valuable domains through a registrar's API.

## Project Structure

```
DomainScanner/
├── domainscanner/
│   ├── analyzers/
│   ├── generators/
│   ├── parsers/
│   ├── registrars/
│   ├── utils/
│   └── config.py
├── data/
│   ├── dictionary.txt
│   └── trend_words.txt
├── main.py
├── requirements.txt
└── README.md
``` 