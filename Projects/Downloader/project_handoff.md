# Reddit Media Grabber: Project Handoff Document

## Project Overview

The Reddit Media Grabber is a Python-based application designed to download images, videos, GIFs, and other media content from Reddit. It provides multiple ways to browse and download content:

1. **Single Post Download**: Download media from a specific Reddit post URL
2. **Subreddit-Specific Downloads**: Download media from a specific subreddit with various sorting options
3. **Global Reddit Search**: Search across all of Reddit with keyword filtering
4. **Subreddit Sync**: Track and download media from multiple subreddits

## Current Project State

### Key Components Implemented

1. **Authentication System**
   - Script-type Reddit app authentication using PRAW
   - Password-based authentication with username/password
   - Fallback to mock mode for testing without credentials
   - 2FA support

2. **Media Downloading**
   - Support for various media types (images, videos, GIFs)
   - Download queue management with ThreadPoolExecutor
   - Progress tracking
   - Media type filtering

3. **Global Search**
   - Keyword-based search across Reddit
   - Sort/time period filtering
   - NSFW content toggle

4. **Subreddit Downloads**
   - Command-line interface for downloading from specific subreddits
   - Sorting options (hot, new, top, rising, controversial)
   - Time period filters
   - Media type filtering

5. **Configuration**
   - Config.ini file for storing Reddit API credentials
   - NSFW content control (per-session or persistent)
   - Default settings management

### Current Structure

```
Downloader/
├── grabber/                     # Main package
│   ├── __init__.py              # Version info and package initialization
│   ├── auth.py                  # Reddit API authentication
│   ├── config.py                # Configuration loading
│   ├── download_manager.py      # Download queue and history management
│   ├── downloader.py            # Media downloading logic
│   ├── global_search.py         # Global Reddit search
│   ├── subreddit_downloader.py  # Subreddit media processing
│   └── ratelimit.py             # Rate limiting for API calls
├── tests/                       # Test suite
├── downloads/                   # Default download directory
├── config.ini                   # Configuration file
├── gui.py                       # Main GUI implementation
├── fixed_subreddit_downloader.py # Subreddit downloader script
├── theme.py                     # UI styling and theme definitions
└── ui_design_prompt.md          # UI design brief
```

## Authentication

The application uses PRAW (Python Reddit API Wrapper) and requires authentication with Reddit's API:

1. **API Credentials**: Stored in `config.ini` file with these fields:
   - `client_id`: Reddit API client ID
   - `client_secret`: Reddit API client secret
   - `username`: Reddit username
   - `user_agent`: String identifying the application
   
2. **Authentication Flow**:
   - App first tries to use stored credentials from `config.ini`
   - If password is required but not stored, it prompts the user
   - Support for 2FA with the format `password:2fa_code`
   - Falls back to mock mode for testing if authentication fails

### Mock Mode

Mock mode allows testing the application without actual Reddit API access. It's activated when:
- Authentication fails
- Environment variable `GRABBER_MOCK_MODE` is set
- `--mock` command line flag is used

## Core Features & Implementation Details

### 1. Download Manager (`grabber.download_manager`)

- **DownloadItem Class**: Represents a file to be downloaded
  - Parameters: `item_id`, `item_type`, `url`, `output_dir`, `metadata`
  - Metadata stores info like post title, author, subreddit

- **DownloadManager Class**: Handles download queue and parallel downloads
  - Manages concurrent downloads with ThreadPoolExecutor
  - Tracks download progress and history
  - Handles different media types (images, videos, etc.)

### 2. Subreddit Downloader (`fixed_subreddit_downloader.py`)

- **Command-line Interface**:
  - Accepts parameters: subreddit, sort, time filter, media type, limit, NSFW
  - Example: `python fixed_subreddit_downloader.py earthporn --sort top --time week --media image --limit 50 --nsfw`

- **NSFW Content Handling**:
  - NSFW content is off by default for safety
  - Three ways to enable:
    1. `--nsfw` flag (prompt confirmation)
    2. `--always-allow-nsfw` flag (store in config)
    3. Setting `allow_nsfw = true` in `config.ini`

### 3. Global Search (`grabber.global_search`)

- Searches across all of Reddit with keywords
- Filters for media type, sort order, time period
- Returns posts with downloadable media

## UI Implementation

### Current GUI

The existing GUI (`gui.py`) implements a basic interface with:
- Tab-based navigation
- Forms for download options
- Progress indicators
- Queue and history views

### Proposed UI Enhancement

A new UI design has been specified in `ui_design_prompt.md` with:
- Purple primary color (#9C27B0) and yellow secondary color (#FFC107)
- Material design-inspired interface
- Tabbed organization
- Card-based content display
- Light and dark theme support

### Theme Implementation

A theming system has been started in `theme.py` that includes:
- Color definitions for light and dark themes
- Stylesheet generators
- Helper functions for styling widgets consistently

## Known Issues & Limitations

1. **Authentication Issues**:
   - Reddit's API can sometimes return 401 errors
   - 2FA implementation needs more testing

2. **Media Extraction**:
   - Some complex media types (galleries, embedded media) may not download correctly
   - Reddit video downloading requires combining separate video and audio streams

3. **GUI Performance**:
   - Current GUI may become unresponsive during heavy downloads
   - Thread safety issues with Qt's signals and slots need careful handling

4. **Error Handling**:
   - More robust error recovery needed in download process
   - Better user feedback for failed downloads

## Next Development Steps

### Critical Priorities

1. **Complete UI Implementation**:
   - Implement new UI design based on `ui_design_prompt.md`
   - Add proper full-screen support
   - Ensure responsive design for different window sizes

2. **Subreddit Download Integration**:
   - Integrate `fixed_subreddit_downloader.py` functionality into the main GUI
   - Add UI elements for all subreddit download options

3. **Error Handling**:
   - Improve error reporting and recovery
   - Add logging system for debugging
   - Implement retry mechanisms for failed downloads

### Future Enhancements

1. **Media Management**:
   - Media organization by subreddit/category
   - Duplicate detection
   - Local media browsing

2. **User Profiles**:
   - Save and load user preferences
   - Multiple authentication profiles

3. **Advanced Filtering**:
   - Content filtering by score, comment count, etc.
   - Custom tag-based filtering
   - NSFW content blur/preview options

4. **Scheduling**:
   - Schedule downloads for specific times
   - Periodic sync of favorite subreddits

5. **Export/Import**:
   - Export download history
   - Import/export settings

## Development Environment

### Dependencies

The project relies on these key dependencies:
- **PRAW**: Python Reddit API Wrapper
- **PySide6**: Qt for Python (GUI framework)
- **Requests**: HTTP library for downloading media
- **Configparser**: For handling configuration files

### Setup Instructions

1. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt  # Create this file with all dependencies
   ```

3. **Reddit API Setup**:
   - Create a Reddit account
   - Go to https://www.reddit.com/prefs/apps
   - Create a new "script" type app
   - Copy client ID and secret to `config.ini`

### Testing

Run the test suite to verify functionality:
```bash
pytest tests/
```

### Debugging

The application has various debugging options:
- Set `GRABBER_MOCK_MODE=1` environment variable to use mock data
- Run with `--mock` flag to bypass Reddit API calls
- Set logging level for more verbose output

## Conclusion

The Reddit Media Grabber is a functional application with solid core functionality but requires UI improvements and some feature integrations. The authentication system works well with script-type Reddit apps, and the download system can handle various media types. The next developer should focus on implementing the new UI design and integrating the subreddit download functionality into the main GUI.

## Contact Information

For questions about this project:
- Original developer: [Your contact information]
- Reddit API documentation: https://www.reddit.com/dev/api/
- PRAW documentation: https://praw.readthedocs.io/
