#!/usr/bin/env python3
"""
视频OCR按秒切割工具
按秒切割视频，每秒保存一帧并用红框标注文字
"""

import cv2
import easyocr
import numpy as np
from pathlib import Path
import argparse
import os


class VideoOCRBySecond:
    def __init__(self, video_path: str, output_dir: str = None, 
                 languages: list = ['en', 'ch_sim'],
                 confidence_threshold: float = 0.3):
        """
        初始化视频OCR按秒切割工具
        
        Args:
            video_path: 视频文件路径
            output_dir: 输出目录（默认为视频名_by_seconds）
            languages: OCR识别语言
            confidence_threshold: 置信度阈值
        """
        self.video_path = video_path
        self.confidence_threshold = confidence_threshold
        
        # 设置输出目录
        if output_dir is None:
            video_name = Path(video_path).stem
            self.output_dir = f"{video_name}_by_seconds"
        else:
            self.output_dir = output_dir
        
        # 创建输出目录
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 初始化OCR
        print("正在初始化OCR引擎...")
        self.reader = easyocr.Reader(languages, gpu=True)
        print("OCR引擎初始化完成！")
    
    def draw_boxes(self, frame, ocr_results):
        """
        在帧上绘制红色边框
        
        Args:
            frame: 原始帧
            ocr_results: OCR识别结果
        
        Returns:
            标注后的帧和文字列表
        """
        annotated = frame.copy()
        detected_texts = []
        
        for (bbox, text, confidence) in ocr_results:
            if confidence >= self.confidence_threshold:
                # 获取边界框的四个点
                pts = np.array(bbox, dtype=np.int32)
                
                # 画红色边框（厚度为3）
                cv2.polylines(annotated, [pts], True, (0, 0, 255), 3)
                
                # 在边框上方添加文字标签（带背景）
                top_left = tuple(pts[0])
                label = f"{text} ({confidence:.2f})"
                
                # 获取文字大小
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 0.6
                font_thickness = 2
                (text_width, text_height), baseline = cv2.getTextSize(
                    label, font, font_scale, font_thickness
                )
                
                # 画文字背景（红色半透明）
                bg_top_left = (top_left[0], top_left[1] - text_height - 10)
                bg_bottom_right = (top_left[0] + text_width, top_left[1])
                
                # 创建半透明背景
                overlay = annotated.copy()
                cv2.rectangle(overlay, bg_top_left, bg_bottom_right, (0, 0, 255), -1)
                cv2.addWeighted(overlay, 0.6, annotated, 0.4, 0, annotated)
                
                # 画白色文字
                text_pos = (top_left[0], top_left[1] - 5)
                cv2.putText(annotated, label, text_pos, font, 
                           font_scale, (255, 255, 255), font_thickness)
                
                detected_texts.append(text)
        
        return annotated, detected_texts
    
    def format_timestamp(self, seconds: int) -> str:
        """将秒数转换为 M:SS 格式"""
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes}:{secs:02d}"
    
    def process_video(self):
        """处理视频并按秒保存标注帧"""
        cap = cv2.VideoCapture(self.video_path)
        
        if not cap.isOpened():
            raise ValueError(f"无法打开视频: {self.video_path}")
        
        # 获取视频信息
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        duration = int(total_frames / fps) + 1
        
        print(f"\n视频信息:")
        print(f"  分辨率: {width}x{height}")
        print(f"  帧率: {fps:.2f} FPS")
        print(f"  总帧数: {total_frames}")
        print(f"  时长: {duration} 秒")
        print(f"\n开始按秒处理...")
        
        frames_info = []
        
        # 按秒处理
        for second in range(duration):
            # 跳转到这一秒的位置
            frame_position = int(second * fps)
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_position)
            
            ret, frame = cap.read()
            if not ret:
                print(f"  警告: 无法读取第 {second} 秒的帧")
                continue
            
            print(f"  处理第 {second} 秒 ({self.format_timestamp(second)})...")
            
            # 执行OCR
            results = self.reader.readtext(frame)
            
            # 绘制标注
            annotated_frame, detected_texts = self.draw_boxes(frame, results)
            
            # 保存帧图像
            frame_filename = os.path.join(
                self.output_dir, 
                f"second_{second:03d}_{self.format_timestamp(second).replace(':', '-')}.jpg"
            )
            cv2.imwrite(frame_filename, annotated_frame)
            
            frames_info.append({
                'second': second,
                'timestamp': self.format_timestamp(second),
                'text_count': len(detected_texts),
                'texts': detected_texts,
                'filename': frame_filename
            })
        
        # 释放资源
        cap.release()
        
        print(f"\n✅ 处理完成！")
        print(f"  总共处理: {len(frames_info)} 秒")
        print(f"  保存位置: {self.output_dir}/")
        
        # 生成统计报告
        self.generate_report(frames_info)
        
        return frames_info
    
    def generate_report(self, frames_info):
        """生成统计报告"""
        report_path = os.path.join(self.output_dir, "by_second_report.txt")
        
        total_texts = sum(f['text_count'] for f in frames_info)
        seconds_with_text = sum(1 for f in frames_info if f['text_count'] > 0)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("视频OCR按秒切割报告\n")
            f.write("=" * 60 + "\n\n")
            
            f.write(f"视频文件: {self.video_path}\n")
            f.write(f"输出目录: {self.output_dir}\n\n")
            
            f.write(f"总秒数: {len(frames_info)}\n")
            f.write(f"包含文字的秒数: {seconds_with_text}\n")
            f.write(f"总检测到的文字块: {total_texts}\n\n")
            
            f.write("=" * 60 + "\n")
            f.write("每秒详细信息:\n")
            f.write("=" * 60 + "\n\n")
            
            for frame_info in frames_info:
                timestamp = frame_info['timestamp']
                f.write(f"[{timestamp}] 第 {frame_info['second']} 秒:\n")
                
                if frame_info['text_count'] > 0:
                    f.write(f"  检测到 {frame_info['text_count']} 个文字块:\n")
                    for text in frame_info['texts']:
                        f.write(f"    - {text}\n")
                else:
                    f.write("  未检测到文字\n")
                
                f.write(f"  文件: {os.path.basename(frame_info['filename'])}\n\n")
        
        print(f"  统计报告: {report_path}")


def main():
    parser = argparse.ArgumentParser(
        description='视频OCR按秒切割工具 - 每秒保存一帧并用红框标注',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python video_ocr_by_second.py video.mp4
  python video_ocr_by_second.py video.mp4 -o output_folder
  python video_ocr_by_second.py video.mp4 -l en        # 只识别英文
  python video_ocr_by_second.py video.mp4 -c 0.5       # 提高置信度阈值
        """
    )
    
    parser.add_argument('video_path', help='视频文件路径')
    parser.add_argument('-o', '--output', help='输出目录')
    parser.add_argument('-l', '--languages', nargs='+', 
                       default=['en', 'ch_sim'],
                       help='OCR识别语言')
    parser.add_argument('-c', '--confidence', type=float, default=0.3,
                       help='置信度阈值 (0-1)')
    
    args = parser.parse_args()
    
    # 检查视频文件
    if not os.path.exists(args.video_path):
        print(f"错误: 找不到视频文件 '{args.video_path}'")
        return
    
    try:
        processor = VideoOCRBySecond(
            video_path=args.video_path,
            output_dir=args.output,
            languages=args.languages,
            confidence_threshold=args.confidence
        )
        
        processor.process_video()
        
        print("\n🎉 完成！你现在可以:")
        print(f"   1. 查看按秒切割的帧图像: {processor.output_dir}/")
        print(f"   2. 查看统计报告: {processor.output_dir}/by_second_report.txt")
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
