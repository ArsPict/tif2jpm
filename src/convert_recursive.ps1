param (
    [Parameter(Mandatory = $true)]
    [string]$sourceDir  # Root directory containing .tif files and subdirectories
)

# Check if ImageMagick is installed
if (-not (Get-Command "magick" -ErrorAction SilentlyContinue)) {
    Write-Host "ImageMagick is not installed or not in your PATH."
    exit 1
}

# Resolve full path of the source directory
$sourceDir = Resolve-Path $sourceDir

# Check if the source directory exists
if (-not (Test-Path $sourceDir)) {
    Write-Host "The specified directory does not exist."
    exit 1
}

# Function to convert .tif files in the given directory
function Convert-TiffToJpm {
    param (
        [string]$currentDir  # Current directory to process
    )

    # Create the equivalent directory structure for the output
    $outputDir = Join-Path (Split-Path $sourceDir -Parent) "$([System.IO.Path]::GetFileName($sourceDir))_jpm"
    $relativePath = $currentDir.Substring($sourceDir.Length)
    $newDir = Join-Path $outputDir $relativePath

    if (-not (Test-Path $newDir)) {
        New-Item -Path $newDir -ItemType Directory -Force | Out-Null
    }

    # Get all .tif files in the current directory
    $tifFiles = Get-ChildItem -Path $currentDir -Filter *.tif

    # Convert each .tif file to .jpm
    foreach ($file in $tifFiles) {
        $outputFile = Join-Path $newDir ("$($file.BaseName).jpm")
        Write-Host "Converting $($file.FullName) to $outputFile"

        # Use ImageMagick (magick) to convert the file
        magick $file.FullName $outputFile

        if ($LASTEXITCODE -ne 0) {
            Write-Host "Failed to convert $($file.FullName)."
        }
    }
}

# Process all directories (including subdirectories)
$allDirs = Get-ChildItem -Path $sourceDir -Recurse -Directory

# Convert files in the source directory itself
Convert-TiffToJpm -currentDir $sourceDir

# Recursively convert files in all subdirectories
foreach ($dir in $allDirs) {
    Convert-TiffToJpm -currentDir $dir.FullName
}

Write-Host "Conversion complete. Converted files are in $([System.IO.Path]::GetFileName($sourceDir))_jpm directory."
