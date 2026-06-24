# Command Hook: /build-all
description: Execute build-all.sh to verify compiling of all websites.

When this slash command is triggered:
1. Run `./build-all.sh` inside the workspace root.
2. Monitor build progress and log if any website directory fails to copy or package.
3. Check the output directory `public-dist/` to confirm that all 26 website builds exist.
4. Output a summary of the distribution files created.
