"""
Direct PRAW Authentication Test

This script tests your Reddit API credentials using PRAW directly,
without any other application code involved.
"""

import configparser
import praw
from prawcore.exceptions import OAuthException, ResponseException

def load_credentials(config_path='config.ini'):
    """Load Reddit credentials from config file."""
    config = configparser.ConfigParser()
    config.read(config_path)
    
    if 'reddit' not in config:
        raise ValueError("No [reddit] section found in config file")
    
    return {
        'client_id': config['reddit'].get('client_id', '').strip('"\''),
        'client_secret': config['reddit'].get('client_secret', '').strip('"\''),
        'username': config['reddit'].get('username', '').strip('"\''),
        'user_agent': config['reddit'].get('user_agent', '').strip('"\'')
    }

def test_read_only_auth(credentials):
    """Test read-only authentication (no username/password required)."""
    print("\n=== Testing Read-Only Authentication ===")
    
    try:
        # Initialize Reddit instance in read-only mode
        reddit = praw.Reddit(
            client_id=credentials['client_id'],
            client_secret=credentials['client_secret'],
            user_agent=credentials['user_agent']
        )
        
        # Test with a simple API call
        print("Attempting to access r/python...")
        subreddit = reddit.subreddit('python')
        post = next(subreddit.hot(limit=1), None)
        
        if post:
            print(f"✅ Success! Retrieved post: {post.title[:50]}...")
            return True
        else:
            print("⚠️ Connected but couldn't retrieve posts.")
            return True
            
    except OAuthException as e:
        print(f"❌ OAuth Error: {str(e)}")
        print("\nThis typically means your client_id or client_secret is incorrect.")
        print("Or your app may not be registered as a 'script' type.")
        return False
        
    except ResponseException as e:
        print(f"❌ API Response Error: {str(e)}")
        if "401" in str(e):
            print("\nThis is an authentication error. Your credentials are likely incorrect.")
        elif "403" in str(e):
            print("\nThis is a permission error. Your account may be restricted or rate-limited.")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected Error: {str(e)}")
        return False

def main():
    print("Direct PRAW Authentication Test")
    print("===============================")
    print("This script tests your Reddit API credentials using PRAW directly.\n")
    
    try:
        # Load credentials from config.ini
        print("Loading credentials from config.ini...")
        credentials = load_credentials()
        
        # Remove quotes if present
        for key in credentials:
            if credentials[key] and credentials[key].startswith('"') and credentials[key].endswith('"'):
                credentials[key] = credentials[key][1:-1]
        
        # Show masked credentials
        print(f"Client ID: {credentials['client_id'][:4]}{'*' * (len(credentials['client_id']) - 4) if len(credentials['client_id']) > 4 else ''}")
        print(f"Client Secret: {credentials['client_secret'][:4]}{'*' * (len(credentials['client_secret']) - 4) if len(credentials['client_secret']) > 4 else ''}")
        print(f"Username: {credentials['username'] if credentials['username'] else 'Not provided (read-only mode)'}")
        print(f"User Agent: {credentials['user_agent']}")
        
        # Test read-only authentication
        success = test_read_only_auth(credentials)
        
        if success:
            print("\n✅ Authentication tests completed successfully!")
            print("Your Reddit API credentials are working correctly.")
        else:
            print("\n❌ Authentication tests failed.")
            print("Please check your credentials and try again.")
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("Please check your config.ini file and try again.")

if __name__ == "__main__":
    main()
