#!/usr/bin/env python3
"""
视频OCR可视化工具
将识别到的文字用红色框标注并保存每一帧
"""

import cv2
import easyocr
import numpy as np
from pathlib import Path
import argparse
import os


class VideoOCRVisualizer:
    def __init__(self, video_path: str, output_dir: str = None, 
                 languages: list = ['en', 'ch_sim'],
                 confidence_threshold: float = 0.3,
                 save_video: bool = True):
        """
        初始化视频OCR可视化工具
        
        Args:
            video_path: 视频文件路径
            output_dir: 输出目录（默认为视频名_frames）
            languages: OCR识别语言
            confidence_threshold: 置信度阈值
            save_video: 是否保存为视频（否则只保存帧图像）
        """
        self.video_path = video_path
        self.confidence_threshold = confidence_threshold
        self.save_video = save_video
        
        # 设置输出目录
        if output_dir is None:
            video_name = Path(video_path).stem
            self.output_dir = f"{video_name}_annotated_frames"
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
            标注后的帧
        """
        annotated = frame.copy()
        
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
        
        return annotated
    
    def process_video(self):
        """处理视频并生成标注帧"""
        cap = cv2.VideoCapture(self.video_path)
        
        if not cap.isOpened():
            raise ValueError(f"无法打开视频: {self.video_path}")
        
        # 获取视频信息
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        print(f"\n视频信息:")
        print(f"  分辨率: {width}x{height}")
        print(f"  帧率: {fps:.2f} FPS")
        print(f"  总帧数: {total_frames}")
        print(f"\n开始处理...")
        
        # 如果保存为视频，创建视频写入器
        video_writer = None
        if self.save_video:
            output_video_path = os.path.join(
                self.output_dir, 
                f"{Path(self.video_path).stem}_annotated.mp4"
            )
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            video_writer = cv2.VideoWriter(
                output_video_path, fourcc, fps, (width, height)
            )
            print(f"  将保存标注视频: {output_video_path}")
        
        frame_count = 0
        annotated_frames = []
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            
            # 显示进度
            if frame_count % 10 == 0 or frame_count == 1:
                progress = (frame_count / total_frames) * 100
                print(f"  进度: {progress:.1f}% (帧 {frame_count}/{total_frames})")
            
            # 执行OCR
            results = self.reader.readtext(frame)
            
            # 绘制标注
            annotated_frame = self.draw_boxes(frame, results)
            
            # 保存帧图像
            frame_filename = os.path.join(
                self.output_dir, 
                f"frame_{frame_count:05d}.jpg"
            )
            cv2.imwrite(frame_filename, annotated_frame)
            
            # 如果需要，写入视频
            if video_writer is not None:
                video_writer.write(annotated_frame)
            
            annotated_frames.append({
                'frame_number': frame_count,
                'ocr_count': len([r for r in results if r[2] >= self.confidence_threshold]),
                'filename': frame_filename
            })
        
        # 释放资源
        cap.release()
        if video_writer is not None:
            video_writer.release()
        
        print(f"\n✅ 处理完成！")
        print(f"  总共处理: {frame_count} 帧")
        print(f"  保存位置: {self.output_dir}/")
        
        if self.save_video:
            print(f"  标注视频: {output_video_path}")
        
        # 生成统计报告
        self.generate_report(annotated_frames)
        
        return annotated_frames
    
    def generate_report(self, frames_info):
        """生成统计报告"""
        report_path = os.path.join(self.output_dir, "annotation_report.txt")
        
        total_ocr_detections = sum(f['ocr_count'] for f in frames_info)
        frames_with_text = sum(1 for f in frames_info if f['ocr_count'] > 0)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("视频OCR标注报告\n")
            f.write("=" * 60 + "\n\n")
            
            f.write(f"视频文件: {self.video_path}\n")
            f.write(f"输出目录: {self.output_dir}\n\n")
            
            f.write(f"总帧数: {len(frames_info)}\n")
            f.write(f"包含文字的帧数: {frames_with_text}\n")
            f.write(f"总检测到的文字块: {total_ocr_detections}\n")
            f.write(f"平均每帧文字块数: {total_ocr_detections/len(frames_info):.2f}\n\n")
            
            f.write("=" * 60 + "\n")
            f.write("每帧详细信息:\n")
            f.write("=" * 60 + "\n\n")
            
            for frame_info in frames_info:
                if frame_info['ocr_count'] > 0:
                    f.write(f"帧 #{frame_info['frame_number']:5d}: "
                           f"{frame_info['ocr_count']} 个文字块 - "
                           f"{frame_info['filename']}\n")
        
        print(f"  统计报告: {report_path}")


def main():
    parser = argparse.ArgumentParser(
        description='视频OCR可视化工具 - 用红色框标注识别到的文字',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python video_ocr_visualizer.py video.mp4
  python video_ocr_visualizer.py video.mp4 -o output_folder
  python video_ocr_visualizer.py video.mp4 --no-video  # 只保存帧图像
  python video_ocr_visualizer.py video.mp4 -c 0.5      # 提高置信度阈值
        """
    )
    
    parser.add_argument('video_path', help='视频文件路径')
    parser.add_argument('-o', '--output', help='输出目录')
    parser.add_argument('-l', '--languages', nargs='+', 
                       default=['en', 'ch_sim'],
                       help='OCR识别语言')
    parser.add_argument('-c', '--confidence', type=float, default=0.3,
                       help='置信度阈值 (0-1)')
    parser.add_argument('--no-video', action='store_true',
                       help='不生成标注视频，只保存帧图像')
    
    args = parser.parse_args()
    
    # 检查视频文件
    if not os.path.exists(args.video_path):
        print(f"错误: 找不到视频文件 '{args.video_path}'")
        return
    
    try:
        visualizer = VideoOCRVisualizer(
            video_path=args.video_path,
            output_dir=args.output,
            languages=args.languages,
            confidence_threshold=args.confidence,
            save_video=not args.no_video
        )
        
        visualizer.process_video()
        
        print("\n🎉 完成！你现在可以:")
        print(f"   1. 查看标注后的帧图像: {visualizer.output_dir}/")
        if not args.no_video:
            print(f"   2. 播放标注视频: {visualizer.output_dir}/*_annotated.mp4")
        print(f"   3. 查看统计报告: {visualizer.output_dir}/annotation_report.txt")
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
