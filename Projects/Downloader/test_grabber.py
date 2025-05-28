"""
Simple test script for the Reddit Grabber application.
"""

import os
import sys
import pathlib
import logging
from unittest.mock import MagicMock, patch

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Set up mock mode
os.environ["GRABBER_MOCK_MODE"] = "true"

# Create output directory
output_dir = pathlib.Path("./test_downloads")
output_dir.mkdir(parents=True, exist_ok=True)
os.environ["GRABBER_OUTPUT_DIR"] = str(output_dir)

# Import grabber modules
from grabber.database import Database
from grabber.search import get_reddit_client, SearchParams
from grabber.downloader import process_submission, extract_media_urls


def create_mock_submission():
    """Create a mock Reddit submission for testing."""
    mock_submission = MagicMock()
    mock_submission.id = "testid123"
    mock_submission.title = "Test Submission"
    mock_submission.url = "https://i.redd.it/testimage.jpg"
    mock_submission.permalink = "/r/test/comments/testid123/test_submission/"
    mock_submission.score = 9999
    mock_submission.author = MagicMock(name="test_user")
    mock_submission.created_utc = 1609459200  # 2021-01-01
    mock_submission.subreddit = MagicMock(display_name="test")
    mock_submission.is_self = False
    
    # Add gallery metadata
    mock_submission.media_metadata = {
        "item1": {"s": {"u": "https://i.redd.it/image1.jpg"}},
        "item2": {"s": {"u": "https://i.redd.it/image2.jpg"}}
    }
    
    return mock_submission


def test_grab_command():
    """Test the grab command functionality."""
    print("\n=== Testing Grab Command ===")
    
    # Create database
    db_path = output_dir / "test.db"
    
    # Make sure the output directory exists
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Initialize database with a string path
    db = Database(str(db_path))
    db.initialize()
    
    try:
        # Create a mock submission
        submission = create_mock_submission()
        
        # Process the submission
        print(f"Processing: {submission.title}")
        print(f"URL: {submission.url}")
        
        # Extract media URLs
        media_urls = extract_media_urls(submission)
        print(f"Found {len(media_urls)} media URLs:")
        for url in media_urls:
            print(f"  - {url}")
        
        # Process the submission (dry run for testing)
        success = process_submission(submission, db, output_dir, dry_run=True)
        
        if success:
            print("\n✅ Grab command test passed!")
        else:
            print("\n❌ Grab command test failed!")
            
    finally:
        # Close the database
        db.close()


def test_sync_command():
    """Test the sync command functionality."""
    print("\n=== Testing Sync Command ===")
    
    # Create database
    db_path = output_dir / "test.db"
    db = Database(str(db_path))
    db.initialize()
    
    try:
        # Create mock submissions
        mock_submissions = []
        for i in range(5):
            mock_sub = MagicMock()
            mock_sub.id = f"test{i}"
            mock_sub.title = f"Test Submission {i}"
            mock_sub.url = f"https://i.redd.it/image{i}.jpg"
            mock_sub.permalink = f"/r/test/comments/test{i}/test_submission_{i}/"
            mock_sub.score = 1000 + i * 100
            mock_sub.author = MagicMock(name=f"user{i}")
            mock_sub.created_utc = 1609459200 + i * 86400  # Each day after Jan 1, 2021
            mock_sub.subreddit = MagicMock(display_name="test")
            mock_sub.is_self = False
            mock_submissions.append(mock_sub)
        
        # Mock the fetch_iter function
        with patch('grabber.sync.fetch_iter', return_value=iter(mock_submissions)):
            from grabber.sync import sync_with_resume
            
            # Define a process function
            def process_func(submission, db):
                print(f"Processing: {submission.title}")
                return True
            
            # Run sync with resume
            stats = sync_with_resume(
                subreddit="test",
                params=SearchParams(limit=5),
                db=db,
                process_func=process_func,
                resume=True
            )
            
            # Extract statistics
            processed = stats["processed"]
            total = stats["total"]
            skipped = stats["skipped"]
            failed = stats["failed"]
            duration = stats["duration"]
            
            print(f"\nStatistics:")
            print(f"  Processed: {processed}")
            print(f"  Skipped: {skipped}")
            print(f"  Failed: {failed}")
            print(f"  Total: {total}")
            print(f"  Duration: {duration:.2f}s")
            
            if processed > 0 and failed == 0:
                print("\n✅ Sync command test passed!")
            else:
                print("\n❌ Sync command test failed!")
                
    finally:
        # Close the database
        db.close()


def cleanup():
    """Clean up test files."""
    # Clean up the database
    db_path = output_dir / "test.db"
    if db_path.exists():
        try:
            db_path.unlink()
            print(f"Deleted test database: {db_path}")
        except Exception as e:
            print(f"Failed to delete test database: {e}")


if __name__ == "__main__":
    try:
        # Run tests
        if len(sys.argv) > 1:
            if sys.argv[1] == "grab":
                test_grab_command()
            elif sys.argv[1] == "sync":
                test_sync_command()
            else:
                print(f"Unknown test: {sys.argv[1]}")
                print("Available tests: grab, sync")
        else:
            # Run all tests
            test_grab_command()
            test_sync_command()
        
    finally:
        # Clean up (optional - comment out to keep test files)
        # cleanup()
        pass
