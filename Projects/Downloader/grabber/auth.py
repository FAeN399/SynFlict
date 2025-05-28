"""
Authentication module for Reddit API access.

Handles OAuth authentication with Reddit API using either:
1. Application-only OAuth (script type app)
2. User-based OAuth for accessing user-specific content
"""

import logging
import os
import webbrowser
from typing import Optional, Dict, Any, Tuple
import configparser
import pathlib

import praw

from grabber.config import load_config

logger = logging.getLogger(__name__)


def get_reddit_instance(user_auth: bool = False, mock: bool = False) -> praw.Reddit:
    """
    Get an authenticated Reddit instance.
    
    Args:
        user_auth: If True, use user authentication; otherwise, use application-only auth
        mock: If True, return a mock Reddit instance for testing
        
    Returns:
        Authenticated PRAW Reddit instance or mock instance
    """
    # Return a mock Reddit instance if requested or if an explicit env flag is set
    if mock or os.environ.get("GRABBER_MOCK_MODE", "").lower() in ("true", "1", "yes"):
        from unittest.mock import MagicMock
        
        logger.info("Using mock Reddit instance for testing")
        
        # Create a mock Reddit instance
        mock_reddit = MagicMock()
        
        # Set up the user attribute
        mock_user = MagicMock()
        mock_user.me.return_value = MagicMock(
            name="mock_user",
            link_karma=9999,
            comment_karma=9999,
            created_utc=1609459200  # 2021-01-01
        )
        mock_reddit.user = mock_user
        
        # Mock the submission function
        mock_submission = MagicMock(
            id="bc4hkg",
            title="Paradise on Earth Lake Louise Banff Canada",
            url="https://i.redd.it/mockimage.jpg",
            permalink="/r/EarthPorn/comments/bc4hkg/paradise_on_earth_lake_louise_banff_canada_oc/",
            score=9999,
            author=MagicMock(name="mock_author"),
            created_utc=1609459200,  # 2021-01-01
            subreddit=MagicMock(display_name="EarthPorn")
        )
        mock_reddit.submission.return_value = mock_submission
        
        # Mock the subreddit function and search functionality
        mock_subreddit = MagicMock()
        
        # Create a list of mock search results
        mock_results = []
        for i in range(10):  # Create 10 mock posts
            mock_post = MagicMock(
                id=f"mock{i}",
                title=f"Mock Post {i}",
                url=f"https://i.redd.it/mockimage{i}.jpg",
                permalink=f"/r/pics/comments/mock{i}/mock_post_{i}/",
                score=100 + i * 10,
                author=MagicMock(name=f"mock_author_{i}"),
                created_utc=1609459200 + i * 3600,  # Incremental timestamps
                subreddit=MagicMock(display_name="pics"),
                over_18=(i % 3 == 0),  # Every third post is NSFW
                is_self=False,
                is_video=(i % 5 == 0),  # Every fifth post is a video
                post_hint="image" if i % 5 != 0 else "hosted:video"
            )
            mock_results.append(mock_post)
        
        # Configure the mock search method
        mock_search = MagicMock()
        mock_search.__iter__.return_value = iter(mock_results)
        mock_subreddit.search.return_value = mock_search
        
        mock_reddit.subreddit.return_value = mock_subreddit
        
        logger.info("Using mock Reddit instance for testing")
        return mock_reddit
    
    # Get config for real authentication
    config = load_config()
    
    # Check for credentials from our config module
    client_id = config.get('reddit_client_id')
    client_secret = config.get('reddit_client_secret')
    username = config.get('reddit_username')
    
    # If config.ini exists in the project root, try to load it directly as a backup
    if not client_id or not client_secret:
        try:
            import configparser
            from pathlib import Path
            
            config_path = Path("config.ini")
            if config_path.exists():
                cfg = configparser.ConfigParser()
                cfg.read(config_path)
                
                if 'reddit' in cfg:
                    # Override with values from config.ini
                    if 'client_id' in cfg['reddit'] and not client_id:
                        client_id = cfg['reddit']['client_id'].strip('"\'')
                        
                    if 'client_secret' in cfg['reddit'] and not client_secret:
                        client_secret = cfg['reddit']['client_secret'].strip('"\'')
                        
                    if 'username' in cfg['reddit'] and not username:
                        username = cfg['reddit']['username'].strip('"\'')
                        
                    # Also load user_agent if available
                    if 'user_agent' in cfg['reddit']:
                        user_agent = cfg['reddit']['user_agent'].strip('"\'')
                        
                    logger.info(f"Loaded credentials from {config_path}")
                    logger.debug(f"Loaded client_id length: {len(client_id)}, contains quotes: {'"' in client_id or "'" in client_id}")
                    logger.debug(f"Loaded client_secret length: {len(client_secret)}, contains quotes: {'"' in client_secret or "'" in client_secret}")
        except Exception as e:
            logger.error(f"Error loading config.ini: {e}")
    
    # Ensure we have a proper user agent (essential for avoiding 401 errors)
    default_username = username or 'anonymous_user'
    user_agent = config.get('reddit_user_agent')
    
    # If user_agent isn't in the config module, check if it was loaded from config.ini
    if not user_agent:
        # Create a default user agent string
        user_agent = f"reddit_media_grabber/0.1 by u/{default_username}"
    
    # Ensure user_agent is properly formatted and doesn't have quotes
    user_agent = user_agent.strip('"\'')
    
    # Log the user agent being used
    logger.info(f"Using user agent: {user_agent}")
    
    if not client_id or not client_secret:
        # If no credentials are found, prompt user to create them
        client_id, client_secret = prompt_for_credentials()
    
    # Log some diagnostic info that might help troubleshoot auth issues
    logger.info(f"Auth attempt with client ID: {client_id[:4]}{'*' * (len(client_id) - 4) if len(client_id) > 4 else ''}")
    logger.info(f"Using user agent: {user_agent}")
    
    try:
        if user_auth:
            # Get username from config or prompt if not available
            stored_username = config.get('reddit_username') or username  # Use the username we loaded earlier
            password = config.get('reddit_password')
            
            # If we have a username but no password, prompt for it
            if stored_username and not password:
                print(f"\nPassword required for Reddit user: {stored_username}")
                print("Note: Your password is only sent to Reddit's API, not stored locally.")
                
                # Get password securely (it won't be saved anywhere)
                password = input("Enter your Reddit password: ").strip()
                
                # Check if using 2FA
                use_2fa = input("Are you using 2-factor authentication? (y/n): ").strip().lower()
                if use_2fa.startswith('y'):
                    code = input("Enter your 2FA code: ").strip()
                    password = f"{password}:{code}"
            
            if stored_username and password:
                # Use password flow (script app)
                logger.info(f"Authenticating as user: {stored_username}")
                reddit = praw.Reddit(
                    client_id=client_id,
                    client_secret=client_secret,
                    user_agent=user_agent,
                    username=stored_username,
                    password=password
                )
                
                # Test authentication by accessing user info
                # This will raise an exception if authentication fails
                me = reddit.user.me()
                logger.info(f"Successfully authenticated as: {me.name}")
            else:
                # Use OAuth flow with user authorization
                logger.info("Starting OAuth flow for user authentication")
                reddit = start_oauth_flow(client_id, client_secret, user_agent, stored_username)
        else:
            # Use application-only auth
            logger.info("Using application-only authentication")
            logger.debug(f"client_id: {client_id[:4]}{'*' * (len(client_id) - 4) if len(client_id) > 4 else ''}")
            logger.debug(f"client_id length: {len(client_id)}")
            logger.debug(f"client_secret: {client_secret[:4]}{'*' * (len(client_secret) - 4) if len(client_secret) > 4 else ''}")
            logger.debug(f"client_secret length: {len(client_secret)}")
            logger.debug(f"user_agent: {user_agent}")
            
            # Print exact same values to console for comparison with direct test
            print(f"DEBUG - Application params:")
            print(f"client_id: {client_id[:4]}{'*' * (len(client_id) - 4) if len(client_id) > 4 else ''}")
            print(f"client_secret: {client_secret[:4]}{'*' * (len(client_secret) - 4) if len(client_secret) > 4 else ''}")
            print(f"user_agent: {user_agent}")
            
            # Create Reddit instance exactly like in direct_praw_test.py
            reddit = praw.Reddit(
                client_id=client_id.strip(),
                client_secret=client_secret.strip(),
                user_agent=user_agent.strip()
            )
            
            # Test connection with a simple API call
            logger.info("Attempting to access r/python...")
            test_subreddit = next(reddit.subreddit('python').new(limit=1), None)
            if test_subreddit:
                logger.info(f"Successfully connected in read-only mode, found post: {test_subreddit.title[:30]}...")
                
        return reddit
        
    except Exception as e:
        logger.error(f"Reddit authentication error: {str(e)}")
        logger.error("Please check that your app is registered as 'script' type and credentials are correct")
        
        # If mock is allowed, return a mock instance instead of raising the exception
        if mock:
            logger.warning("Falling back to mock client due to authentication failure")
            return get_reddit_instance(mock=True)
        raise
    
    # Code execution should never reach here due to the return/raise in the try/except block


def prompt_for_credentials() -> Tuple[str, str]:
    """
    Prompt the user to create Reddit API credentials.
    
    Returns:
        Tuple of (client_id, client_secret)
    """
    print("\n===== Reddit API Credentials =====")
    print("You need to create a Reddit API application to use this tool.")
    print("1. Go to https://www.reddit.com/prefs/apps")
    print("2. Scroll down and click 'create another app...'")
    print("3. Fill in the details:")
    print("   - Name: RedditGrabber")
    print("   - Select 'script'")
    print("   - Description: Tool for downloading media from Reddit")
    print("   - About URL: (leave blank)")
    print("   - Redirect URI: http://localhost:8080")
    print("4. Click 'create app'")
    print("5. Copy the client ID (the string under the app name)")
    print("6. Copy the client secret\n")
    
    client_id = input("Enter your client ID: ").strip()
    client_secret = input("Enter your client secret: ").strip()
    
    # Save credentials to config file
    save_credentials(client_id, client_secret)
    
    return client_id, client_secret


def save_credentials(client_id: str, client_secret: str, 
                     username: Optional[str] = None, 
                     password: Optional[str] = None) -> None:
    """
    Save Reddit API credentials to a config file.
    
    Args:
        client_id: Reddit API client ID
        client_secret: Reddit API client secret
        username: Reddit username (optional)
        password: Reddit password (optional)
    """
    # Create config directory if it doesn't exist
    config_dir = pathlib.Path.home() / ".config" / "reddit-grabber"
    config_dir.mkdir(parents=True, exist_ok=True)
    
    # Create config file
    config_file = config_dir / "credentials.ini"
    
    config = configparser.ConfigParser()
    
    # Read existing config if it exists
    if config_file.exists():
        config.read(config_file)
    
    # Ensure reddit section exists
    if "reddit" not in config:
        config["reddit"] = {}
    
    # Update credentials
    config["reddit"]["client_id"] = client_id
    config["reddit"]["client_secret"] = client_secret
    
    if username:
        config["reddit"]["username"] = username
    
    if password:
        config["reddit"]["password"] = password
    
    # Write config file
    with open(config_file, "w") as f:
        config.write(f)
    
    logger.info(f"Saved Reddit API credentials to {config_file}")


def start_oauth_flow(client_id: str, client_secret: str, user_agent: str, username: Optional[str] = None) -> praw.Reddit:
    """
    Start OAuth flow for user authentication.
    
    Args:
        client_id: Reddit API client ID
        client_secret: Reddit API client secret
        user_agent: User agent string
        
    Returns:
        Authenticated PRAW Reddit instance
    """
    # For script type applications, we can use username/password flow instead of OAuth
    print("\n===== Reddit User Authentication =====")
    print("To access your Reddit account, please provide your credentials.")
    print("Note: Your password is only sent to Reddit, not stored or logged.")
    
    # Use provided username if available, otherwise prompt
    if username:
        print(f"Username: {username}")
    else:
        username = input("Enter your Reddit username: ").strip()
        
    password = input("Enter your Reddit password: ").strip()
    
    # Check if user is using 2FA
    use_2fa = input("Are you using 2-factor authentication? (y/n): ").strip().lower()
    if use_2fa.startswith('y'):
        code = input("Enter your current 2FA code: ").strip()
        password = f"{password}:{code}"
    
    # Create Reddit instance with password auth
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent,
        username=username,
        password=password,
        redirect_uri="http://localhost:8080"
    )
    
    return reddit


def setup_user_auth() -> None:
    """
    Interactive function to set up user authentication.
    """
    print("\n===== Reddit User Authentication Setup =====")
    print("This will guide you through setting up authentication with your Reddit account.")
    
    # Get existing or new credentials
    config = load_config()
    client_id = config.get('reddit_client_id')
    client_secret = config.get('reddit_client_secret')
    
    if not client_id or not client_secret:
        client_id, client_secret = prompt_for_credentials()
    
    # Ask for username/password
    print("\nPlease enter your Reddit credentials to authenticate:")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    
    # Save credentials (username only, not password)
    save_credentials(client_id, client_secret, username)
    
    # Test authentication
    try:
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=f"grabber/0.1.0",
            username=username,
            password=password
        )
        
        # Verify authentication
        me = reddit.user.me()
        if me:
            print(f"\n✅ Successfully authenticated as: {me.name}")
            print("You can now use the grabber with your Reddit account.")
        else:
            print("\n❌ Authentication failed. Please check your credentials.")
    except Exception as e:
        print(f"\n❌ Error during authentication: {e}")
        print("Please try again with correct credentials.")
