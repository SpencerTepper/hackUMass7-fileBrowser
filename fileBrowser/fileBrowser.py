import os
import sys
import termios
import tty
from FileList import FileList

# ANSI escape codes for terminal control
CLEAR_SCREEN = "\033[2J"
RESET_CURSOR = "\033[H"
HIGHLIGHT = "\033[7m"
RESET = "\033[0m"

# Function to read a single character input
def getInput():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

# Function to display files in a TUI
def display_files(current_path, fileList, selected_index):
    sys.stdout.write(CLEAR_SCREEN + RESET_CURSOR)
    print(f"Current Path: {current_path}")

    for i, entry in enumerate(fileList):
        label = entry['label'] if isinstance(entry, dict) else f"{'Dir ' if entry.is_dir() else 'File'} {entry.name}"
        if i == selected_index:
            sys.stdout.write(f"{HIGHLIGHT}> {label}{RESET}\n")
        else:
            sys.stdout.write(f"  {label}\n")

    sys.stdout.flush()

# Main TUI function
def tui_file_browser():
    current_path = os.getcwd()
    selected_index = 0

    while True:
        fileListOBJ = FileList(current_path)
        entries = fileListOBJ.getEntryList()
        
        # Add custom dict entry for '..' for parent directory navigation
        fileList = [{'name': '..', 'label': 'Dir  .. (Go up)'}] + entries

        display_files(current_path, fileList, selected_index)

        key = getInput()

        # Handle arrow keys
        if key == '\x1b':  # ESC sequence for arrow keys
            getInput()  # Skip '['
            arrow_key = getInput()
            if arrow_key == 'A':  # Up arrow
                selected_index = max(0, selected_index - 1)
            elif arrow_key == 'B':  # Down arrow
                selected_index = min(len(fileList) - 1, selected_index + 1)

        # Enter key to open directory or file
        elif key == '\r':
            selected_entry = fileList[selected_index]

            if isinstance(selected_entry, dict) and selected_entry['name'] == "..":
                # Navigate to the parent directory
                current_path = os.path.dirname(current_path)
                selected_index = 0
            elif selected_entry.is_dir():
                # Navigate into the selected directory
                current_path = os.path.join(current_path, selected_entry.name)
                selected_index = 0
            else:
                sys.stdout.write(CLEAR_SCREEN + RESET_CURSOR)
                print(f"Selected File: {os.path.join(current_path, selected_entry.name)}")
                break

        # Quit the TUI with 'q'
        elif key == 'q':
            sys.stdout.write(CLEAR_SCREEN + RESET_CURSOR)
            # help user cd to the path they are at in the fileBrowser
            print("to go to the target path, run this")
            print(f"cd {current_path}")
            break

if __name__ == "__main__":
    tui_file_browser()

