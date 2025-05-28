"""
Test mode utilities for the grabber application.
"""

import os
import sys
import pathlib
import logging
import random
from types import SimpleNamespace
from typing import List, Optional
from unittest.mock import MagicMock

import praw

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def create_mock_submission(
    submission_id: str = "bc4hkg",
    title: str = "Paradise on Earth Lake Louise Banff Canada",
    url: str = "https://i.redd.it/mockimage.jpg",
    subreddit: str = "EarthPorn",
    author: str = "mock_author",
    score: int = 9999,
    over_18: bool = False,
) -> MagicMock:
    """
    Create a mock submission for testing.
    
    Args:
        submission_id: ID of the submission
        title: Title of the submission
        url: URL of the media
        subreddit: Name of the subreddit
        author: Username of the author
        score: Score of the submission
        over_18: If True, mark the submission as NSFW (over 18)
        
    Returns:
        Mock submission object using SimpleNamespace instead of MagicMock
    """
    # Create mock author and subreddit using SimpleNamespace
    mock_author = SimpleNamespace(name=author)
    mock_subreddit = SimpleNamespace(display_name=subreddit)
    
    # Create mock media metadata for gallery support
    media_metadata = {
        "item1": {"s": {"u": "https://i.redd.it/mockimage1.jpg"}},
        "item2": {"s": {"u": "https://i.redd.it/mockimage2.jpg"}}
    }
    
    # Create the mock submission using SimpleNamespace
    mock_submission = SimpleNamespace(
        id=submission_id,
        title=title,
        url=url,
        permalink=f"/r/{subreddit}/comments/{submission_id}/title/",
        score=score,
        author=mock_author,
        created_utc=1609459200,  # 2021-01-01
        subreddit=mock_subreddit,
        is_self=False,
        over_18=over_18,  # This will properly evaluate as a boolean
        media_metadata=media_metadata
    )
    
    return mock_submission


def create_mock_submissions(count: int = 5, subreddit: str = "EarthPorn", nsfw_ratio: float = 0.4) -> List[MagicMock]:
    """
    Create a list of mock submissions for testing.
    
    Args:
        count: Number of submissions to create
        subreddit: Name of the subreddit
        nsfw_ratio: Ratio of submissions that should be marked as NSFW (0.0 to 1.0)
        
    Returns:
        List of mock submission objects
    """
    submissions = []
    
    for i in range(count):
        submission_id = f"mock{i}"
        
        # Determine if this submission should be NSFW based on the ratio
        is_nsfw = (i % int(1/nsfw_ratio) == 0) if nsfw_ratio > 0 else False
        
        # Create different titles and URLs based on NSFW status
        if is_nsfw:
            title = f"[NSFW] Mock Submission {i} - Adult Content"
            url = f"https://i.redd.it/nsfw_mockimage{i}.jpg"
            # Use different subreddits for NSFW content
            sub = random.choice(["NSFWContent", "GoneWild", "AdultContent", "NSFW"])
        else:
            title = f"Mock Submission {i} - Beautiful Landscape"
            url = f"https://i.redd.it/mockimage{i}.jpg"
            sub = subreddit
        
        submission = create_mock_submission(
            submission_id=submission_id,
            title=title,
            url=url,
            subreddit=sub,
            author=f"user{i}",
            score=1000 + i * 100,
            over_18=is_nsfw  # Set the NSFW flag
        )
        
        submissions.append(submission)
    
    return submissions


def setup_test_environment(output_dir: Optional[pathlib.Path] = None) -> pathlib.Path:
    """
    Set up a test environment for the grabber application.
    
    Args:
        output_dir: Optional output directory
        
    Returns:
        Path to the output directory
    """
    # Set up mock mode
    os.environ["GRABBER_MOCK_MODE"] = "true"
    
    # Create a temporary output directory if not provided
    if output_dir is None:
        import tempfile
        temp_dir = tempfile.TemporaryDirectory()
        output_dir = pathlib.Path(temp_dir.name)
    
    # Ensure the output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Set environment variables
    os.environ["GRABBER_OUTPUT_DIR"] = str(output_dir)
    
    logger.info(f"Test environment set up with output directory: {output_dir}")
    
    return output_dir


def run_test_grab():
    """
    Test the grab command with mock data.
    """
    from grabber.search import get_reddit_client
    from grabber.database import Database
    from grabber.downloader import process_submission
    
    # Set up test environment
    output_dir = setup_test_environment()
    
    # Create a test database
    db_path = output_dir / "test.db"
    db = Database(db_path)
    db.initialize()
    
    try:
        # Get mock Reddit client
        reddit = get_reddit_client(user_auth=True, mock=True)
        
        # Get a mock submission
        submission = create_mock_submission()
        
        print(f"Processing mock submission: {submission.title}")
        print(f"Submission URL: {submission.url}")
        print(f"Subreddit: r/{submission.subreddit.display_name}")
        
        # Process the submission
        success = process_submission(submission, db, output_dir, dry_run=False)
        
        if success:
            print(f"Successfully processed mock submission!")
        else:
            print(f"Failed to process mock submission.")
    
    finally:
        # Close the database
        db.close()


def run_test_sync():
    """
    Test the sync command with mock data.
    """
    from grabber.search import SearchParams
    from grabber.database import Database
    from grabber.downloader import process_submission
    from grabber.sync import sync_with_resume
    
    # Set up test environment
    output_dir = setup_test_environment()
    
    # Create a test database
    db_path = output_dir / "test.db"
    db = Database(db_path)
    db.initialize()
    
    try:
        # Create mock submissions
        mock_submissions = create_mock_submissions(count=5)
        
        # Create a processing function
        def process_func(submission, db):
            print(f"Processing: {submission.title}")
            return process_submission(submission, db, output_dir, dry_run=False)
        
        # Mock the fetch_iter function
        from unittest.mock import patch
        with patch('grabber.sync.fetch_iter', return_value=iter(mock_submissions)):
            # Run sync with mock data
            total, success_count = sync_with_resume(
                subreddit="EarthPorn",
                params=SearchParams(limit=5),
                db=db,
                process_func=process_func,
                resume=True
            )
        
        print(f"Completed: {success_count}/{total} submissions processed successfully")
    
    finally:
        # Close the database
        db.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m grabber.test_mode [grab|sync]")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "grab":
        run_test_grab()
    elif command == "sync":
        run_test_sync()
    else:
        print(f"Unknown command: {command}")
        print("Available commands: grab, sync")
        sys.exit(1)
