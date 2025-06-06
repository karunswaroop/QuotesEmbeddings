#!/usr/bin/env python3
# Instagram Image Downloader for @shailosophy
import instaloader
import os
import argparse
from datetime import datetime

def download_instagram_images(profile_name, output_dir=None, login_username=None, login_password=None):
    """
    Download all posts from an Instagram profile
    
    Args:
        profile_name (str): Instagram profile username (without @)
        output_dir (str, optional): Directory to save images. If None, creates a directory with the profile name.
        login_username (str, optional): Instagram username for login if needed
        login_password (str, optional): Instagram password for login if needed
    """
    # Create instance
    L = instaloader.Instaloader(
        download_videos=False,       # We only want images
        download_video_thumbnails=False,
        download_geotags=False,
        download_comments=False,
        save_metadata=True,          # Save metadata for reference
        compress_json=False,
        post_metadata_txt_pattern=''  # Don't create .txt files for each post
    )
    
    # Create output directory if it doesn't exist
    if output_dir is None:
        output_dir = profile_name
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")
    
    try:
        # Login if credentials provided
        if login_username and login_password:
            print(f"Logging in as {login_username}...")
            try:
                L.login(login_username, login_password)
                print("Login successful!")
            except instaloader.exceptions.BadCredentialsException:
                print("Error: Invalid login credentials")
                return
        
        # Get profile
        print(f"Fetching profile: {profile_name}")
        profile = instaloader.Profile.from_username(L.context, profile_name)
        
        # Count total posts
        post_count = profile.mediacount
        print(f"Found {post_count} posts on {profile.username}'s profile")
        
        # Download all posts
        print(f"Downloading posts from {profile.username}...")
        
        # Track progress
        downloaded = 0
        
        # Iterate through posts and download
        for post in profile.get_posts():
            # Download the post
            L.download_post(post, target=output_dir)
            
            downloaded += 1
            print(f"Downloaded post {downloaded}/{post_count} - {post.date}")
            
        print(f"\nDownload complete! All posts from @{profile_name} have been saved to {output_dir}")
        
    except instaloader.exceptions.ProfileNotExistsException:
        print(f"Error: Profile @{profile_name} does not exist")
    except instaloader.exceptions.LoginRequiredException:
        print("Error: This profile requires login. Try using the --login option.")
    except Exception as e:
        print(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(description='Download Instagram images from a profile')
    parser.add_argument('profile', type=str, help='Instagram profile to download from (without @)')
    parser.add_argument('--output', '-o', type=str, help='Directory to save images')
    parser.add_argument('--login', '-l', action='store_true', help='Login to Instagram (will prompt for credentials)')
    
    args = parser.parse_args()
    
    # Profile to download from
    profile_name = args.profile if args.profile else "shailosophy"
    
    # Directory to save images
    output_dir = args.output if args.output else f"{profile_name}_quotes_{datetime.now().strftime('%Y%m%d')}"
    
    # Optional login
    login_username = None
    login_password = None
    
    if args.login:
        import getpass
        login_username = input("Instagram username: ")
        login_password = getpass.getpass("Instagram password: ")
    
    # Download images
    download_instagram_images(profile_name, output_dir, login_username, login_password)

if __name__ == "__main__":
    main()
