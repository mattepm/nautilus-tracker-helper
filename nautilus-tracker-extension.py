from gi.repository import Nautilus, GObject
from typing import List
import os
import subprocess

class StopIndexingExtension(GObject.GObject, Nautilus.MenuProvider):
    def __init__(self):
        super().__init__()
        print("Initialized Stop Indexing extension")

    def menu_activate_cb(self, menu: Nautilus.MenuItem, current_folder: Nautilus.FileInfo) -> None:
        print("Stop indexing action activated in folder:", current_folder.get_name())
        
        # Get the current folder path
        current_folder_path = current_folder.get_location().get_path()

        # Get the current ignored directories
        current_dirs = subprocess.check_output(
            ["gsettings", "get", "org.freedesktop.Tracker3.Miner.Files", "ignored-directories"],
            text=True
        ).strip()
        
        # Remove brackets and split paths
        current_dirs = current_dirs.strip("[]").split(", ")

        # Check if the current folder is already in the ignored directories
        if current_folder_path in current_dirs:
            print(f"'{current_folder_path}' is already in ignored directories.")
            return  # Exit if the folder is already ignored

        # Add the current folder path to the ignored directories
        current_dirs.append(f"'{current_folder_path}'")
        
        # Remove duplicates by converting to a set and back to list
        unique_dirs = list(set(current_dirs))

        # Create the new ignored directories string
        new_dirs = f"[{', '.join(unique_dirs)}]"

        # Set the new ignored directories
        subprocess.run(["gsettings", "set", "org.freedesktop.Tracker3.Miner.Files", "ignored-directories", new_dirs])
        
        print(f"Added '{current_folder_path}' to ignored directories.")

        # Refresh the menu to update the action
        loading_path = os.path.join(current_folder.get_location().get_path(), '.trackerignore')
        with open(loading_path, 'w') as f:
            f.write("")

    def resume_indexing_cb(self, menu: Nautilus.MenuItem, current_folder: Nautilus.FileInfo) -> None:
        print("Resume indexing action activated in folder:", current_folder.get_name())
        
        # Get the current folder path
        current_folder_path = current_folder.get_location().get_path()

        # Get the current ignored directories
        current_dirs = subprocess.check_output(
            ["gsettings", "get", "org.freedesktop.Tracker3.Miner.Files", "ignored-directories"],
            text=True
        ).strip()
        
        # Remove brackets and split paths
        current_dirs = current_dirs.strip("[]").split(", ")

        # Remove the current folder path from the ignored directories
        current_dirs = [d for d in current_dirs if d.strip("'") != current_folder_path]

        # Create the new ignored directories string
        new_dirs = f"[{', '.join(current_dirs)}]"

        # Set the new ignored directories
        subprocess.run(["gsettings", "set", "org.freedesktop.Tracker3.Miner.Files", "ignored-directories", new_dirs])
        
        print(f"Removed '{current_folder_path}' from ignored directories.")    
        
        # Refresh the menu to update the action
        loading_path = os.path.join(current_folder.get_location().get_path(), '.trackerignore')
        if os.path.isfile(loading_path):
            os.remove(loading_path)


    def get_background_items(self, current_folder: Nautilus.FileInfo) -> List[Nautilus.MenuItem]:
        # Get the current folder path
        current_folder_path = current_folder.get_location().get_path()
        
        # Get the current ignored directories
        current_dirs = subprocess.check_output(
            ["gsettings", "get", "org.freedesktop.Tracker3.Miner.Files", "ignored-directories"],
            text=True
        ).strip()
        
        # Remove brackets and split paths
        current_dirs = current_dirs.strip("[]").split(", ")

        # Check if the current folder is already ignored
        if f"'{current_folder_path}'" in current_dirs:
            resume_item = Nautilus.MenuItem(
                name="StopIndexingExtension::Resume_Indexing",
                label="Resume indexing",
                tip="Resume indexing this folder",
            )
            resume_item.connect("activate", self.resume_indexing_cb, current_folder)
            return [resume_item]  # Return resume item if already ignored
        else:
            item = Nautilus.MenuItem(
                name="StopIndexingExtension::Stop_Indexing",
                label="Stop indexing",
                tip="Stop indexing this folder",
            )
            item.connect("activate", self.menu_activate_cb, current_folder)
            return [item]  # Return the item to display in the background menu

        return []  # No items to display if neither option applies