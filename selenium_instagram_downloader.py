#!/usr/bin/env python3
# Instagram Image Downloader using Selenium
import os
import time
import argparse
import requests
import random
import re
from datetime import datetime, timedelta
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver(headless=True):
    """Set up and return a Selenium WebDriver"""
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def login_to_instagram(driver, username, password):
    """Login to Instagram"""
    print(f"Logging in as {username}...")
    driver.get("https://www.instagram.com/accounts/login/")
    
    # Wait for the login page to load
    try:
        # Accept cookies if the dialog appears
        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept') or contains(text(), 'Allow')]"))
            ).click()
            print("Accepted cookies")
        except:
            print("No cookie dialog or already accepted")
        
        # Enter username
        username_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']"))
        )
        username_input.send_keys(username)
        
        # Enter password
        password_input = driver.find_element(By.CSS_SELECTOR, "input[name='password']")
        password_input.send_keys(password)
        
        # Click login button
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
        
        # Wait for login to complete
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//div[@role='dialog'] | //a[contains(@href, '/direct/inbox')] | //svg[@aria-label='Home']"))
        )
        
        # Handle "Save Login Info" dialog if it appears
        try:
            not_now_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))
            )
            not_now_button.click()
            print("Clicked 'Not Now' on save login dialog")
        except:
            print("No 'Save Login Info' dialog appeared")
            
        # Handle notifications dialog if it appears
        try:
            not_now_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))
            )
            not_now_button.click()
            print("Clicked 'Not Now' on notifications dialog")
        except:
            print("No notifications dialog appeared")
            
        print("Login successful!")
        return True
    except Exception as e:
        print(f"Login failed: {e}")
        return False

def download_image(url, output_dir, index, post_date=None):
    """Download an image from URL"""
    try:
        # Parse URL to get file extension
        parsed_url = urlparse(url)
        file_extension = os.path.splitext(parsed_url.path)[1]
        if not file_extension:
            file_extension = ".jpg"  # Default to jpg if no extension found
            
        # Create a filename with timestamp to avoid duplicates
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Include post date in filename if available
        if post_date:
            date_str = post_date.strftime("%Y%m%d")
            filename = f"image_{date_str}_{index}{file_extension}"
        else:
            filename = f"image_{timestamp}_{index}{file_extension}"
            
        filepath = os.path.join(output_dir, filename)
        
        # Download the image
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                
        print(f"Downloaded: {filename}")
        return True
    except Exception as e:
        print(f"Error downloading image {index}: {e}")
        return False

def parse_date_string(date_str):
    """Parse date string in various formats to datetime object"""
    formats = [
        "%Y-%m-%d",       # 2023-01-31
        "%d-%m-%Y",       # 31-01-2023
        "%Y/%m/%d",       # 2023/01/31
        "%d/%m/%Y",       # 31/01/2023
        "%b %d, %Y",      # Jan 31, 2023
        "%d %b %Y",       # 31 Jan 2023
        "%B %d, %Y",      # January 31, 2023
        "%d %B %Y"        # 31 January 2023
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    
    raise ValueError(f"Could not parse date: {date_str}. Please use format YYYY-MM-DD.")

def extract_post_date(driver):
    """Extract the date of the current post"""
    try:
        # Try to find date elements with multiple selectors
        date_elements = driver.find_elements(By.CSS_SELECTOR, "time")
        
        if date_elements:
            # Get datetime attribute or text content
            for date_elem in date_elements:
                # Try to get datetime attribute
                datetime_attr = date_elem.get_attribute("datetime")
                if datetime_attr:
                    try:
                        # Instagram typically uses ISO format
                        return datetime.fromisoformat(datetime_attr.replace('Z', '+00:00'))
                    except ValueError:
                        pass
                
                # Try to get text content which might contain a date
                date_text = date_elem.text
                if date_text:
                    # Try to parse common date formats
                    try:
                        # Handle relative dates like "2d" (2 days ago), "5w" (5 weeks ago)
                        if re.match(r'^\d+[dwmy]$', date_text.lower()):
                            value = int(date_text[:-1])
                            unit = date_text[-1].lower()
                            
                            now = datetime.now()
                            if unit == 'd':  # days
                                return now - timedelta(days=value)
                            elif unit == 'w':  # weeks
                                return now - timedelta(weeks=value)
                            elif unit == 'm':  # months (approximate)
                                return now - timedelta(days=value*30)
                            elif unit == 'y':  # years (approximate)
                                return now - timedelta(days=value*365)
                        
                        # Try other common formats
                        return parse_date_string(date_text)
                    except ValueError:
                        pass
        
        # If we couldn't find a date, return None
        return None
    except Exception as e:
        print(f"Error extracting post date: {e}")
        return None

def scroll_and_extract_images(driver, profile_name, output_dir, max_images=None, scroll_pause=2.0, start_date=None, end_date=None, download=False):
    """Scroll through profile and extract image URLs"""
    # Navigate to profile page
    profile_url = f"https://www.instagram.com/{profile_name}/"
    print(f"Navigating to {profile_url}")
    driver.get(profile_url)
    
    # Wait for page to load
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "img"))
        )
        print("Page loaded successfully")
    except Exception as e:
        print(f"Error loading profile page: {e}")
        return
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")
    
    # Set a default max_images if not provided or if we couldn't get post count
    if max_images is None:
        max_images = 500  # Default to 500 images
        print(f"No max images specified, will attempt to download up to {max_images} images")
    else:
        print(f"Will attempt to download up to {max_images} images")
    
    # Scroll and collect image URLs
    image_urls = set()
    scroll_attempts = 0
    max_scroll_attempts = 100  # Increased limit to support downloading more images
    
    print("Starting to scroll and collect images...")
    
    # Wait for posts to load
    time.sleep(3)
    
    # Try to click on the first post to open it in a modal
    try:
        # First try to find all post links
        print("Looking for post links...")
        post_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/p/']")
        if post_links:
            print(f"Found {len(post_links)} post links")
            # Click on the first post
            post_links[0].click()
            print("Clicked on first post")
            time.sleep(2)
            
            # Now we're in the post modal, we can extract the image and then navigate through posts
            for i in range(min(max_images, 500)):  # Limit to avoid infinite loops
                try:
                    # Find the image in the modal
                    modal_images = driver.find_elements(By.CSS_SELECTOR, "img[style*='object-fit']")
                    if not modal_images:
                        modal_images = driver.find_elements(By.CSS_SELECTOR, "img[sizes*='px']")
                    if not modal_images:
                        modal_images = driver.find_elements(By.TAG_NAME, "img")
                    
                    # Extract image URL
                    for img in modal_images:
                        try:
                            src = img.get_attribute("src")
                            if src and src not in image_urls and not src.endswith(".svg"):
                                # Filter out small images and icons
                                if ("profile_pic" not in src and 
                                    "s150x150" not in src and 
                                    "avatar" not in src.lower() and
                                    "icon" not in src.lower()):
                                    # Extract post date if date filtering is enabled
                                    post_date = None
                                    if start_date or end_date:
                                        post_date = extract_post_date(driver)
                                        if post_date:
                                            print(f"Post date: {post_date.strftime('%Y-%m-%d')}")
                                            
                                            # Skip if post is outside date range
                                            if (start_date and post_date < start_date) or \
                                               (end_date and post_date > end_date):
                                                print(f"Skipping post (outside date range)")
                                                continue
                                    
                                    # Store both URL and date
                                    image_urls.add((src, post_date))
                                    print(f"Found image in post modal: {len(image_urls)}/{max_images}")
                                    break
                        except:
                            continue
                    
                    # Click next button to go to next post
                    next_buttons = driver.find_elements(By.CSS_SELECTOR, "button[aria-label*='Next']")
                    if not next_buttons:
                        next_buttons = driver.find_elements(By.XPATH, "//button[contains(@aria-label, 'Next')]")
                    if not next_buttons:
                        next_buttons = driver.find_elements(By.XPATH, "//svg[@aria-label='Next']/ancestor::button")
                    
                    if next_buttons:
                        next_buttons[0].click()
                        print("Clicked next button")
                        time.sleep(1)
                    else:
                        print("No next button found, breaking loop")
                        break
                        
                    # If we have enough images, break
                    if len(image_urls) >= max_images:
                        break
                        
                except Exception as e:
                    print(f"Error navigating posts: {e}")
                    break
            
            # Return to profile page
            driver.get(profile_url)
            time.sleep(2)
        
    except Exception as e:
        print(f"Error clicking on first post: {e}")
    
    # If we didn't get enough images from the modal approach, try the traditional scrolling approach
    if len(image_urls) < max_images:
        print(f"Only found {len(image_urls)} images using modal approach, trying scroll approach...")
        
        while len(image_urls) < max_images and scroll_attempts < max_scroll_attempts:
            scroll_attempts += 1
            
            # Find all images on the page
            try:
                # Try multiple selectors to find post images
                all_images = driver.find_elements(By.TAG_NAME, "img")
                print(f"Found {len(all_images)} total images on page")
                
                # Filter images to find post images
                new_images_found = 0
                for img in all_images:
                    try:
                        # Get image source
                        src = img.get_attribute("src")
                        if not src or src in image_urls or src.endswith(".svg"):
                            continue
                            
                        # Filter out small images, profile pics, icons
                        if ("profile_pic" in src or 
                            "s150x150" in src or 
                            "avatar" in src.lower() or 
                            "icon" in src.lower()):
                            continue
                        
                        # Check image dimensions if available
                        try:
                            width = img.get_attribute("width")
                            height = img.get_attribute("height")
                            if width and height and (int(width) < 150 or int(height) < 150):
                                continue
                        except:
                            pass
                            
                        # For scroll approach, we can't easily get post dates
                        # So we just add the URL without a date
                        image_urls.add((src, None))
                        new_images_found += 1
                        
                        # If we've found enough images, break
                        if len(image_urls) >= max_images:
                            break
                    except Exception as e:
                        continue
            
                
                print(f"Found {new_images_found} new images. Total: {len(image_urls)}/{max_images}")
                
                # If we've found enough images, break
                if len(image_urls) >= max_images:
                    break
                    
            except Exception as e:
                print(f"Error finding images: {e}")
            
            # Scroll down
            driver.execute_script("window.scrollBy(0, 1000);")
            
            # Wait for new content to load
            time.sleep(scroll_pause + random.uniform(0.5, 1.0))
        
        # Scroll down
        driver.execute_script("window.scrollBy(0, 1000);")
        
        # Wait for new content to load
        time.sleep(scroll_pause + random.uniform(0.5, 1.0))
        
        # If we've scrolled several times and found no images, try clicking "Load more" or "See more"
        if scroll_attempts % 5 == 0:
            try:
                # Try different button text variations
                for button_text in ["Load more", "See more", "Show more", "View more"]:
                    buttons = driver.find_elements(By.XPATH, f"//button[contains(text(), '{button_text}')]")
                    if buttons:
                        buttons[0].click()
                        print(f"Clicked '{button_text}' button")
                        time.sleep(2)  # Wait for content to load
                        break
            except:
                pass  # Ignore if no buttons found or can't click
    
    # Download or just count the images
    if len(image_urls) > 0:
        if download:
            print(f"\nDownloading {len(image_urls)} images...")
            downloaded_count = 0
            
            for i, item in enumerate(image_urls):
                # Unpack URL and date
                if isinstance(item, tuple):
                    url, post_date = item
                else:
                    # For backward compatibility
                    url, post_date = item, None
                    
                if download_image(url, output_dir, i, post_date):
                    downloaded_count += 1
                
                # Add a small delay between downloads
                time.sleep(random.uniform(0.2, 0.5))
            
            print(f"\nDownload complete! {downloaded_count} images from @{profile_name} have been saved to {output_dir}")
        else:
            print(f"\nFound {len(image_urls)} images in the specified date range.")
            print(f"To download these images, run the command again with the --download flag.")
    else:
        print(f"No images found on {profile_name}'s profile. Try with --login option or check if the profile exists.")

def main():
    parser = argparse.ArgumentParser(description='Download Instagram images from a profile using Selenium')
    parser.add_argument('profile', type=str, help='Instagram profile to download from (without @)')
    parser.add_argument('--output', '-o', type=str, help='Directory to save images')
    parser.add_argument('--login', '-l', nargs='?', const='prompt', help='Login to Instagram (--login for prompt, --login username to specify username)')
    parser.add_argument('--password', '-p', type=str, help='Instagram password (use with --login username)')
    parser.add_argument('--max-images', '-m', type=int, help='Maximum number of images to download')
    parser.add_argument('--visible', '-v', action='store_true', help='Make browser visible (not headless)')
    parser.add_argument('--start-date', '-s', type=str, help='Start date for filtering posts (format: YYYY-MM-DD)')
    parser.add_argument('--end-date', '-e', type=str, help='End date for filtering posts (format: YYYY-MM-DD)')
    parser.add_argument('--download', '-d', action='store_true', help='Download images (if not specified, only count images)')
    
    args = parser.parse_args()
    
    # Profile to download from
    profile_name = args.profile
    
    # Directory to save images
    output_dir = args.output if args.output else f"{profile_name}_quotes_{datetime.now().strftime('%Y%m%d')}"
    
    # Create output directory if it doesn't exist and we're downloading
    if args.download:
        os.makedirs(output_dir, exist_ok=True)
    
    # Set up the WebDriver
    driver = setup_driver(headless=not args.visible)
    
    try:
        # Handle login if requested
        if args.login:
            import getpass
            
            # Determine username
            username = None
            if args.login != 'prompt':
                # User provided username via --login username
                username = args.login
            else:
                # Prompt for username
                username = input("Instagram username: ")
            
            # Determine password
            password = None
            if args.password:
                # User provided password via --password
                password = args.password
            else:
                # Prompt for password securely
                password = getpass.getpass("Instagram password: ")
            
            # Attempt login
            print(f"Logging in as {username}...")
            if not login_to_instagram(driver, username, password):
                print("Login failed. Exiting.")
                driver.quit()
                return
            
            # Wait a moment after login before navigating to profile
            time.sleep(2)
        
        # Parse date range if provided
        start_date = None
        if args.start_date:
            try:
                start_date = parse_date_string(args.start_date)
                print(f"Filtering posts from {start_date.strftime('%Y-%m-%d')}")
            except ValueError as e:
                print(f"Error parsing start date: {e}")
                driver.quit()
                return
                
        if args.end_date:
            try:
                end_date = parse_date_string(args.end_date)
                print(f"Filtering posts until {end_date.strftime('%Y-%m-%d')}")
            except ValueError as e:
                print(f"Error parsing end date: {e}")
                driver.quit()
                return
        
        # Download images with date filtering
        scroll_and_extract_images(
            driver, 
            profile_name, 
            output_dir, 
            args.max_images,
            start_date=start_date,
            end_date=end_date,
            download=args.download
        )
        
    finally:
        # Clean up
        driver.quit()

if __name__ == "__main__":
    main()
