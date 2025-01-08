# X FORMELY TWITTER Trending Tweets Scraper

A Flask-based web application that scrapes trending tweets using Selenium and ProxyMesh integration.

## Project Overview

This project consists of three main components:
- A Flask web application to serve the interface
- A Selenium-based scraping script for Twitter
- A web interface to display the scraped tweets

## Prerequisites

- Python
- Flask
- Selenium WebDriver
- Chrome/Firefox WebDriver
- ProxyMesh account and credentials
- Required Python packages (see Installation section)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd xscrape
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Project Structure

```
twitter-scraper/
├── app.py              # Flask application
├── selenium_script.py          # Selenium scraping script
├── templates/          # HTML templates
│   └── index.html
├── .env          # Configuration file
└── requirements.txt   # Project dependencies
```

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Access the web interface at `http://localhost:5000`

3. The application will:
   - Connect to Twitter using ProxyMesh
   - Scrape 5 trending tweets
   - Display them on the web interface

## Features

- Proxy rotation using ProxyMesh
- Real-time tweet scraping
- Web interface for viewing results
- Error handling and retry mechanism
- Rate limiting compliance

## Configuration

### ProxyMesh Setup
- Update `.env` with your ProxyMesh credentials
- Configure proxy endpoints in the scraping script
- Adjust request timeout settings if needed

### Selenium Configuration
- Supports both Chrome and Firefox WebDrivers
- Configurable wait times and retry attempts
- Custom user agent settings

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Disclaimer

This tool is for educational purposes only. Ensure compliance with Twitter's Terms of Service and rate limiting policies when using this scraper.
