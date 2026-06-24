# Command Hook: /update-socials
description: Run the python script to sync footer social media links across all directories.

When this slash command is triggered:
1. Run `python3 update-socials.py`.
2. Parse the script output to verify if any business pages were NOT found or flagged with warnings.
3. Print a clean, compiled table listing each business folder, Facebook status, Instagram status, and notes.
