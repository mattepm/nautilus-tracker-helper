# nautilus-tracker-helper
Nautilus extension in Python that adds a right click menu item that allows you stop/resume indexing the current folder in tracker-miner-fs-3.
Unfortunately, tracker-miner-fs-3 can get very resource eager. Navigating through terminal running gsettings to narrow down the set of directories to index can be time consuming, so this extension simply adds a Stop/Resume button on the right menu click of Nautilus to easily stop the indexing for that folder.

To keep in mind:
- Folders with many files and sub-directories are more resource eager
- You can see if a folder has indexing by showing hidden files with CTRL-H and verifying if there is a .trackerignore file
- Turning off indexing may be a bad idea on some folders that need it

# Important notes
Avoid managing manually the **.trackerignore** files. 
They don't have a real usage for ignoring the files since the extension uses ignore-directories from gsettings. 
They actually serve to refreshing Nautilus correctly in a creative way since there is no command to refresh it.

Remember that by tracker-miner design, if you blacklist a parent directory, all configurations in child directories are ignored. For example:
If you stop indexing /home/your_user/ the configurations set for Desktop, Documents, Downloads will be completely ignored.
So if you care about indexing Pictures, Downloads, Desktop files, etc. you shouldn't flag your home folder, but rather its subdirectories that you want to exclude.

# Install
Run the install script, or follow below manual steps:

## Pre-reqs:
Install python3-nautilus:
**sudo apt install python3-nautilus**

## Copy the script to the Python Nautilus extensions folder
**mkdir -p ~/.local/share/nautilus-python/extensions/**

**cp nautilus-tracker-extension.py ~/.local/share/nautilus-python/extensions/**

## Kill Nautilus
**nautilus -q**

Then re-open Nautilus via UI.