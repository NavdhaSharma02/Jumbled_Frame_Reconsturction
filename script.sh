#!/usr/bin/env bash
set -euo pipefail

# Simple driver to extract frames, run main.py and re-encode sorted frames.
# Now includes total execution time measurement.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

print_usage() {
  cat <<EOF
Usage: $(basename "$0") -i INPUT_VIDEO [-f FPS] [-t TEMP_FRAMES_DIR] [-s SORTED_DIR] [-o OUTPUT_VIDEO]
Defaults: FPS=30, TEMP_FRAMES_DIR=image_frames, SORTED_DIR=sorted_frames, OUTPUT_VIDEO=output.mp4
EOF
}

# Defaults
FPS=30
FRAMES_DIR="image_frames"
SORTED_DIR="sorted_frames"
OUTPUT_VIDEO="output.mp4"

# Record start time
START_TIME=$(date +%s)

# Parsing Arguments
while getopts "i:f:t:s:o:h" opt; do
  case $opt in
    i) INPUT_VIDEO="$OPTARG" ;;
    f) FPS="$OPTARG" ;;
    t) FRAMES_DIR="$OPTARG" ;;
    s) SORTED_DIR="$OPTARG" ;;
    o) OUTPUT_VIDEO="$OPTARG" ;;
    h) print_usage; exit 0 ;;
    *) print_usage; exit 1 ;;
  esac
done

if [ -z "${INPUT_VIDEO-}" ]; then
  echo "Error: input video is required."
  print_usage
  exit 1
fi

# Checking dependencies
command -v ffmpeg >/dev/null 2>&1 || { echo "ffmpeg not found"; exit 1; }
command -v python >/dev/null 2>&1 || { echo "python not found"; exit 1; }

# Frame directories
mkdir -p "$FRAMES_DIR"
rm -f "$FRAMES_DIR"/frame_*.png
mkdir -p "$SORTED_DIR"
rm -f "$SORTED_DIR"/frame_*.png

echo "--------------------------------------------"
echo "Extracting frames from '$INPUT_VIDEO' at ${FPS} fps -> ${FRAMES_DIR}/frame_%05d.png"
echo "--------------------------------------------"
ffmpeg -y -i "$INPUT_VIDEO" -vf "fps=${FPS}" "${FRAMES_DIR}/frame_%05d.png"

echo "--------------------------------------------"
echo "Running main.py (frame sorting)"
echo "--------------------------------------------"
python "$SCRIPT_DIR/main.py" --input-dir "$FRAMES_DIR" --output-dir "$SORTED_DIR" --max-side 192

echo "--------------------------------------------"
echo "Re-encoding sorted frames into '$OUTPUT_VIDEO' at ${FPS} fps"
echo "--------------------------------------------"
ffmpeg -y -framerate "$FPS" -i "${SORTED_DIR}/frame_%05d.png" -c:v libx264 -pix_fmt yuv420p "$OUTPUT_VIDEO"


END_TIME=$(date +%s)
ELAPSED=$((END_TIME - START_TIME))
MINUTES=$((ELAPSED / 60))
SECONDS=$((ELAPSED % 60))

echo "--------------------------------------------"
echo "Done. Output video: $OUTPUT_VIDEO"
echo "Frame mapping file: ${SORTED_DIR}/order.tsv"
echo "Total Execution Time: ${MINUTES}m ${SECONDS}s"
echo "--------------------------------------------"
