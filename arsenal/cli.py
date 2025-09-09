"""
Handles command-line argument parsing and the main control flow of the application.
"""
import argparse
import sys
from .core import menu
from .core import tools_loader

def main():
    """
    The main function that orchestrates the application's lifecycle.
    """
    #
    # Future implementation will handle CLI arguments for non-interactive mode.
    # For now, we focus on the interactive menu.
    #
    parser = argparse.ArgumentParser(description="Arsenal - A Kali Linux Tool Orchestrator")
    # Add arguments here in the future, e.g., --tool, --cmd, etc.

    args = parser.parse_args()

    # --- Application Startup ---
    # 1. Load all tool definitions from the data directory.
    print("Loading tool definitions...")
    try:
        tools = tools_loader.load_tools()
        if not tools:
            print("Error: No tool definitions found. Exiting.")
            sys.exit(1)
        print(f"Successfully loaded {len(tools)} tools.")
    except Exception as e:
        print(f"Fatal Error: Could not load tool definitions. {e}")
        sys.exit(1)


    # 2. Check for dependencies (Future Implementation)
    # installer.check_and_install(tools)

    # 3. Check for Rules of Engagement (Future Implementation)
    # roes.check_roe()

    # 4. Start the main interactive menu
    try:
        menu.start_main_menu(tools)
    except KeyboardInterrupt:
        print("\nExiting Arsenal. Goodbye!")
        sys.exit(0)

if __name__ == '__main__':
    main()

