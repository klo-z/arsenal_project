"""
Arsenal: A Kali Linux Tool Orchestrator

This is the main entrypoint for the Arsenal application.
It follows the best practice of keeping the __main__.py file minimal,
delegating the actual application logic to other modules.
"""

from .cli import main

if __name__ == "__main__":
    main()

