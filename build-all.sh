#!/bin/bash
set -e

# Create output directory
OUT_DIR="public-dist"
rm -rf "$OUT_DIR"
mkdir -p "$OUT_DIR"

# Loop through all subdirectories in the current directory
for d in */; do
  # Remove trailing slash
  dir=${d%/}
  
  # Skip non-project directories
  if [ "$dir" == "public-dist" ] || [ "$dir" == "Users" ] || [ "$dir" == "node_modules" ] || [ "$dir" == "dist" ]; then
    continue
  fi
  
  # Check if it has a package.json (meaning it's a project)
  if [ -f "$dir/package.json" ]; then
    echo "------------------------------------------------"
    echo "Building $dir..."
    echo "------------------------------------------------"
    
    # Enter directory
    cd "$dir"
    
    # Ensure dependencies are installed (in case some were skipped)
    if [ ! -d "node_modules" ]; then
      npm install
    fi
    
    # Build with relative base path so it runs in a subfolder
    npx vite build --base "./"
    
    # Go back to root
    cd ..
    
    # Copy build files to output directory
    mkdir -p "$OUT_DIR/$dir"
    cp -r "$dir/dist/"* "$OUT_DIR/$dir/"
    
    echo "Built $dir successfully!"
  fi
done

# Create a clean index.html in public-dist that lists all 26 websites
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

for d in */; do
  dir=${d%/}
  if [ "$dir" == "public-dist" ] || [ "$dir" == "Users" ] || [ "$dir" == "node_modules" ] || [ "$dir" == "dist" ]; then
    continue
  fi
  if [ -f "$dir/package.json" ]; then
    # Format name for display
    display_name=$(echo "$dir" | sed 's/-/ /g')
    echo "        <a href=\"$dir/\" class=\"card\"><h3>🌿 $display_name</h3><p>Live interactive preview</p></a>" >> "$OUT_DIR/index.html"
  fi
done

cat <<EOT >> "$OUT_DIR/index.html"
    </div>
</body>
</html>
EOT

echo "All sites built and output generated in $OUT_DIR!"
