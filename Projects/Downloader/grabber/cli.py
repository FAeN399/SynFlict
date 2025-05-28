"""
Command-line interface for the Reddit Grabber utility.
"""

import os
import re
import sys
import time
import pathlib
from typing import Optional, List, Dict, Any, Union, Tuple
from enum import Enum

import typer
from rich.console import Console
from rich.logging import RichHandler
from dotenv import load_dotenv

from grabber import __version__

# Initialize console for rich output
console = Console()
error_console = Console(stderr=True)

# Load environment variables from .env file
load_dotenv()

# Initialize Typer app
app = typer.Typer(
    name="grabber",
    help="Utility for downloading media from Reddit",
    add_completion=False,
)

# Add authentication command
auth_app = typer.Typer(name="auth", help="Authentication commands")
app.add_typer(auth_app)


class UIType(str, Enum):
    """UI wrapper options."""
    NONE = "none"
    TEXTUAL = "textual"
    PYSIDE = "pyside"


def _get_config() -> Dict[str, Any]:
    """
    Load configuration from various sources in order of precedence:
    1. Environment variables
    2. User config file
    3. Project config file
    
    Returns:
        Dict with merged configuration
    """
    # This is a stub that will be expanded later
    config = {}
    
    # Load from environment variables with GRABBER_ prefix
    for key, value in os.environ.items():
        if key.startswith("GRABBER_"):
            config_key = key[8:].lower()
            config[config_key] = value
    
    # Reddit API credentials
    for key in ["REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET", "REDDIT_USER_AGENT"]:
        if key in os.environ:
            config[key.lower()] = os.environ[key]
    
    return config


def _extract_submission_id(url: str) -> Optional[str]:
    """
    Extract submission ID from various Reddit URL formats.
    
    Args:
        url: Reddit URL
        
    Returns:
        Submission ID or None if URL is invalid
    """
    pattern = r'(?:reddit\.com/r/\w+/comments/|redd\.it/|reddit\.com/comments/)([a-z0-9]+)'
    match = re.search(pattern, url, re.IGNORECASE)
    
    if match:
        return match.group(1)
    return None


@app.callback()
def callback(
    output: Optional[pathlib.Path] = typer.Option(
        "./downloads",
        "--output", "-o",
        help="Custom destination root directory",
        dir_okay=True,
        file_okay=False,
    ),
    config: Optional[pathlib.Path] = typer.Option(
        None,
        "--config", "-c",
        help="Load extra defaults from a TOML/YAML config file",
        exists=True,
        dir_okay=False,
        file_okay=True,
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet", "-q",
        help="Suppress normal log lines (errors only)",
    ),
    ui: Optional[UIType] = typer.Option(
        None,
        help="Force chosen UI wrapper",
    ),
    max_rps: Optional[float] = typer.Option(
        None,
        help="Override rate limiting algorithm (requests per second)",
        min=0.1,
        max=100.0,
    ),
):
    """
    Reddit Grabber - Download images and videos from Reddit submissions and subreddits.
    """
    # Setup logging based on quiet flag
    import logging
    log_level = logging.ERROR if quiet else logging.INFO
    
    logging.basicConfig(
        level=log_level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)]
    )
    
    # Validate output directory
    if output:
        output = pathlib.Path(output).resolve()
        if not output.exists():
            output.mkdir(parents=True, exist_ok=True)
            console.print(f"Created output directory: {output}")
    
    # Load config if specified
    if config:
        # This will be expanded when we implement config handling
        console.print(f"Loading configuration from: {config}")


@app.command("grab")
def grab_command(
    submission_url: str = typer.Argument(
        ...,
        help="URL to Reddit submission",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Show what would be downloaded without actually downloading",
    ),
):
    """
    Download all media from a single Reddit submission.
    """
    import tempfile
    from grabber.search import get_reddit_client
    from grabber.database import Database
    from grabber.downloader import process_submission
    
    # Extract submission ID from URL
    submission_id = _extract_submission_id(submission_url)
    
    if not submission_id:
        error_console.print(
            f"[bold red]Error:[/] Invalid Reddit submission URL: {submission_url}"
        )
        raise typer.Exit(code=1)
    
    # Get configuration
    config = _get_config()
    output_dir = pathlib.Path(config.get("output_dir", "./downloads"))
    
    # Get database path
    db_dir = pathlib.Path.home() / ".local" / "share" / "reddit-grabber"
    db_dir.mkdir(parents=True, exist_ok=True)
    db_path = db_dir / "grabber.db"
    
    # Initialize database
    db = Database(db_path)
    db.initialize()
    
    try:
        # Get Reddit client
        console.print(f"Authenticating with Reddit...")
        reddit = get_reddit_client(user_auth=True)
        
        # Get submission
        console.print(f"Fetching submission {submission_id}...")
        submission = reddit.submission(id=submission_id)
        
        # Process submission
        if dry_run:
            console.print(f"[DRY RUN] Would download media from: {submission.title}")
        else:
            console.print(f"Downloading media from: {submission.title}")
            
            # Process the submission
            success = process_submission(submission, db, output_dir, dry_run)
            
            if success:
                console.print(f"[bold green]Success:[/] Downloaded media from submission")
            else:
                error_console.print(f"[bold yellow]Warning:[/] Some media downloads failed")
    
    except Exception as e:
        error_console.print(f"[bold red]Error:[/] {str(e)}")
        raise typer.Exit(code=1)
    
    finally:
        # Close the database
        db.close()


@app.command("sync")
def sync_command(
    subreddit: str = typer.Argument(
        ...,
        help="Name of subreddit to download from (with or without r/ prefix)",
    ),
    query: Optional[str] = typer.Option(
        None,
        help="Keyword search in title (AND-joined)",
    ),
    flair: Optional[str] = typer.Option(
        None,
        help="Include only posts whose flair matches regex",
    ),
    since: Optional[str] = typer.Option(
        None,
        help="ISO date or duration (3d, 6h) for oldest post",
    ),
    until: Optional[str] = typer.Option(
        None,
        help="ISO date or duration (3d, 6h) for newest post",
    ),
    min_score: Optional[int] = typer.Option(
        None,
        help="Skip submissions below Reddit score",
        min=0,
    ),
    media: Optional[str] = typer.Option(
        None,
        help="Filter by media type",
    ),
    user: Optional[List[str]] = typer.Option(
        None,
        help="Only posts by specific author(s)",
    ),
    limit: int = typer.Option(
        100,
        help="Max submissions fetched this run",
        min=1,
        max=1000,
    ),
    allow_nsfw: bool = typer.Option(
        False,
        help="Explicitly permit NSFW content",
    ),
    pushshift: bool = typer.Option(
        False,
        help="Fall back to Pushshift API when Reddit search is throttled",
    ),
    dry_run: bool = typer.Option(
        False,
        help="Show what would be downloaded without actually downloading",
    ),
):
    """
    Download media from a subreddit based on search criteria.
    """
    # Import here to avoid circular imports
    from grabber.search import SearchParams, fetch_iter, get_reddit_client
    from grabber.database import Database
    from grabber.downloader import process_submission
    from grabber.sync import sync_with_resume
    
    # Normalize subreddit name (remove r/ if present)
    if subreddit.startswith('r/'):
        subreddit = subreddit[2:]
    
    # Display search parameters
    console.print(f"[bold]Subreddit:[/] r/{subreddit}")
    
    if query:
        console.print(f"[bold]Query:[/] {query}")
    
    # Get configuration
    config = _get_config()
    output_dir = pathlib.Path(config.get("output_dir", "./downloads"))
    
    # Get database path
    db_dir = pathlib.Path.home() / ".local" / "share" / "reddit-grabber"
    db_dir.mkdir(parents=True, exist_ok=True)
    db_path = db_dir / "grabber.db"
    
    # Initialize database
    db = Database(db_path)
    db.initialize()
    
    # Create search parameters from CLI arguments
    search_params = SearchParams(
        query=query,
        flair=flair,
        since=since,
        until=until,
        min_score=min_score,
        media=media,
        user=user,
        limit=limit,
        allow_nsfw=allow_nsfw,
        pushshift=pushshift
    )
    
    try:
        # Get Reddit client
        console.print(f"Authenticating with Reddit...")
        reddit = get_reddit_client(user_auth=True)
        
        if dry_run:
            # In dry run mode, preview the submissions that would be processed
            console.print("[bold]Action:[/] Would download media matching the following submissions:")
            console.print(f"[bold]Limit:[/] {limit} submissions")
            
            # Get submissions iterator
            submissions_iter = fetch_iter(subreddit, search_params)
            
            # Preview the submissions that would be processed
            submission_count = 0
            for submission in submissions_iter:
                submission_count += 1
                console.print(f"[bold]{submission_count}.[/] {submission.title} [dim](Score: {submission.score})[/]")
                
            console.print(f"\nFound [bold]{submission_count}[/] submissions matching criteria")
        else:
            # In real mode, process and download the submissions
            console.print(f"[bold green]Syncing[/] media from r/{subreddit}")
            
            # Create a processing function that will handle each submission
            def process_func(submission, db):
                console.print(f"Processing: {submission.title}")
                return process_submission(submission, db, output_dir, dry_run)
            
            # Start the sync process with resume capability
            total, success_count = sync_with_resume(
                subreddit=subreddit,
                params=search_params,
                db=db,
                process_func=process_func,
                resume=True
            )
            
            # Show summary
            console.print(f"[bold green]Completed:[/] {success_count}/{total} submissions processed successfully")
    
    except Exception as e:
        error_console.print(f"[bold red]Error:[/] {str(e)}")
        raise typer.Exit(code=1)
    
    finally:
        # Close the database
        db.close()
    
    # Note: The summary is now printed inside the try block above


@app.command("db-vacuum")
def db_vacuum_command():
    """
    Clean and optimize the SQLite cache database.
    """
    console.print("[bold]Cleaning[/] and optimizing SQLite cache")
    # Actual database vacuum functionality will be implemented later
    console.print("Database optimization not yet implemented")


@app.command("version")
def version_command():
    """
    Display the current version of Reddit Grabber.
    """
    console.print(f"Reddit Grabber v{__version__}")
    console.print(f"Python {sys.version.split()[0]}")
    console.print(f"Platform: {sys.platform}")


@auth_app.command("login")
def auth_login(password_auth: bool = typer.Option(False, "--password", "-p", help="Use password authentication instead of OAuth")):
    """
    Log in to your Reddit account.
    
    This allows access to restricted subreddits and higher API limits.
    """
    from grabber.auth import setup_user_auth
    
    console.print("[bold]Reddit Authentication[/]")
    try:
        setup_user_auth()
        console.print("\n[bold green]Authentication setup complete![/]")
    except Exception as e:
        error_console.print(f"[bold red]Error setting up authentication:[/] {e}")
        raise typer.Exit(code=1)


@auth_app.command("setup")
def auth_setup():
    """
    Set up Reddit API credentials.
    
    This guides you through creating a Reddit app and setting up credentials.
    """
    from grabber.auth import prompt_for_credentials
    
    console.print("[bold]Reddit API Credential Setup[/]")
    try:
        client_id, client_secret = prompt_for_credentials()
        console.print(f"\n[bold green]Credentials saved successfully![/]")
    except Exception as e:
        error_console.print(f"[bold red]Error setting up credentials:[/] {e}")
        raise typer.Exit(code=1)


@auth_app.command("status")
def auth_status():
    """
    Check authentication status with Reddit.
    """
    from grabber.auth import get_reddit_instance
    
    console.print("[bold]Reddit Authentication Status[/]")
    try:
        # Try to get a Reddit instance with user auth
        reddit = get_reddit_instance(user_auth=True)
        user = reddit.user.me()
        
        if user:
            console.print(f"[bold green]Authenticated as:[/] u/{user.name}")
            karma = user.link_karma + user.comment_karma
            console.print(f"Account karma: {karma}")
            console.print(f"Account created: {time.strftime('%Y-%m-%d', time.gmtime(user.created_utc))}")
        else:
            console.print("[bold yellow]Not logged in with a user account.[/]")
            console.print("Use 'grabber auth login' to authenticate.")
    
    except Exception as e:
        error_console.print(f"[bold red]Authentication error:[/] {e}")
        console.print("Use 'grabber auth setup' to set up your API credentials.")
        console.print("Then use 'grabber auth login' to authenticate with your user account.")


if __name__ == "__main__":
    app()