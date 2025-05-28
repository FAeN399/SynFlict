"""
Verify Reddit API credentials from config.ini

This script tests if your Reddit API credentials are working properly.
It attempts to:
1. Test read-only access (client ID & secret only)
2. Test authenticated access (with username & password)
"""

import configparser
import os
import sys
import praw
from pathlib import Path

def verify_credentials():
    print("Verifying Reddit API credentials from config.ini...")
    
    # Load credentials from config.ini
    config = configparser.ConfigParser()
    config_path = Path("config.ini")
    
    if not config_path.exists():
        print("❌ Error: config.ini not found")
        return False
    
    config.read(config_path)
    
    if 'reddit' not in config:
        print("❌ Error: [reddit] section missing from config.ini")
        return False
    
    # Extract credentials
    client_id = config['reddit'].get('client_id')
    client_secret = config['reddit'].get('client_secret')
    username = config['reddit'].get('username')
    user_agent = config['reddit'].get('user_agent')
    
    if not client_id or not client_secret:
        print("❌ Error: client_id or client_secret missing from config.ini")
        return False
    
    print(f"Client ID: {client_id}")
    print(f"User Agent: {user_agent}")
    
    # Test read-only authentication
    print("\n1. Testing read-only authentication (client ID & secret)...")
    try:
        reddit_readonly = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )
        
        # Test a simple API call
        posts = list(reddit_readonly.subreddit("python").hot(limit=1))
        if posts:
            print(f"✅ Read-only authentication successful!")
            print(f"   Sample post: {posts[0].title[:50]}...")
        else:
            print("⚠️ Connected but didn't retrieve any posts")
            
    except Exception as e:
        print(f"❌ Read-only authentication failed: {str(e)}")
        print("\nCommon causes of this error:")
        print("1. Incorrect client_id or client_secret in config.ini")
        print("2. Poor network connection")
        print("3. Reddit API might be down or rate-limiting")
        return False
    
    # Test user authentication if username is provided
    if username:
        print(f"\n2. Testing user authentication for u/{username}...")
        print("   You'll need to enter your password:")
        
        try:
            password = input("   Password: ").strip()
            
            # If using 2FA, allow appending the code
            if ":" not in password and input("   Are you using 2FA? (y/n): ").lower().startswith("y"):
                code = input("   Enter your 2FA code: ").strip()
                password = f"{password}:{code}"
            
            reddit_user = praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                username=username,
                password=password,
                user_agent=user_agent
            )
            
            me = reddit_user.user.me()
            print(f"✅ User authentication successful! Logged in as: u/{me.name}")
            print(f"   Account age: {me.created_utc}")
            print(f"   Karma: {me.link_karma + me.comment_karma}")
            
            # Try listing user's saved posts as a deeper test
            saved = list(reddit_user.user.me().saved(limit=1))
            if saved:
                print(f"   Successfully accessed user data")
            
        except Exception as e:
            print(f"❌ User authentication failed: {str(e)}")
            print("\nCommon causes of this error:")
            print("1. Incorrect password")
            print("2. If using 2FA, you need to append the code to your password as 'password:123456'")
            print("3. App might not be registered as 'script' type (must be 'personal use script')")
            print("4. Username in config.ini might not match the app owner account")
            return False
    
    print("\n✅ Credential verification complete!")
    print("Your Reddit API credentials are correctly configured.")
    return True

if __name__ == "__main__":
    verify_credentials()
