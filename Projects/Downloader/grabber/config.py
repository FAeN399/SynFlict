"""
Configuration loading module for Reddit Grabber.

Handles loading configuration from various sources in order of precedence:
1. CLI arguments
2. Environment variables with GRABBER_ prefix
3. User config file (~/.config/reddit-grabber/config.toml)
4. Project-local config file (grabber.toml in current directory)
"""

import os
import pathlib
from typing import Dict, Any, Optional, Union

# Try to import toml parsing library (tomli for Python < 3.11, tomllib for >= 3.11)
try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib
    except ImportError:
        tomllib = None


def load_config(
    cli_args_or_path: Optional[Union[Dict[str, Any], str, pathlib.Path]] = None,
    config_file: Optional[pathlib.Path] = None
) -> Dict[str, Any]:
    """
    Load configuration from various sources in order of precedence.
    
    Args:
        cli_args_or_path: Command-line arguments that override other sources,
                          or a path string to a config file
        config_file: Explicit path to config file
        
    Returns:
        Dictionary with merged configuration
    """
    config = {}
    
    # Handle string or Path arguments for GUI usage
    if isinstance(cli_args_or_path, (str, pathlib.Path)):
        # If we got a string path, use it as the config file
        config_file = pathlib.Path(cli_args_or_path)
        cli_args = None
    else:
        # Otherwise it's the CLI args dictionary
        cli_args = cli_args_or_path
    
    # 4. Load from project config files (lowest precedence)
    
    # Check for INI file first (simpler format)
    project_ini = pathlib.Path("config.ini")
    if project_ini.exists():
        try:
            import configparser
            ini_config = configparser.ConfigParser()
            ini_config.read(project_ini)
            
            # Process Reddit section
            if "reddit" in ini_config:
                for key, value in ini_config["reddit"].items():
                    # Strip quotes from values (critical for API credentials)
                    stripped_value = value.strip('"\'')
                    config_key = f"reddit_{key}"
                    config[config_key] = stripped_value
                print(f"Loaded Reddit credentials from {project_ini}")
        except Exception as e:
            # Log error but continue
            print(f"Warning: Error loading project INI file: {e}")
    
    # Also check for TOML file
    project_config = pathlib.Path("grabber.toml")
    if project_config.exists() and tomllib:
        try:
            with open(project_config, "rb") as f:
                toml_data = tomllib.load(f)
                _merge_config_from_toml(config, toml_data)
        except Exception as e:
            # Log error but continue
            print(f"Warning: Error loading project TOML file: {e}")
    
    # 3. Load from user config file
    user_config_dir = pathlib.Path.home() / ".config" / "reddit-grabber"
    user_config_file = user_config_dir / "config.toml"
    
    if user_config_file.exists() and tomllib:
        try:
            with open(user_config_file, "rb") as f:
                toml_data = tomllib.load(f)
                _merge_config_from_toml(config, toml_data)
        except Exception as e:
            # Log error but continue
            print(f"Warning: Error loading user config file: {e}")
    
    # Override with explicit config file if provided
    if config_file and config_file.exists() and tomllib:
        try:
            with open(config_file, "rb") as f:
                toml_data = tomllib.load(f)
                _merge_config_from_toml(config, toml_data)
        except Exception as e:
            # Log error but continue
            print(f"Warning: Error loading specified config file: {e}")
    
    # 2. Load from environment variables with GRABBER_ prefix
    for key, value in os.environ.items():
        if key.startswith("GRABBER_"):
            config_key = key[8:].lower()
            config[config_key] = _convert_value(value)
    
    # Load Reddit API credentials from environment
    for key in ["REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET", "REDDIT_USER_AGENT", 
               "REDDIT_USERNAME", "REDDIT_PASSWORD"]:
        if key in os.environ:
            config_key = key.lower()
            config[config_key] = os.environ[key]
            
    # Load Reddit credentials from credentials file
    creds_path = pathlib.Path.home() / ".config" / "reddit-grabber" / "credentials.ini"
    if creds_path.exists():
        try:
            import configparser
            creds = configparser.ConfigParser()
            creds.read(creds_path)
            
            if "reddit" in creds:
                for key, value in creds["reddit"].items():
                    # Strip quotes from values (critical for API credentials)
                    stripped_value = value.strip('"\'')
                    config_key = f"reddit_{key}"
                    # Only set if not already set from environment
                    if config_key not in config:
                        config[config_key] = stripped_value
        except Exception as e:
            # Log error but continue
            print(f"Warning: Error loading Reddit credentials: {e}")
    
    # 1. Override with CLI arguments (highest precedence)
    if cli_args:
        for key, value in cli_args.items():
            if value is not None:  # Only override if value is provided
                config[key] = value
    
    return config


def _merge_config_from_toml(config: Dict[str, Any], toml_data: Dict[str, Any]) -> None:
    """
    Merge TOML configuration into the config dictionary.
    
    Args:
        config: Configuration dictionary to update
        toml_data: TOML data loaded from file
    """
    # Handle grabber section
    if "grabber" in toml_data:
        for key, value in toml_data["grabber"].items():
            config[key] = value
    
    # Handle reddit section
    if "reddit" in toml_data:
        for key, value in toml_data["reddit"].items():
            config[f"reddit_{key}"] = value


def _convert_value(value: str) -> Any:
    """
    Convert string value to appropriate type.
    
    Args:
        value: String value to convert
        
    Returns:
        Converted value (int, float, bool, or original string)
    """
    # Convert 'true'/'false' strings to boolean
    if value.lower() in ["true", "yes", "1"]:
        return True
    elif value.lower() in ["false", "no", "0"]:
        return False
        
    # Try to convert to numbers
    try:
        # Try integer first
        return int(value)
    except ValueError:
        try:
            # Then try float
            return float(value)
        except ValueError:
            # Otherwise, return as is
            return value


def save_config(config: Dict[str, Any], config_path: str) -> bool:
    """
    Save configuration to a file.
    
    Args:
        config: Configuration dictionary to save
        config_path: Path to the configuration file
        
    Returns:
        True if saved successfully, False otherwise
    """
    try:
        # If the file is an INI file, use configparser
        if config_path.endswith('.ini'):
            import configparser
            ini_config = configparser.ConfigParser()
            
            # Convert flat dictionary to sections
            for key, value in config.items():
                if isinstance(value, dict):
                    # This is a section
                    if key not in ini_config:
                        ini_config[key] = {}
                    for subkey, subvalue in value.items():
                        ini_config[key][subkey] = str(subvalue)
                else:
                    # Add to DEFAULT section
                    if 'DEFAULT' not in ini_config:
                        ini_config['DEFAULT'] = {}
                    ini_config['DEFAULT'][key] = str(value)
            
            # Write to file
            with open(config_path, 'w') as f:
                ini_config.write(f)
                
        # If it's a TOML file and tomllib is available
        elif config_path.endswith('.toml') and tomllib:
            # Unfortunately tomllib doesn't support writing, so we need to use a different library
            try:
                import toml
                with open(config_path, 'w') as f:
                    toml.dump(config, f)
            except ImportError:
                print("Warning: TOML writing not supported. Please install 'toml' package.")
                return False
        else:
            print(f"Warning: Unsupported config file format: {config_path}")
            return False
            
        return True
    except Exception as e:
        print(f"Error saving config: {e}")
        return False
