# Comparing pixels of two images and highlighting differences
import cv2, os, numpy as np
from skimage.metrics import structural_similarity as ssim
import cv2
import os

# FRAME EXTRACTION
def extract_frames(video_path, output_folder="frames", resize_to=None):
    """
    Extracts all frames from a video and saves them as JPG images.

    Parameters:
        video_path (str): Path to input video file (e.g., 'jumbled_video.mp4')
        output_folder (str): Folder to store extracted frames (default: 'frames')
        resize_to (tuple): Optional (width, height) to resize frames
    """
    os.makedirs(output_folder, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"❌ Cannot open video file: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"🎞 FPS: {fps:.2f}, Total Frames: {total}")

    count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if resize_to is not None:
            frame = cv2.resize(frame, resize_to)

        frame_path = os.path.join(output_folder, f"frame_{count:04d}.jpg")
        cv2.imwrite(frame_path, frame)
        count += 1

    cap.release()
    print(f"✅ Extracted {count} frames to '{output_folder}'")

if __name__ == "__main__":
    # Example usage
    video_file = "jumbled_video.mp4"
    output_dir = "frames"
    extract_frames(video_file, output_dir)

# RECONSTRUCTION BASED ON PIXEL SIMILARITY
cap = cv2.VideoCapture("jumbled_video.mp4")
frames=[]; 
while True:
    ok,f=cap.read()
    if not ok: break
    frames.append(cv2.resize(f,(224,224)))
cap.release()

def frame_diff(a,b):
    return ssim(cv2.cvtColor(a,cv2.COLOR_BGR2GRAY),
                cv2.cvtColor(b,cv2.COLOR_BGR2GRAY))

n=len(frames)
sim=np.zeros((n,n))
for i in range(n):
    for j in range(n):
        if i!=j: sim[i,j]=frame_diff(frames[i],frames[j])

order=[np.argmax(sim.sum(1))]
used=np.zeros(n,bool); used[order[0]]=True
for _ in range(n-1):
    nxt=np.argmax(sim[order[-1]]*(~used))
    order.append(nxt); used[nxt]=True

h,w,_=frames[0].shape
out=cv2.VideoWriter("recon_pixel.avi",cv2.VideoWriter_fourcc(*'XVID'),30,(w,h))
for i in order: out.write(frames[i])
out.release()
