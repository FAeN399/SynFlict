# Reddit Grabber

A cross-platform utility that downloads images and videos from Reddit submissions and subreddits.

## Features

- **Download Media**: Automatically downloads all images and videos from Reddit posts
- **Subreddit Sync**: Traverse a subreddit with custom filters and download matching media
- **Smart Rate Limiting**: Dynamically adjusts request rate based on Reddit API headers
- **De-duplication**: Avoids downloading the same content twice
- **Multiple UI Options**: Command-line interface, Text-based UI, and optional Qt desktop interface

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/reddit-grabber.git
cd reddit-grabber

# Install with pip
pip install -e .

# Optional: Install with GUI support
pip install -e ".[gui]"
```

## Usage

### Command Line Interface

```bash
# Download media from a specific Reddit post
grabber grab https://www.reddit.com/r/aww/comments/abcdef/cute_cat_picture/

# Sync media from a subreddit with filters
grabber sync r/wallpapers --query "nature" --min-score 100 --limit 50

# Show help
grabber --help
```

### Rate Limiting

Reddit Grabber implements automatic rate limit back-off to prevent hitting Reddit's API limits:

- Monitors `X-Ratelimit-*` headers from Reddit API responses
- Dynamically adjusts request timing based on remaining quota
- Falls back to safe limits when headers are unavailable
- Provides visual feedback on rate limit status

## Configuration

Create a `.env` file in your project directory with your Reddit API credentials:

```
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=reddit-grabber/0.1.0 (by /u/your_username)
```

## Development

### Setting Up Development Environment

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

### Project Structure

- `grabber/`: Main package
  - `ratelimit.py`: Rate limiting implementation
  - `cli.py`: Command-line interface
  - `reddit.py`: Reddit API interaction
  - `downloader.py`: Media downloading logic
  - `ui/`: User interface implementations

## License

MIT License
