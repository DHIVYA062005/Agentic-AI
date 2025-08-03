import cv2
import numpy as np
import pandas as pd
import os

width, height = 640, 480
fps = 10
duration_seconds = 15
frame_count = fps * duration_seconds

workers = {
    1: {"pos": [100, 100], "velocity": [2, 1], "color": (0, 255, 0), "status": "working"},
    2: {"pos": [300, 150], "velocity": [0, 0], "color": (0, 0, 255), "status": "idle"},
    3: {"pos": [200, 300], "velocity": [1, -1], "color": (255, 0, 0), "status": "working"},
    4: {"pos": [500, 400], "velocity": [0, 0], "color": (0, 255, 255), "status": "idle"},
    5: {"pos": [50, 400], "velocity": [2, -2], "color": (255, 0, 255), "status": "working"},
}

output_dir = "output"
os.makedirs(output_dir, exist_ok=True)
video_path = os.path.join(output_dir, "simulated_cctv_long.mp4")
csv_path = os.path.join(output_dir, "simulated_log_long.csv")

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(video_path, fourcc, fps, (width, height))

log_data = []

for frame_num in range(frame_count):
    frame = np.ones((height, width, 3), dtype=np.uint8) * 255

    for worker_id, info in workers.items():
        x, y = info["pos"]
        vx, vy = info["velocity"]

        cv2.circle(frame, (int(x), int(y)), 20, info["color"], -1)
        cv2.putText(frame, f"ID:{worker_id}", (int(x)-20, int(y)-25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
        cv2.putText(frame, info["status"], (int(x)-20, int(y)+35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)

        log_data.append([frame_num, worker_id, x, y, info["status"]])

        if info["status"] == "working":
            info["pos"][0] += vx
            info["pos"][1] += vy
            if not (0 < info["pos"][0] < width): info["velocity"][0] *= -1
            if not (0 < info["pos"][1] < height): info["velocity"][1] *= -1

    out.write(frame)

out.release()
df = pd.DataFrame(log_data, columns=["frame", "worker_id", "x", "y", "status"])
df.to_csv("simulated_log.csv", index=False)  # Important: Output same as used by Streamlit
print("Simulation complete. Files saved.")
