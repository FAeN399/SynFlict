"""
Test script to verify Reddit API credentials.
Run this to check if your credentials are working correctly.
"""

import praw
import sys

def test_reddit_auth(client_id, client_secret, username=None, password=None):
    """Test Reddit API authentication with provided credentials."""
    
    print(f"Testing Reddit API authentication...")
    print(f"Client ID: {client_id[:4]}{'*' * (len(client_id) - 4)}")
    
    try:
        # First try read-only mode to test client_id and client_secret
        print("\n1. Testing client ID and secret in read-only mode...")
        user_agent = f"reddit_media_grabber/0.1 (by u/{username or 'anonymous_user'})"
        
        reddit_readonly = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )
        
        # Test a simple API call
        test_sub = next(reddit_readonly.subreddit("python").hot(limit=1), None)
        if test_sub:
            print(f"✅ Read-only mode successful! Retrieved post: {test_sub.title[:40]}...")
        else:
            print("⚠️ Could connect but didn't get any posts. Strange but not an auth error.")
        
        # If username and password provided, test user authentication
        if username and password:
            print("\n2. Testing full authentication with username and password...")
            
            reddit_user = praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                username=username,
                password=password,
                user_agent=user_agent
            )
            
            me = reddit_user.user.me()
            print(f"✅ Full authentication successful! Logged in as: {me.name}")
            print(f"Account created: {me.created_utc}")
            print(f"Karma: {me.link_karma + me.comment_karma}")
        
        return True
        
    except Exception as e:
        print(f"❌ Authentication Error: {str(e)}")
        print("\nPlease check:")
        print("1. Is your app registered as a 'script' type?")
        print("2. Did you copy the client ID and secret correctly?")
        print("3. If using username/password: Is the account the same one that created the app?")
        print("4. If using 2FA: Did you append the code to your password as 'password:123456'?")
        return False

if __name__ == "__main__":
    # If no arguments provided, prompt for credentials
    if len(sys.argv) == 1:
        print("Enter your Reddit API credentials:")
        client_id = input("Client ID: ").strip()
        client_secret = input("Client Secret: ").strip()
        
        test_user = input("Test with username/password? (y/n): ").strip().lower() == 'y'
        username = password = None
        
        if test_user:
            username = input("Username: ").strip()
            password = input("Password (+ 2FA code if enabled as 'password:123456'): ").strip()
        
        test_reddit_auth(client_id, client_secret, username, password)
    
    # If arguments provided, use them
    elif len(sys.argv) >= 3:
        client_id = sys.argv[1]
        client_secret = sys.argv[2]
        username = sys.argv[3] if len(sys.argv) > 3 else None
        password = sys.argv[4] if len(sys.argv) > 4 else None
        
        test_reddit_auth(client_id, client_secret, username, password)
    
    else:
        print("Usage: python test_reddit_auth.py [client_id] [client_secret] [username] [password]")
        print("Or run without arguments for interactive mode.")
