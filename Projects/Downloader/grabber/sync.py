"""
Sync functionality for downloading Reddit submissions.

Provides functionality for syncing submissions from a subreddit,
with support for resuming interrupted downloads.
"""

import logging
import time
from typing import Optional, List, Dict, Any, Callable, Iterator

from grabber.database import Database
from grabber.search import SearchParams, fetch_iter

logger = logging.getLogger(__name__)


def sync_with_resume(
    subreddit: str,
    params: SearchParams,
    db: Database,
    process_func: Callable = None,
    resume: bool = False,
    skip_downloaded: bool = False,
    checkpoint_interval: int = 10
) -> Dict[str, Any]:
    """
    Sync submissions from a subreddit with resume capability.
    
    Args:
        subreddit: Name of the subreddit to sync
        params: Search parameters
        db: Database instance
        process_func: Function to process each submission (takes submission and db as args)
        resume: Whether to resume from the last position
        skip_downloaded: Whether to skip already downloaded submissions
        checkpoint_interval: Number of submissions to process before creating a checkpoint
        
    Returns:
        Statistics about the sync operation
    """
    logger.info(f"Starting sync for r/{subreddit} (resume={resume}, skip_downloaded={skip_downloaded})")
    
    # Initialize statistics
    stats = {
        "processed": 0,
        "skipped": 0,
        "failed": 0,
        "total": 0,
        "start_time": time.time()
    }
    
    # Get submissions iterator
    submissions = fetch_iter(subreddit, params)
    
    # Process submissions
    last_checkpoint_time = time.time()
    last_id = None
    already_processed = set()
    
    # If resuming, get a list of already processed submissions
    if resume:
        processed_posts = db.get_all_posts(downloaded_only=True)
        already_processed = {post['id'] for post in processed_posts}
        logger.info(f"Resuming sync, {len(already_processed)} submissions already processed")
    
    for submission in submissions:
        stats["total"] += 1
        submission_id = submission.id
        
        # Skip if we're resuming and this submission has already been processed
        if resume and submission_id in already_processed:
            logger.debug(f"Skipping already processed submission: {submission_id}")
            stats["skipped"] += 1
            continue
        
        # Skip if we're skipping downloaded submissions and this one is already downloaded
        if skip_downloaded and db.is_post_downloaded(submission_id):
            logger.debug(f"Skipping already downloaded submission: {submission_id}")
            stats["skipped"] += 1
            continue
        
        # Process the submission
        try:
            # Make sure the submission is in the database
            if not db.has_post(submission_id):
                db.add_post(submission_id, submission.permalink)
            
            # Process the submission if a process function is provided
            if process_func:
                result = process_func(submission, db)
                
                # If the process function returns False, stop processing
                if result is False:
                    logger.info(f"Processing interrupted at submission: {submission_id}")
                    break
            
            # Mark as processed
            stats["processed"] += 1
            last_id = submission_id
            already_processed.add(submission_id)  # Add to processed set
            
            # Create a checkpoint periodically
            if stats["processed"] % checkpoint_interval == 0:
                current_time = time.time()
                elapsed = current_time - last_checkpoint_time
                logger.info(f"Checkpoint: Processed {stats['processed']} submissions "
                           f"({checkpoint_interval / elapsed:.2f} submissions/s)")
                last_checkpoint_time = current_time
                
        except Exception as e:
            logger.error(f"Error processing submission {submission_id}: {e}")
            stats["failed"] += 1
    
    # Calculate final statistics
    stats["end_time"] = time.time()
    stats["duration"] = stats["end_time"] - stats["start_time"]
    stats["last_id"] = last_id
    
    logger.info(f"Sync completed for r/{subreddit}: "
               f"Processed {stats['processed']}, "
               f"Skipped {stats['skipped']}, "
               f"Failed {stats['failed']}, "
               f"Total {stats['total']} "
               f"in {stats['duration']:.2f}s")
    
    return stats


def process_submission(submission, db: Database) -> bool:
    """
    Process a Reddit submission.
    
    This is a stub that will be expanded later with actual download functionality.
    
    Args:
        submission: Reddit submission to process
        db: Database instance
        
    Returns:
        True if processing was successful, False otherwise
    """
    # This is a stub that will be expanded later
    logger.info(f"Processing submission: {submission.id} - {submission.title}")
    
    # Mark the submission as downloaded
    db.mark_post_downloaded(submission.id)
    
    return True
