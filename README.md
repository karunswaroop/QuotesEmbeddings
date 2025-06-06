# Instagram Quote Image Downloader

A Python tool to download quote images from Instagram profiles, specifically designed for downloading from @shailosophy.

## Features

- Download all images from an Instagram profile
- Skip video content
- Save metadata for each post
- Command-line interface with options for output directory
- Optional login for private profiles
- Filter posts by date range
- Count images without downloading
- Two different approaches: Instaloader API and Selenium browser automation

## Installation

1. Clone this repository or download the files
2. Install the required dependencies:

```bash
# For the Instaloader approach
pip install -r requirements.txt

# For the Selenium approach (recommended)
pip install selenium webdriver-manager requests pillow
```

## Usage

### Approach 1: Instaloader (May Hit Rate Limits)

To download all images from @shailosophy using the Instaloader approach:

```bash
python instagram_downloader.py shailosophy
```

With login (recommended to avoid rate limits):

```bash
python instagram_downloader.py shailosophy --login
```

You will be prompted to enter your Instagram username and password.

### Approach 2: Selenium (Recommended)

The Selenium approach is more reliable as it simulates a real browser:

```bash
python selenium_instagram_downloader.py shailosophy
```

With login (recommended):

```bash
python selenium_instagram_downloader.py shailosophy --login
```

To see the browser in action (not headless):

```bash
python selenium_instagram_downloader.py shailosophy --login --visible
```

Limit the number of images to download (default is 500):

```bash
python selenium_instagram_downloader.py shailosophy --max-images 100 --download
```

### Count Images Without Downloading

To only count images without downloading them:

```bash
# Count all images from a profile
python selenium_instagram_downloader.py shailosophy

# Count images within a date range
python selenium_instagram_downloader.py shailosophy --start-date "2024-01-01" --end-date "2025-06-05"
```

### Filter by Date Range

Download posts from a specific date range:

```bash
# Download posts from January 1, 2024 to today
python selenium_instagram_downloader.py shailosophy --start-date "2024-01-01" --download

# Download posts between specific dates
python selenium_instagram_downloader.py shailosophy --start-date "2023-06-01" --end-date "2023-12-31" --download

# Combine with login and other options
python selenium_instagram_downloader.py shailosophy --login --start-date "2024-01-01" --end-date "2025-06-05" --visible --download
```

The script supports multiple date formats:
- YYYY-MM-DD (2023-01-31)
- DD-MM-YYYY (31-01-2023)
- YYYY/MM/DD (2023/01/31)
- DD/MM/YYYY (31/01/2023)
- Month DD, YYYY (Jan 31, 2023)
- DD Month YYYY (31 Jan 2023)

### Specify Output Directory (Both Approaches)

```bash
python selenium_instagram_downloader.py shailosophy --output quotes_folder
```

## Handling Instagram Rate Limits

Instagram has strict rate limits and anti-scraping measures. Here are some tips:

1. **Always use the login option** when possible
2. **Use the Selenium approach** for more reliable results
3. **Be patient** - the script includes built-in delays to avoid being blocked
4. **If blocked, wait** several hours before trying again
5. **Consider using a VPN** if you continue to face issues

## How It Works

### Instaloader Approach

The `instagram_downloader.py` script uses the Instaloader library to:
- Authenticate with Instagram (if login provided)
- Access the target profile
- Download posts and metadata

This approach is simpler but more likely to be blocked by Instagram.

### Selenium Approach

The `selenium_instagram_downloader.py` script:
- Controls a real Chrome browser (headless by default)
- Logs in like a real user (if credentials provided)
- Scrolls through the profile page to load images
- Extracts image URLs and downloads them

This approach better mimics human behavior and is less likely to be blocked.

## Notes

- Instagram's website structure may change, which could affect these scripts
- These tools are for educational purposes only
- Please respect Instagram's terms of service and rate limits
- Consider using Instagram's official API for business use cases

## Requirements

- Python 3.6 or higher
- For Instaloader approach: instaloader library
- For Selenium approach: selenium, webdriver-manager, requests, pillow

## License

This project is open-source and available under the MIT License.

### Basic Usage

To download all images from @shailosophy:

```bash
python instagram_downloader.py shailosophy
```

This will create a directory named `shailosophy_quotes_YYYYMMDD` and download all images to it.

### Specify Output Directory

```bash
python instagram_downloader.py shailosophy --output quotes_folder
```

### Private Profiles

If the profile is private and you need to log in:

```bash
python instagram_downloader.py shailosophy --login
```

You will be prompted to enter your Instagram username and password.

## Notes

- Instagram has rate limits. If you encounter errors related to too many requests, wait a while before trying again.
- Instagram's API and website structure may change, which could affect this tool's functionality.
- This tool is for educational purposes only. Please respect Instagram's terms of service.

## Requirements

- Python 3.6 or higher
- instaloader library

## License

This project is open-source and available under the MIT License.
