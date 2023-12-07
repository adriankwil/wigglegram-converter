#!/bin/zsh

if [ $# -eq 0 ]; then
    echo "Usage: $0 <source image> <dest path (optional)>"
    exit 1
fi

input_image="$1"

if [ $# -eq 2 ]; then
  output_directory=$2
else;
  output_directory=$(dirname "$1")
fi

output_image=$(basename "$1")


# Check if ImageMagick is installed
command -v convert >/dev/null 2>&1 || { echo >&2 "ImageMagick is required but not installed. Aborting."; exit 1; }

# Input image file (replace with your actual file path)

# Output directory and filenames
# output_directory="/Users/adrianwi/Pictures/WiggleGrams copy/out"
output_prefix="$output_image"
gif_output="$output_image.webp"

# Create output directory if it doesn't exist
mkdir -p "$output_directory"

# Split the image vertically into three parts
convert "$input_image" -crop 3x1@ +repage +adjoin -resize 1024x "${output_directory}/${output_prefix}_%02d.png"
cp "${output_directory}/${output_prefix}_01.png" "${output_directory}/${output_prefix}_03.png"

# align the images using opencv
python align.py $output_prefix $output_directory
# Combine the three images into a GIF with a faster speed and width of 512 pixels
convert -delay 1 -loop 1 "${output_directory}/${output_prefix}_aligned_image_0_to_1.png" "${output_directory}/${output_prefix}_01.png" "${output_directory}/${output_prefix}_aligned_image_2_to_1.png" "${output_directory}/${output_prefix}_03.png" "$output_directory/gifs/$gif_output"


# Combine the three images into a GIF with a faster speed and width of 512 pixels
# convert -delay 1 -loop 0 "${output_directory}/${output_prefix}_00.png" "${output_directory}/${output_prefix}_01.png" "${output_directory}/${output_prefix}_02.png" "${output_directory}/${output_prefix}_03.png" "$output_directory/gifs/$gif_output"

rm "${output_directory}/${output_prefix}_00.png"
rm "${output_directory}/${output_prefix}_aligned_image_0_to_1.png"
rm "${output_directory}/${output_prefix}_01.png"
rm "${output_directory}/${output_prefix}_aligned_image_2_to_1.png"
rm "${output_directory}/${output_prefix}_02.png"
rm "${output_directory}/${output_prefix}_03.png"
