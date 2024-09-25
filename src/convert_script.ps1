param (
    [Parameter(Mandatory = $true)]
    [string]$sourceDir  # Directory containing .tif files
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

# Create a new directory for converted .jpm files
$outputDir = Join-Path (Split-Path $sourceDir -Parent) "$([System.IO.Path]::GetFileName($sourceDir))_jpm"
New-Item -Path $outputDir -ItemType Directory -Force | Out-Null

# Get all .tif files in the source directory
$tifFiles = Get-ChildItem -Path $sourceDir -Filter *.tif

if ($tifFiles.Count -eq 0) {
    Write-Host "No .tif files found in the directory."
    exit 1
}

# Convert each .tif file to .jpm
foreach ($file in $tifFiles) {
    $outputFile = Join-Path $outputDir ("$($file.BaseName).jpm")
    Write-Host "Converting $($file.FullName) to $outputFile"

    # Use ImageMagick (magick) to convert the file
    magick $file.FullName $outputFile

    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to convert $($file.FullName)."
    }
}

Write-Host "Conversion complete. Converted files are in $outputDir."
