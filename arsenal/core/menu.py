"""
This module handles the interactive menu system for the user.
It's responsible for displaying menus, getting user input,
and orchestrating the command execution flow.
"""
import os
import sys
from typing import List, Dict, Any
from . import runner # We will create runner.py next

# --- ANSI Color Codes for a better UI ---
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def clear_screen():
    """Clears the terminal screen."""
    # Works for both Linux/macOS ('posix') and Windows ('nt')
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Prints the main application banner."""
    banner = f"""
{Colors.RED}
             _____     _____   ______   _   _              _      
     /\     |  __ \   / ____| |  ____| | \ | |     /\     | |     
    /  \    | |__) | | (___   | |__    |  \| |    /  \    | |     
   / /\ \   |  _  /   \___ \  |  __|   | . ` |   / /\ \   | |     
  / ____ \  | | \ \   ____) | | |____  | |\  |  / ____ \  | |____ 
 /_/    \_\ |_|  \_\ |_____/  |______| |_| \_| /_/    \_\ |______|
                                                                  
                                                                  

{Colors.ENDC}
{Colors.YELLOW}                      A Kali Linux Tool Orchestrator{Colors.ENDC}
"""
    print(banner)

def get_user_inputs(inputs: List[Dict[str, Any]]) -> Dict[str, str]:
    """
    Prompts the user for required inputs based on the command's definition.

    Args:
        inputs: A list of input dictionaries from the tool's JSON definition.

    Returns:
        A dictionary mapping input names to the values provided by the user.
    """
    collected_inputs = {}
    print(f"\n{Colors.CYAN}--- Please provide the following details ---{Colors.ENDC}")
    for input_item in inputs:
        prompt_text = f"{Colors.GREEN}{input_item['prompt']}{Colors.ENDC}"
        if 'default' in input_item:
            prompt_text += f" (default: {input_item['default']}): "
        else:
            prompt_text += ": "

        while True:
            user_value = input(prompt_text).strip()
            if user_value:
                collected_inputs[input_item['name']] = user_value
                break
            if 'default' in input_item:
                collected_inputs[input_item['name']] = input_item['default']
                break
            if input_item.get('required', False):
                print(f"{Colors.RED}This field is required. Please provide a value.{Colors.ENDC}")
            else:
                collected_inputs[input_item['name']] = '' # Not required, can be empty
                break
    return collected_inputs

def handle_command_execution(command: Dict[str, Any]):
    """
    Handles the process of getting inputs for and executing a command.

    Args:
        command: The specific command dictionary chosen by the user.
    """
    user_values = get_user_inputs(command.get('inputs', []))
    
    # Build the final command list by substituting placeholders
    final_command = []
    for part in command['cmd_template']:
        # This simple replacement works for placeholders like {target}
        # It iterates through user values and replaces any matching placeholder
        placeholder = part.strip('{}')
        if placeholder in user_values:
            final_command.append(user_values[placeholder])
        else:
            final_command.append(part)

    print(f"\n{Colors.YELLOW}Executing: {' '.join(final_command)}{Colors.ENDC}\n")
    input("Press Enter to continue...")
    
    # Call the runner to execute the command
    runner.execute_command(final_command)

    print(f"\n{Colors.GREEN}--- Command finished. ---{Colors.ENDC}")
    input("Press Enter to return to the menu...")


def show_tool_submenu(tool: Dict[str, Any]):
    """
    Displays the submenu for a specific tool.

    Args:
        tool: The dictionary definition for the selected tool.
    """
    while True:
        clear_screen()
        print_banner()
        print(f"{Colors.HEADER}{Colors.BOLD}--- {tool['name']} Menu ---{Colors.ENDC}\n")
        
        commands = tool['commands']
        for i, command in enumerate(commands):
            print(f"  {Colors.BLUE}{i + 1:2}{Colors.ENDC}: {command['label']}")
        
        print(f"\n  {Colors.YELLOW} b{Colors.ENDC}: Back to Main Menu")

        choice = input(f"\n{Colors.CYAN}Choose an option: {Colors.ENDC}").strip().lower()

        if choice == 'b':
            break
        
        try:
            choice_index = int(choice) - 1
            if 0 <= choice_index < len(commands):
                handle_command_execution(commands[choice_index])
            else:
                print(f"{Colors.RED}Invalid choice. Please try again.{Colors.ENDC}")
                input("Press Enter to continue...")
        except ValueError:
            print(f"{Colors.RED}Invalid input. Please enter a number.{Colors.ENDC}")
            input("Press Enter to continue...")

def start_main_menu(tools: List[Dict[str, Any]]):
    """
    Starts the main interactive menu loop.

    Args:
        tools: The list of all loaded tool definitions.
    """
    while True:
        clear_screen()
        print_banner()
        print(f"{Colors.HEADER}{Colors.BOLD}--- Main Menu ---{Colors.ENDC}\n")
        
        for i, tool in enumerate(tools):
            print(f"  {Colors.BLUE}{i + 1:2}{Colors.ENDC}: {tool['name']}")

        print(f"\n  {Colors.YELLOW} q{Colors.ENDC}: Quit Arsenal")

        choice = input(f"\n{Colors.CYAN}Choose a tool to use: {Colors.ENDC}").strip().lower()
        
        if choice == 'q':
            raise KeyboardInterrupt # Cleanly exit the application

        try:
            choice_index = int(choice) - 1
            if 0 <= choice_index < len(tools):
                show_tool_submenu(tools[choice_index])
            else:
                print(f"{Colors.RED}Invalid choice. Please try again.{Colors.ENDC}")
                input("Press Enter to continue...")
        except ValueError:
            print(f"{Colors.RED}Invalid input. Please enter a number.{Colors.ENDC}")
            input("Press Enter to continue...")

