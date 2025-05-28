"""
Manifest JSON generation and writing for Reddit Grabber.

Handles creating, storing, and retrieving metadata about downloaded submissions.
"""

import json
import logging
import pathlib
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional

from grabber.reddit import fetch_submission

logger = logging.getLogger(__name__)


@dataclass
class Manifest:
    """
    Represents metadata about a downloaded Reddit submission.
    
    This follows the manifest JSON schema as specified in the functional spec.
    """
    id: str
    subreddit: str
    title: str
    author: str
    permalink: str
    utc_timestamp: int
    score: int
    flair: Optional[str] = None
    downloaded: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the manifest to a dictionary suitable for JSON serialization.
        
        Returns:
            Dictionary representation of the manifest
        """
        return asdict(self)


def create_manifest_from_submission(submission_id: str, downloaded_files: List[str]) -> Manifest:
    """
    Create a manifest from a Reddit submission.
    
    Args:
        submission_id: ID of the Reddit submission
        downloaded_files: List of filenames that were downloaded
        
    Returns:
        Manifest object with submission metadata
    """
    logger.info(f"Creating manifest for submission: {submission_id}")
    
    # Fetch the submission data
    submission = fetch_submission(submission_id)
    
    # Extract subreddit name (can be either a string or an object with display_name attribute)
    if hasattr(submission.subreddit, 'display_name'):
        subreddit_name = submission.subreddit.display_name
    else:
        subreddit_name = str(submission.subreddit)
    
    # Create the manifest
    manifest = Manifest(
        id=submission.id,
        subreddit=subreddit_name,
        title=submission.title,
        author=f"u/{submission.author.name}" if hasattr(submission.author, 'name') else submission.author,
        permalink=submission.permalink,
        utc_timestamp=int(submission.created_utc),
        score=submission.score,
        flair=submission.link_flair_text if hasattr(submission, 'link_flair_text') else None,
        downloaded=downloaded_files
    )
    
    return manifest


def write_manifest(manifest: Manifest, output_dir: pathlib.Path) -> pathlib.Path:
    """
    Write the manifest to a JSON file.
    
    Args:
        manifest: Manifest object to write
        output_dir: Directory to write the manifest to
        
    Returns:
        Path to the written manifest file
    """
    # Ensure the output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create the manifest file path
    manifest_path = output_dir / "manifest.json"
    
    # Write the manifest to the file
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest.to_dict(), f, indent=2, ensure_ascii=False)
    
    logger.info(f"Wrote manifest to: {manifest_path}")
    
    return manifest_path


def read_manifest(manifest_path: pathlib.Path) -> Optional[Manifest]:
    """
    Read a manifest from a JSON file.
    
    Args:
        manifest_path: Path to the manifest file
        
    Returns:
        Manifest object, or None if the file doesn't exist or is invalid
    """
    if not manifest_path.exists():
        logger.warning(f"Manifest file not found: {manifest_path}")
        return None
    
    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest_data = json.load(f)
        
        # Create a Manifest object from the data
        manifest = Manifest(
            id=manifest_data["id"],
            subreddit=manifest_data["subreddit"],
            title=manifest_data["title"],
            author=manifest_data["author"],
            permalink=manifest_data["permalink"],
            utc_timestamp=manifest_data["utc_timestamp"],
            score=manifest_data["score"],
            flair=manifest_data.get("flair"),
            downloaded=manifest_data.get("downloaded", [])
        )
        
        return manifest
    
    except (json.JSONDecodeError, KeyError) as e:
        logger.error(f"Error reading manifest file: {e}")
        return None
