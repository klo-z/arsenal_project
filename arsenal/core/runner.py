import subprocess
import sys
from .colors import Colors  # <-- THIS IS THE UPDATED IMPORT

def execute_command(command: list):
    """
    Executes a command in a subprocess, streaming its output in real-time.

    Args:
        command (list): The command and its arguments as a list of strings.
    """
    try:
        # Use Popen for real-time output streaming
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1  # Line-buffered
        )

        # Read and print output line by line
        if process.stdout:
            for line in iter(process.stdout.readline, ''):
                print(line, end='')
        
        process.wait() # Wait for the process to complete
        
        if process.returncode != 0:
            print(f"\n{Colors.FAIL}Command finished with an error (exit code: {process.returncode}).{Colors.ENDC}")

    except FileNotFoundError:
        print(f"{Colors.FAIL}Error: The command '{command[0]}' was not found.{Colors.ENDC}")
        print(f"{Colors.WARNING}Please ensure the tool is installed and in your system's PATH.{Colors.ENDC}")
    except PermissionError:
        print(f"{Colors.FAIL}Error: Permission denied to execute '{command[0]}'.{Colors.ENDC}")
        print(f"{Colors.WARNING}Try running Arsenal with 'sudo' privileges.{Colors.ENDC}")
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Command interrupted by user.{Colors.ENDC}")
        if 'process' in locals() and process.poll() is None:
            process.terminate() # Terminate the child process
    except Exception as e:
        print(f"{Colors.FAIL}An unexpected error occurred: {e}{Colors.ENDC}")


