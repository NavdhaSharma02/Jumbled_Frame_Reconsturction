# Jumbled Frame Reconstruction

This project reconstructs a jumbled video back into its correct chronological order using structural similarity (SSIM) between frames.The algorithm identifies the natural temporal sequence by measuring how visually similar each frame is to others, then arranging them to form the most consistent sequence.

## Table of Contents
- Problem Statement
- Overview
- Algorithm Explanation
- Installation
- Usage
- Testing
- Example Output
- References

 ## Problem Statement
We are provided with a 5-second, 1080p, 60 FPS video whose frames have been randomly jumbled.The goal is to reconstruct the original video by restoring the correct frame order asaccurately and efficiently as possible.

## Overview
This project automatically reconstructs a jumbled video by sorting its shuffled frames into their correct order using pairwise pixel similarity.
It includes:
A Python script (main.py) for frame sorting
A Bash automation script (script.sh) to handle extraction, sorting and re-encoding end-to-end

## Installation

### **Requirements**
Bash Shell
Python 3.12 or later
ffmpeg installed and in PATH
pip package manager

### **Install Dependencies**
Install dependencies via the follwing command:-
pip install numpy pillow scipy

### **How to Run**

You can run it using the bash script by opening git bash or the vscode and using the following commands for:

- Making it executable: chmod +x run_sorting.sh
- Runnning it: ./run_sorting.sh -i input_video.mp4

## Algorithm 

The algorithm relies on a pixel-based similarity metric to reorder frames:

**Frame Preprocessing** :Each frame is converted to grayscale (reducing color noise).Resized so that the longest side = max_side (default 192 px) to speed up computation.Flattened into a 1D NumPy array of pixel intensities.

**Pairwise Distance Matrix** : A full N×N distance matrix is computed using Manhattan Distance (Sum of Absolute Differences) via scipy.spatial.distance.cdist. This measures how visually different each frame is from every other.

**Starting Frame Selection** :The algorithm locates the two frames that are most different (maximum distance).One of them becomes the starting point, since it’s likely at an “edge” of the sequence.

**Greedy Frame Linking** :Starting from the initial frame, the algorithm repeatedly finds the closest unused frame (lowest distance) to form a continuous “chain.”This heuristic works because consecutive frames in a real video are visually similar.

**Output**: The frames are reordered according to this chain and saved sequentially.

## Design Considerations
**Similarity Metric**:-	Manhattan Distance (Sum of Absolute Differences)	Efficient and robust for grayscale images.

**Approach**:-	Greedy nearest-neighbor chaining	Simple, deterministic, no ML training required.

**Time Complexity** :-	O(N²)	Due to full pairwise distance computation.

**Optimization**:-	Frame resizing via --max-side	Balances accuracy and speed.

**Robustness**:-	Works well for visually coherent frames (low motion noise)	May need feature-based matching for heavy motion.

## Testing and Evaluation

You can test on any short video clip:
 
./run_sorting.sh -i sample_jumbled.mp4

Verify results by comparing:
Original video vs. output.mp4
Visual smoothness and logical motion continuity

**Optional metrics:**
SSIM (Structural Similarity Index) between consecutive frames
Average frame distance reduction after sorting





  










