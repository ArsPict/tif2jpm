import os
import subprocess
import logging
from pathlib import Path

# Set up logging for failed conversions
logging.basicConfig(
    filename='conversion_failures.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def convert_tif_to_jpm(src_dir, out_dir):
    # Ensure output directory exists
    Path(out_dir).mkdir(parents=True, exist_ok=True)

    # Walk through the source directory recursively
    for root, dirs, files in os.walk(src_dir):
        print(f"Converting {root}")

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

                # Skip if output file already exists
                if os.path.exists(output_file):
                    continue

                # Perform the conversion using ImageMagick's "magick" command
                try:
                    subprocess.run(["magick", input_file, output_file], check=True)
                    print(f"Converted: {input_file} -> {output_file}")
                except subprocess.CalledProcessError as e:
                    # Log failed conversions
                    logging.error(f"Failed to convert {input_file}: {e}")
                    print(f"Failed to convert {input_file}: {e}")
                except Exception as e:
                    # Catch other exceptions and log them
                    logging.error(f"Unexpected error with {input_file}: {e}")
                    print(f"Unexpected error with {input_file}: {e}")
        print(f"Finished converting {root}")


if __name__ == "__main__":
    src_directory = input("Enter source directory: ")
    output_directory = input("Enter output directory: ")

    convert_tif_to_jpm(src_directory, output_directory)

    # Print source and output directory structure for confirmation
    step = ""
    print("\nSource Directory Structure:")
    for root, dirs, files in os.walk(src_directory, topdown=True):
        print(step, root, dirs, files)
        step += "  "

    step = ""
    print("\nOutput Directory Structure:")
    for root, dirs, files in os.walk(output_directory, topdown=True):
        print(step, root, dirs, files)
        step += "  "
