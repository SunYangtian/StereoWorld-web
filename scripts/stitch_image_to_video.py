#!/usr/bin/env python3
"""
将 materials/stereovideo 下的 PNG 图像处理后拼接到对应视频左侧：
  1. 若 PNG 含 Alpha 通道（RGBA），先填充白色背景
  2. 等比 resize，使高度与视频一致
  3. Pad 到固定宽度（视频宽度的 1/4），居中，白色填充
  4. 拼接到视频左侧，输出至 materials/stereovideo/stitched/

依赖：ffmpeg（需系统已安装）
"""

import subprocess
import json
from pathlib import Path

INPUT_DIR = Path(__file__).parent.parent / "materials" / "stereovideo"
OUTPUT_DIR = INPUT_DIR / "stitched"


def get_video_info(video_path: Path) -> dict:
    """使用 ffprobe 获取视频宽高和帧率。"""
    cmd = [
        "ffprobe", "-v", "quiet",
        "-print_format", "json",
        "-show_streams",
        str(video_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    info = json.loads(result.stdout)
    for stream in info["streams"]:
        if stream.get("codec_type") == "video":
            return {
                "width": int(stream["width"]),
                "height": int(stream["height"]),
                "r_frame_rate": stream.get("r_frame_rate", "30/1"),
                "duration": float(stream.get("duration", stream.get("tags", {}).get("DURATION", "0").replace(":", "").replace(".", "") or "0")),
            }
    raise RuntimeError(f"未找到视频流: {video_path}")


def stitch(image_path: Path, video_path: Path, output_path: Path):
    """将 PNG 处理后拼接到视频左侧。"""
    info = get_video_info(video_path)
    vw = info["width"]
    vh = info["height"]
    fps = info["r_frame_rate"]

    # 目标图片列宽 = 视频宽度的 1/4（保证为偶数）
    target_w = (vw // 4) // 2 * 2

    # 计算精确时长（秒）：取帧数 / fps，避免浮点误差
    num, den = map(int, fps.split("/"))
    fps_float = num / den

    # 用 ffprobe 取精确帧数以确定时长
    probe = subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "stream=nb_frames",
         "-select_streams", "v:0", "-of", "csv=p=0", str(video_path)],
        capture_output=True, text=True, check=True,
    )
    nb_frames_str = probe.stdout.strip()
    if nb_frames_str.isdigit():
        duration = int(nb_frames_str) / fps_float
    else:
        duration = float(info["duration"]) if info["duration"] else 10.0

    # filtergraph 说明：
    # 1. [0:v] scale：高度缩放至 vh，宽度等比（-2 保证偶数）
    # 2. color=white 生成 target_w x vh 的白色背景
    # 3. overlay 将缩放后图像居中叠加到白色背景
    #    —— overlay 自动处理 RGBA alpha 通道（合成到白色），RGB 图像则直接覆盖
    # 4. [img][1:v] hstack 横向拼接
    filter_complex = (
        f"[0:v]scale=-2:{vh}[scaled];"
        f"color=white:size={target_w}x{vh}:rate={fps}[bg];"
        f"[bg][scaled]overlay=main_w/2-overlay_w/2:main_h/2-overlay_h/2[img];"
        f"[img][1:v]hstack=inputs=2[out]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-framerate", fps,                        # 图片输入帧率与视频一致
        "-loop", "1", "-i", str(image_path),      # 输入 0：静态图（loop）
        "-i", str(video_path),                    # 输入 1：原始视频
        "-filter_complex", filter_complex,
        "-map", "[out]",
        "-map", "1:a?",                           # 保留音频（若有）
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-c:a", "copy",
        "-t", str(duration),                      # 明确限制输出时长
        "-r", fps,
        str(output_path),
    ]

    print(f"处理: {image_path.name} + {video_path.name} -> {output_path.name}")
    print(f"  视频尺寸: {vw}x{vh}  图片列宽: {target_w}  时长: {duration:.2f}s @ {fps}fps")
    subprocess.run(cmd, check=True)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 找到所有配对的 png+mp4
    png_files = sorted(INPUT_DIR.glob("*.png"))
    if not png_files:
        print("未找到 PNG 文件，退出。")
        return

    for png in png_files:
        video = png.with_suffix(".mp4")
        if not video.exists():
            print(f"  [跳过] 未找到对应视频: {video.name}")
            continue

        output = OUTPUT_DIR / f"{png.stem}_stitched.mp4"
        try:
            stitch(png, video, output)
            print(f"  -> 已保存: {output.relative_to(INPUT_DIR.parent.parent)}")
        except subprocess.CalledProcessError as e:
            print(f"  [错误] 处理 {png.name} 时失败: {e}")

    print("\n全部完成！")


if __name__ == "__main__":
    main()
