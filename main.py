import argparse
import shutil
from pathlib import Path
import numpy as np
from PIL import Image
from scipy.spatial.distance import cdist


def preprocess_frame(path: Path, max_side: int) -> np.ndarray:
    """Preprocess frame: grayscale + resize + flatten."""
    with Image.open(path) as img:
        img = img.convert("L")
        if max_side:
            scale = max_side / max(img.size)
            if scale < 1.0:
                new_size = tuple(max(1, int(round(dim * scale))) for dim in img.size)
                img = img.resize(new_size, Image.BILINEAR)
        return np.asarray(img, dtype=np.float32).ravel()


def sort_frames(frames: list[Path], max_side: int) -> list[int]:
    ##Sorting frames by building a "chain" based on pairwise pixel distance (Sum of Absolute Differences).
    print("Preprocessing frames...")
    data = np.stack([preprocess_frame(path, max_side) for path in frames])
    num_frames = len(frames)

    print("Calculating N-by-N pairwise distance matrix...")
    dist_matrix = cdist(data, data, 'cityblock')

    # Finding the two frames that are the most different( likely start and end points)
    i, j = np.unravel_index(np.argmax(dist_matrix), dist_matrix.shape)
    start_index = i
    print(f"Building chain, starting from frame {start_index} ({frames[start_index].name})...")

    sorted_indices = [start_index]
    used = {start_index}
    current_index = start_index

    while len(used) < num_frames:
        best_dist = np.inf
        best_neighbor = -1
        for neighbor in range(num_frames):
            if neighbor not in used:
                dist = dist_matrix[current_index, neighbor]
                if dist < best_dist:
                    best_dist = dist
                    best_neighbor = neighbor

        if best_neighbor != -1:
            current_index = best_neighbor
            sorted_indices.append(current_index)
            used.add(current_index)
        else:
            print("Error: Could not find next frame in chain.")
            break
            
    print("Reversing frame order to ensure correct sequence direction...")
    sorted_indices.reverse()

    return sorted_indices


def main() -> None:
    parser = argparse.ArgumentParser(description="Sort jumbled frames using pairwise pixel distance.")
    parser.add_argument("--input-dir", default="output_frames", help="Directory containing the source frames.")
    parser.add_argument("--glob", default="frame*.png", help="Glob pattern for frame files.")
    parser.add_argument("--output-dir", default="sorted_frames", help="Directory to place sorted frames.")
    parser.add_argument("--max-side", type=int, default=192, help="Resize longest side to this many pixels before distance computation.")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    frames = sorted(input_dir.glob(args.glob))
    if not frames:
        raise SystemExit(f"No frames matched {args.glob} under {input_dir}")

    order = sort_frames(frames, args.max_side)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    mapping_lines = []
    for idx, frame_idx in enumerate(order, start=1):
        src = frames[frame_idx]
        dst_name = f"frame_{idx:05d}{src.suffix}"
        dst = output_dir / dst_name
        shutil.copy2(src, dst)
        mapping_lines.append(f"{dst_name}\t{src.name}")

    (output_dir / "order.tsv").write_text("\n".join(mapping_lines) + "\n", encoding="utf-8")
    print(f"Sorted {len(frames)} frames into {output_dir}")


if __name__ == "__main__":
    main()
