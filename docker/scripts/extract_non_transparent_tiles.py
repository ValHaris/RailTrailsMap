#!/usr/bin/python3
import struct
from io import BytesIO
from PIL import Image
from pathlib import Path
import os
import argparse
from tqdm import tqdm


def parse_args():
    parser = argparse.ArgumentParser(description='Extract non-transparent tiles from a meta file')
    parser.add_argument('--file_path', type=Path, default=Path("/data/tiles/default/"), help='Path to the folder containing meta files')
    parser.add_argument('--outputdir', type=Path, default=Path("/data/extracted-tiles/"), help='Output directory to save the extracted tiles (without zoom folder)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Print debug information')
    parser.add_argument("--loop", action="store_true", help="Loop through the available zoom levels")
    return parser.parse_args()


HEADER_SIZE = 20
transparent_tiles = list()
non_transparent_tiles = list()
default_tile_extracted = False


def find_meta_files(folder):
    """Find all files with .meta extension in the given folder."""
    return list(folder.glob('**/*.meta'))


def is_transparent(image_data):
    image = Image.open(BytesIO(image_data))
    
    if image.mode == 'P':
        # Check if all pixels have the same color
        #
        # Different versions of PIL behave differently:
        # Some return a palette of 1 color, some return a palette of 256 colors
        palette = image.getpalette()
        if len(palette) == 3 or len(image.getcolors()) <= 1:
            return True
        
    elif image.mode == 'RGBA':
        alpha_channel = image.getchannel('A')
        if all(pixel == 0 for pixel in alpha_channel.getdata()):
            return True
    else:
        print(f"Unexpected image format {image.mode}")
    return False


def are_all_transparent(data, startx, starty, zoom, num_of_images, args):
    non_transparent_images = 0
    global default_tile_extracted

    for i in range(num_of_images):
        try:
            offset = HEADER_SIZE + i * 8
            x = startx + i // 8
            y = starty + i % 8
            imgoffset, size = struct.unpack('<II', data[offset:offset+8])
            
            if size:
                if not is_transparent(data[imgoffset:imgoffset+size]):
                    non_transparent_images += 1
                    non_transparent_tiles.append((x, y))
                    target_dir = args.outputdir / f"{zoom}/{x}"
                    target_file = target_dir / f"{y}.png"

                    save_image(data, i, target_file)
                else:
                    transparent_tiles.append((x, y))
                    if not default_tile_extracted:
                        save_image(data, i, args.outputdir / "transparent.png")
                        default_tile_extracted = True
                        
        except Exception as e:
            print(f"Error processing image {i}: {e}")


    return non_transparent_images == 0

def save_image(data, i, target_file):
    os.makedirs(target_file.parent, exist_ok=True)
    with open(target_file, 'wb') as f:
        offset = HEADER_SIZE + i * 8
        imgoffset, size = struct.unpack('<II', data[offset:offset+8])
        f.write(data[imgoffset:imgoffset+size])



def read_meta_tile(file_path, args):
    with open(file_path, 'rb') as f:
        data = f.read()
    
    magic, number, x, y, zoom = struct.unpack('<4sIIII', data[:HEADER_SIZE])
    
    if magic != b'META':
        raise ValueError("Invalid meta tile format")
    
    if args.verbose:
        print(f"{number} tiles, Zoom Level: {zoom} , X: {x}, Y: {y}")

    if are_all_transparent(data, x, y, zoom, number, args):    
        if args.verbose:
            print(f"All images are transparent")

    return zoom


def output_next_zoom_tile_list(outputfile, zoom):
    with open(outputfile, 'w') as f:
        for x, y in non_transparent_tiles:
            f.write(f"{2*x} {2*y} {zoom+1}\n")
            f.write(f"{2*x+1} {2*y} {zoom+1}\n")
            f.write(f"{2*x} {2*y+1} {zoom+1}\n")
            f.write(f"{2*x+1} {2*y+1} {zoom+1}\n")

def run(args):
    meta_files = find_meta_files(args.file_path)
    if args.verbose:
        print(f"Found meta files: {len(meta_files)}")
    if len(meta_files) == 0:
        raise Exception(f"No meta files found in {args.file_path}")
    for meta_file in tqdm(meta_files, desc="Scanning meta tiles"):
        zoom = read_meta_tile(meta_file, args)
    output_next_zoom_tile_list(args.file_path / "next_level_tiles.txt", zoom)
    print(f"Number of transparent tiles: {len(transparent_tiles)}, non-transparent tiles: {len(non_transparent_tiles)}")


if __name__ == "__main__":
    cmd_args = parse_args()
    if cmd_args.loop:
        file_path = cmd_args.file_path
        for zoom in file_path.glob("*"):
            if os.path.isdir(zoom):
                cmd_args.file_path = zoom
                run(cmd_args)
    else:
        run(cmd_args)
