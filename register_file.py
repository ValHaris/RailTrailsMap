import glob
import argparse
import os
from pathlib import Path
import sys
import re

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find and register a downloaded Planet file")
    parser.add_argument("--folder", type=Path, required=True, help="Download folder")
    parser.add_argument("--news", required=True, help="html news file")
    args = parser.parse_args()

    files = glob.glob(f"{args.folder}/planet-*.osm.pbf")
    if not files:
        sys.exit("No planet files found")
    newest = next(iter(sorted(files, reverse=True)))

    newest_date = re.search(r"planet-(\d{2})(\d{2})(\d{2})\.osm\.pbf", newest)
    if not newest_date:
        sys.exit("No valid planet file found")

    target_file = args.folder / "planet.osm.pbf"
    if os.path.exists(target_file):
        os.remove(target_file)
    os.link(newest, target_file)

    with open(args.news, "r") as f:
        news_content = f.read()
    
    with open(args.news, "w") as f:
        f.write( re.sub( r'<span class="date">\d{4}-\d{2}-\d{2}</span>', f'<span class="date">20{newest_date.group(1)}-{newest_date.group(2)}-{newest_date.group(3)}</span>', news_content))


