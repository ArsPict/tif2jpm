import os
import subprocess
from pathlib import Path


def convert_tif_to_jpm(src_dir, out_dir):
    # Ensure output directory exists
    Path(out_dir).mkdir(parents=True, exist_ok=True)

    # Walk through the source directory recursively
    for root, dirs, files in os.walk(src_dir):
        # Determine the relative path from the source directory
        relative_path = os.path.relpath(root, src_dir)

        # Create the corresponding directory in the output directory
        output_path = os.path.join(out_dir, relative_path)
        Path(output_path).mkdir(parents=True, exist_ok=True)

        # Loop through files in the current directory
        for file in files:
            # Check if the file is a .tif file
            if file.lower().endswith(".tif"):
                # Define full paths for input and output files
                input_file = os.path.join(root, file)
                output_file = os.path.join(output_path, os.path.splitext(file)[0] + ".jpm")

                # Perform the conversion using ImageMagick's "magick" command
                try:
                    subprocess.run(["magick", input_file, output_file], check=True)
                    print(f"Converted: {input_file} -> {output_file}")
                except subprocess.CalledProcessError as e:
                    print(f"Failed to convert {input_file}: {e}")


if __name__ == "__main__":
    src_directory = r"C:\Users\Arsenii\Desktop\Biesdorf_1892_1893_S_tif"  # Replace with your source directory
    output_directory = r"C:\Users\Arsenii\Desktop\Biesdorf_1892_1893_S_jpm" # Replace with your output directory
    src_directory = input()
    output_directory = input()
    convert_tif_to_jpm(src_directory, output_directory)
