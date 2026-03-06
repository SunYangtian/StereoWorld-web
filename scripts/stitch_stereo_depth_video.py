#!/usr/bin/env python3
"""
将 stereo video 与 depth video 左右拼接（hstack）。

支持的目录：
  materials/stereodepthvideo  —— stereo_video{N}.mp4  +  disp_vis{N}.mp4
  materials/eba_video         —— left_stereo{N}.mp4   +  depth_vis{N}.mp4

用法：
  python3 scripts/stitch_stereo_depth_video.py                   # 处理两个目录
  python3 scripts/stitch_stereo_depth_video.py stereodepthvideo  # 只处理指定目录
  python3 scripts/stitch_stereo_depth_video.py eba_video

依赖：ffmpeg（系统已安装）
"""

import re
import subprocess
import sys
from pathlib import Path

# 项目根目录
ROOT = Path(__file__).parent.parent
MATERIALS = ROOT / "materials"

# 每个目录的文件命名规则
# key: 目录名  value: (stereo_glob_prefix, depth_glob_prefix)
DIR_PATTERNS: dict[str, tuple[str, str]] = {
    "stereodepthvideo": ("stereo_video", "disp_vis"),
    "eba_video":        ("left_stereo",  "depth_vis"),
}


# ──────────────────────────────────────────────
# 工具函数
# ──────────────────────────────────────────────

def get_video_info(path: Path) -> dict:
    """用 ffprobe 取视频宽、高、帧率、精确帧数。"""
    import json
    cmd = [
        "ffprobe", "-v", "quiet",
        "-print_format", "json",
        "-show_streams",
        str(path),
    ]
    info = json.loads(subprocess.run(cmd, capture_output=True, text=True, check=True).stdout)
    for s in info["streams"]:
        if s.get("codec_type") == "video":
            return {
                "width":  int(s["width"]),
                "height": int(s["height"]),
                "fps":    s.get("r_frame_rate", "30/1"),
            }
    raise RuntimeError(f"未找到视频流: {path}")


def get_nb_frames(path: Path, fps_str: str) -> float:
    """返回视频精确时长（秒）。"""
    probe = subprocess.run(
        ["ffprobe", "-v", "quiet",
         "-show_entries", "stream=nb_frames",
         "-select_streams", "v:0",
         "-of", "csv=p=0", str(path)],
        capture_output=True, text=True, check=True,
    )
    nb = probe.stdout.strip()
    num, den = map(int, fps_str.split("/"))
    fps_float = num / den
    if nb.isdigit():
        return int(nb) / fps_float
    # fallback: 用 duration tag
    probe2 = subprocess.run(
        ["ffprobe", "-v", "quiet",
         "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)],
        capture_output=True, text=True, check=True,
    )
    return float(probe2.stdout.strip() or "0")


def scale_filter(label_in: str, label_out: str, target_h: int) -> str:
    """生成将视频等比缩放到 target_h 高度的 filter 片段。"""
    return f"[{label_in}]scale=-2:{target_h}[{label_out}]"


def hstack_videos(
    stereo: Path,
    depth: Path,
    output: Path,
    scale_depth: bool = False,
) -> None:
    """
    将 stereo 与 depth 左右拼接输出。
    若两者高度不一致，自动将 depth 缩放至 stereo 的高度。
    """
    s_info = get_video_info(stereo)
    d_info = get_video_info(depth)
    fps = s_info["fps"]

    sh, dh = s_info["height"], d_info["height"]
    duration = get_nb_frames(stereo, fps)

    if sh == dh:
        # 高度一致，直接 hstack
        filter_complex = "[0:v][1:v]hstack=inputs=2[out]"
    else:
        # 将 depth 缩放至与 stereo 相同高度
        filter_complex = (
            f"[1:v]scale=-2:{sh}[depth_scaled];"
            f"[0:v][depth_scaled]hstack=inputs=2[out]"
        )

    sw = s_info["width"]
    dw_display = d_info["width"] if sh == dh else int(d_info["width"] * sh / dh)
    print(f"\n[拼接] {stereo.name}  ({sw}×{sh})")
    print(f"       + {depth.name}  ({d_info['width']}×{dh})")
    print(f"  => {output.name}  ({sw + dw_display}×{sh})  {duration:.2f}s @ {fps}fps")

    cmd = [
        "ffmpeg", "-y",
        "-i", str(stereo),
        "-i", str(depth),
        "-filter_complex", filter_complex,
        "-map", "[out]",
        "-map", "0:a?",          # 保留主视频音频（若存在）
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-c:a", "copy",
        "-t", str(duration),
        "-r", fps,
        str(output),
    ]
    subprocess.run(cmd, check=True)
    print(f"  [完成] => {output}")


# ──────────────────────────────────────────────
# 主逻辑
# ──────────────────────────────────────────────

def extract_index(name: str, prefix: str) -> str | None:
    """从文件名中提取前缀后面的数字索引（例如 stereo_video1 → '1'）。"""
    m = re.fullmatch(re.escape(prefix) + r"(\d+)", name)
    return m.group(1) if m else None


def process_dir(dir_name: str) -> None:
    directory = MATERIALS / dir_name
    if not directory.is_dir():
        print(f"[跳过] 目录不存在: {directory}")
        return

    stereo_prefix, depth_prefix = DIR_PATTERNS[dir_name]
    output_dir = directory / "stitched"
    output_dir.mkdir(exist_ok=True)

    # 按索引收集 stereo 文件
    stereo_files: dict[str, Path] = {}
    depth_files:  dict[str, Path] = {}

    for mp4 in sorted(directory.glob("*.mp4")):
        idx = extract_index(mp4.stem, stereo_prefix)
        if idx is not None:
            stereo_files[idx] = mp4
            continue
        idx = extract_index(mp4.stem, depth_prefix)
        if idx is not None:
            depth_files[idx] = mp4

    if not stereo_files:
        print(f"[警告] {dir_name}: 未找到匹配 '{stereo_prefix}*.mp4' 的文件")
        return
    if not depth_files:
        print(f"[警告] {dir_name}: 未找到匹配 '{depth_prefix}*.mp4' 的文件")
        return

    common = sorted(set(stereo_files) & set(depth_files))
    if not common:
        print(f"[警告] {dir_name}: stereo 和 depth 文件没有匹配的索引")
        return

    print(f"\n=== {dir_name}（共 {len(common)} 对）===")
    for idx in common:
        out_name = f"{stereo_prefix}{idx}_with_{depth_prefix}{idx}.mp4"
        hstack_videos(
            stereo=stereo_files[idx],
            depth=depth_files[idx],
            output=output_dir / out_name,
        )

    only_stereo = set(stereo_files) - set(depth_files)
    only_depth  = set(depth_files)  - set(stereo_files)
    if only_stereo:
        print(f"[跳过] {dir_name}: 仅有 stereo 无对应 depth 的索引: {sorted(only_stereo)}")
    if only_depth:
        print(f"[跳过] {dir_name}: 仅有 depth 无对应 stereo 的索引: {sorted(only_depth)}")


def main() -> None:
    targets = sys.argv[1:] or list(DIR_PATTERNS.keys())
    invalid = [t for t in targets if t not in DIR_PATTERNS]
    if invalid:
        valid_list = ", ".join(DIR_PATTERNS.keys())
        print(f"[错误] 未知目录名: {invalid}。可选值: {valid_list}")
        sys.exit(1)

    for t in targets:
        process_dir(t)

    print("\n全部完成。")


if __name__ == "__main__":
    main()
