import os
import time
from json import load
from tkinter import Tk, Label
from tkinterdnd2 import DND_FILES, TkinterDnD
# hook-tkinterdnd2.py
from PyInstaller.utils.hooks import collect_data_files

datas = collect_data_files('tkinterdnd2')

target_key = input("please enter the json key you want to find:\n")

def process_file(file_path):
    # Add your code here to handle the file
    print(f"Processing file: {file_path}")
    if not file_path.__contains__(".json"):
        input("not a json please press any key to quit...")
        return
    try:
        with open(file_path, encoding='utf-8') as fp:
            data = load(fp)
        j_path = find_all_json_keys(data)
        os.system('cls')
        print('\n'.join(j_path))
        print("\n please review target json key path above...")
        while True:
            time.sleep(60)
    except Exception as e:
        print(e.__str__()+"\n")
        input("failed to process file press any key to quit...")

def drop(event):
    file_path = event.data
    event.widget.master.destroy()
    process_file(file_path)

def main():
    root = TkinterDnD.Tk()  # Use TkinterDnD.Tk instead of Tk
    root.title("Drag and Drop File")

    label = Label(root, text="Please drag your file here")
    label.pack(padx=70, pady=70)

    # Bind the drop event to the label
    label.drop_target_register(DND_FILES)
    label.dnd_bind('<<Drop>>', drop)

    root.mainloop()

def find_all_json_keys(data, parent_key=None, matches=None):
    if parent_key is None:
        parent_key = []
    if matches is None:
        matches = []

    if isinstance(data, dict):
        for key, value in data.items():
            new_parent_key = parent_key + [f"[\"{key}\"]"]
            if key == target_key:
                matches.append(''.join(new_parent_key))
            # Recurse into dictionaries
            if isinstance(value, dict):
                find_all_json_keys(value, new_parent_key, matches)
            # Check each item in lists
            elif isinstance(value, list):
                for index, item in enumerate(value):
                    find_all_json_keys(item, new_parent_key + [f"[{index}]"], matches)

    return matches


if __name__ == "__main__":
    main()