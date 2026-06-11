#!/bin/bash
set -e

# Create output directory
OUT_DIR="public-dist"
rm -rf "$OUT_DIR"
mkdir -p "$OUT_DIR"

# Find all subdirectories containing package.json (excluding node_modules and public-dist)
find . -name "package.json" | while read -r pkg_file; do
  # Skip node_modules or public-dist
  if [[ "$pkg_file" == *"/node_modules/"* ]] || [[ "$pkg_file" == *"/public-dist/"* ]]; then
    continue
  fi
  
  # Get the project directory path
  proj_path=$(dirname "$pkg_file")
  # Strip leading ./
  proj_path=${proj_path#./}
  
  # Get just the project folder name (e.g. bkk-plumbing)
  proj_name=$(basename "$proj_path")
  
  echo "------------------------------------------------"
  echo "Building $proj_name ($proj_path)..."
  echo "------------------------------------------------"
  
  # Enter directory
  cd "$proj_path"
  
  # Ensure dependencies are installed
  if [ ! -d "node_modules" ]; then
    npm install
  fi
  
  # Build with relative base path so it runs in a subfolder
  npx vite build --base "./"
  
  # Go back to root
  cd - > /dev/null
  
  # Copy build files to output directory under flat folder name
  mkdir -p "$OUT_DIR/$proj_name"
  cp -r "$proj_path/dist/"* "$OUT_DIR/$proj_name/"
  
  echo "Built $proj_name successfully!"
done

# Create a clean index.html in public-dist that lists all websites
cat <<EOT > "$OUT_DIR/index.html"
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CQ Local Business Websites - Live Previews</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Outfit', sans-serif;
            background: #121212;
            color: #ffffff;
            margin: 0;
            padding: 4rem 2rem;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            font-weight: 800;
            background: linear-gradient(45deg, #F57F17, #8FBC8F);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        p {
            color: #aaa;
            margin-bottom: 3rem;
            text-align: center;
            max-width: 600px;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 1.5rem;
            max-width: 1200px;
            width: 100%;
        }
        .card {
            background: #1e1e1e;
            border: 1px solid #333;
            border-radius: 8px;
            padding: 1.5rem;
            transition: all 0.3s ease;
            text-decoration: none;
            color: inherit;
        }
        .card:hover {
            transform: translateY(-5px);
            border-color: #F57F17;
            box-shadow: 0 10px 20px rgba(0,0,0,0.3);
        }
        .card h3 {
            margin: 0 0 0.5rem 0;
            font-size: 1.25rem;
        }
        .card p {
            margin: 0;
            color: #888;
            font-size: 0.9rem;
            text-align: left;
        }
    </style>
</head>
<body>
    <h1>CQ Local Business Websites</h1>
    <p>Live preview directory of premium website mockups for local Central Queensland business outreach campaigns.</p>
    <div class="grid">
EOT

# Populate index link items recursively
find . -name "package.json" | while read -r pkg_file; do
  if [[ "$pkg_file" == *"/node_modules/"* ]] || [[ "$pkg_file" == *"/public-dist/"* ]]; then
    continue
  fi
  proj_path=$(dirname "$pkg_file")
  proj_path=${proj_path#./}
  proj_name=$(basename "$proj_path")
  display_name=$(echo "$proj_name" | sed 's/-/ /g')
  echo "        <a href=\"$proj_name/\" class=\"card\"><h3>🌿 $display_name</h3><p>Live interactive preview</p></a>" >> "$OUT_DIR/index.html"
done

cat <<EOT >> "$OUT_DIR/index.html"
    </div>
</body>
</html>
EOT

echo "All sites built recursively and output generated in $OUT_DIR!"
