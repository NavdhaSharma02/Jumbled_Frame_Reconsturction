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

##  Overview
Let's first see what are the different ways this task could be done
### Pixel Difference (Fastest, Simple) :
The main idea of pixel difference is that instead of storing every full frame,you store only how each frame differs from the previous one ( pixel-wise changes).Then, reconstruction simply means adding those differences back over time to rebuild the original frames.
### Feature Matching (Classic CV):
While pixel difference compares raw intensity values between consecutive frames, feature matching compares key points or distinctive features (like edges, corners, textures) that represent objects or structures in the scene.
### Deep Embeddings (Modern & Accurate):
Instead of comparing frame by frame we embed these frames via pretrained CNN (ResNet, CLIP, ViT) then sort frames using cosine similarity.
### Optical Flow or motion estimation
Estimate direction of motion between frames (how objects move). Then reorder based on forward flow continuity.

## Why SSIM?

The SSIM (Structural Similarity Index Metric) is a perceptual metric that measures image quality degradation based on structural information, luminance, and contrast.  
In this project, SSIM is applied to each corresponding frame pair from two videos to determine how visually similar they are.

Unlike simple pixel-wise metrics such as MSE or PSNR, SSIM correlates better with human visual perception.It compares images based on structure, brightness and contrast resulting in more meaningful quality assessment.In this project SSIM based approach proved to be more accruate because:
- Video has little Camera Change
- Feature Detectors (ORB, SIFT, etc.) don’t Work Well on Smooth or Repetitive Scenes and in the video given here, there are almost similar background and very few unstable keypoints.
- Deep networks like ResNet or CLIP focus on semantic meaning what’s in the image, not how slightly it changed.Two consecutive frames of a person waving look identical to a CNN, because both contain “a person.”
- Optical Flow May Fail if Motion Is Minimal


##  Algorithm Explanation

### **Techniques Used**
- Structural Similarity Index (SSIM) from `skimage.metrics`
- Frame-by-frame comparison using OpenCV
- Average SSIM score computed across all frames

### **Working Steps**
1. Read both reference and test videos using OpenCV.  
2. Ensure both videos have the same frame size and number of frames.  
3. Convert each frame to grayscale.  
4. Compute SSIM between corresponding frames.  
5. Store per-frame SSIM and calculate the overall average.



## Installation











