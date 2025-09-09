"""
This module is responsible for discovering, loading, and validating
the tool definition JSON files from the data directory.
"""
import os
import json
from typing import List, Dict, Any

def load_tools() -> List[Dict[str, Any]]:
    """
    Finds and loads all tool definition .json files.

    Scans the 'data/tools' directory relative to this script's location,
    parses each JSON file, and returns a list of tool definitions.

    Returns:
        A list of dictionaries, where each dictionary is a parsed tool definition.
        Returns an empty list if the directory doesn't exist or contains no valid files.
    """
    tools = []
    # Construct a path to the 'data/tools' directory relative to this file
    # This makes the path independent of where the script is run from.
    script_dir = os.path.dirname(__file__)
    data_dir = os.path.join(script_dir, '..', 'data', 'tools')

    if not os.path.isdir(data_dir):
        print(f"Error: Tools directory not found at {data_dir}")
        return []

    for filename in os.listdir(data_dir):
        if filename.endswith('.json'):
            file_path = os.path.join(data_dir, filename)
            try:
                with open(file_path, 'r') as f:
                    tool_data = json.load(f)
                    # Basic validation: ensure required keys exist
                    if 'name' in tool_data and 'commands' in tool_data:
                        tools.append(tool_data)
                    else:
                        print(f"Warning: Skipping invalid tool file (missing keys): {filename}")
            except json.JSONDecodeError:
                print(f"Warning: Could not decode JSON from file: {filename}")
            except Exception as e:
                print(f"Warning: An error occurred while loading {filename}: {e}")

    # Sort tools alphabetically by name for a consistent menu order
    tools.sort(key=lambda x: x['name'])
    return tools

