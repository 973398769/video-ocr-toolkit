#!/usr/bin/env python3
"""
创建包含文字的演示视频
用于展示Video OCR Toolkit的功能
"""

import cv2
import numpy as np


def create_demo_video(output_path='demo_text_video.mp4', duration=10, fps=30):
    """创建包含文字的演示视频"""
    
    width, height = 1280, 720
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    total_frames = duration * fps
    
    print(f"创建演示视频: {output_path}")
    print(f"分辨率: {width}x{height}, 时长: {duration}秒, 帧率: {fps} FPS")
    
    # 定义要显示的文字场景
    scenes = [
        # (开始帧, 结束帧, 文字, 位置, 字体大小, 颜色)
        (0, 90, "VIDEO OCR TOOLKIT", (200, 200), 2.5, (255, 255, 255)),
        (0, 90, "Demo Video", (300, 300), 1.5, (200, 200, 255)),
        
        (90, 180, "Text Detection", (100, 150), 2.0, (255, 255, 100)),
        (90, 180, "Multi-language Support", (100, 300), 1.3, (100, 255, 255)),
        (90, 180, "English • 中文 • 日本語", (100, 400), 1.0, (200, 200, 200)),
        
        (180, 270, "Timestamp: 6-9 seconds", (150, 250), 1.5, (100, 255, 100)),
        (180, 270, "Precise Frame Analysis", (150, 350), 1.2, (255, 200, 100)),
        (180, 270, "GPU Accelerated OCR", (150, 450), 1.2, (255, 100, 255)),
        
        (270, 300, "GitHub: video-ocr-toolkit", (100, 300), 1.3, (255, 255, 255)),
        (270, 300, "Open Source • MIT License", (100, 400), 1.0, (180, 180, 180)),
    ]
    
    for frame_idx in range(total_frames):
        # 创建渐变背景
        progress = frame_idx / total_frames
        bg_color = int(20 + progress * 40)
        frame = np.ones((height, width, 3), dtype=np.uint8) * bg_color
        
        # 添加网格效果
        for i in range(0, width, 100):
            cv2.line(frame, (i, 0), (i, height), (bg_color + 20, bg_color + 20, bg_color + 20), 1)
        for i in range(0, height, 100):
            cv2.line(frame, (0, i), (width, i), (bg_color + 20, bg_color + 20, bg_color + 20), 1)
        
        # 显示当前时间
        current_time = frame_idx / fps
        time_text = f"Time: {current_time:.1f}s"
        cv2.putText(frame, time_text, (width - 200, 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (150, 150, 150), 2)
        
        # 绘制场景中的文字
        for start_frame, end_frame, text, pos, size, color in scenes:
            if start_frame <= frame_idx < end_frame:
                # 添加文字阴影效果
                cv2.putText(frame, text, (pos[0] + 3, pos[1] + 3), 
                           cv2.FONT_HERSHEY_SIMPLEX, size, (0, 0, 0), 
                           int(size * 3))
                # 绘制主文字
                cv2.putText(frame, text, pos, 
                           cv2.FONT_HERSHEY_SIMPLEX, size, color, 
                           int(size * 2))
        
        out.write(frame)
        
        # 显示进度
        if frame_idx % 30 == 0:
            progress_pct = (frame_idx / total_frames) * 100
            print(f"  进度: {progress_pct:.1f}%")
    
    out.release()
    print(f"\n✅ 演示视频创建完成: {output_path}")
    print(f"  文件大小: {cv2.os.path.getsize(output_path) / 1024:.1f} KB")


if __name__ == "__main__":
    create_demo_video('demo_text_video.mp4', duration=10, fps=30)
