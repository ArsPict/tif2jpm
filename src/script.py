import os

from PIL import Image
import subprocess
import sys
import os

os.chdir(r'..\06_SV_50_27_ÜF')
# Open the TIFF file
tiff_file = "06_SV_50_27_ÜF_0001.tif"
image = Image.open(tiff_file)


# Convert the JP2 to JPM using OpenJPEG's opj_compress tool
jpm_file = tiff_file[:-4] + ".jpm"
print(jpm_file)
subprocess.run(["opj_compress", "-i", tiff_file, "-o", jpm_file])

print(f"Converted {tiff_file} to {jpm_file}")


