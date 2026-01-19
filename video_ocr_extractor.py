#!/usr/bin/env python3
"""
视频OCR文字提取工具 V2
从视频中提取所有可见文字，按时间戳和位置排序
时间戳格式: [M:SS-M:SS] (秒为单位)
精确追踪: 第一个字母可读 → 最后一个字母完全消失后
"""

import cv2
import easyocr
import numpy as np
from collections import defaultdict
import argparse
import os
from typing import List, Dict, Tuple


class VideoOCRExtractor:
    def __init__(self, video_path: str, languages: List[str] = ['en', 'ch_sim'], 
                 frame_interval: int = 1, confidence_threshold: float = 0.3,
                 min_text_length: int = 1):
        """
        初始化视频OCR提取器
        
        Args:
            video_path: 视频文件路径
            languages: OCR识别语言列表 (默认英文和简体中文)
            frame_interval: 采样间隔（每N帧处理一次，建议1以获得最精确的时间戳）
            confidence_threshold: 置信度阈值（0-1之间）
            min_text_length: 最小文字长度（过滤太短的文字）
        """
        self.video_path = video_path
        self.frame_interval = frame_interval
        self.confidence_threshold = confidence_threshold
        self.min_text_length = min_text_length
        
        # 初始化OCR读取器
        print("正在初始化OCR引擎...")
        self.reader = easyocr.Reader(languages, gpu=True)
        print("OCR引擎初始化完成！")
        
        # 存储文字块的信息
        self.text_blocks = []
        
    def format_timestamp_seconds(self, seconds: float) -> str:
        """
        将秒数转换为 M:SS 或 MM:SS 格式
        例如: 0:00, 0:01, 1:23, 12:45
        """
        total_seconds = int(seconds)
        minutes = total_seconds // 60
        secs = total_seconds % 60
        return f"{minutes}:{secs:02d}"
    
    def get_text_position_key(self, bbox) -> Tuple[int, int]:
        """
        获取文字块的位置键值（用于排序）
        返回 (y坐标, x坐标) 以实现从上到下、从左到右的排序
        """
        # bbox 是 [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
        top_left = bbox[0]
        y_pos = int(top_left[1])
        x_pos = int(top_left[0])
        return (y_pos, x_pos)
    
    def is_similar_text_block(self, text1: str, bbox1, text2: str, bbox2, 
                              position_threshold: int = 50) -> bool:
        """
        判断两个文字块是否相似（同一文字在不同帧）
        
        Args:
            text1, text2: 文字内容
            bbox1, bbox2: 边界框
            position_threshold: 位置阈值（像素）
        """
        # 文字必须完全相同
        if text1 != text2:
            return False
        
        # 位置必须接近
        pos1 = self.get_text_position_key(bbox1)
        pos2 = self.get_text_position_key(bbox2)
        
        y_diff = abs(pos1[0] - pos2[0])
        x_diff = abs(pos1[1] - pos2[1])
        
        return y_diff < position_threshold and x_diff < position_threshold
    
    def extract_text_from_video(self):
        """从视频中提取所有文字并记录精确时间戳"""
        cap = cv2.VideoCapture(self.video_path)
        
        if not cap.isOpened():
            raise ValueError(f"无法打开视频文件: {self.video_path}")
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps
        
        print(f"视频信息: {fps:.2f} FPS, {total_frames} 帧, 时长: {self.format_timestamp_seconds(duration)}")
        print(f"开始提取文字（每 {self.frame_interval} 帧采样一次）...")
        
        frame_count = 0
        active_texts = []  # 当前活跃的文字块 {text, bbox, start_time, last_seen_time, first_frame}
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # 只处理指定间隔的帧
            if frame_count % self.frame_interval != 0:
                frame_count += 1
                continue
            
            current_time = frame_count / fps
            
            # 进度显示
            if frame_count % (self.frame_interval * 30) == 0:
                progress = (frame_count / total_frames) * 100
                print(f"进度: {progress:.1f}% ({self.format_timestamp_seconds(current_time)})")
            
            # 执行OCR
            results = self.reader.readtext(frame)
            
            # 处理当前帧的OCR结果
            current_frame_texts = []
            for (bbox, text, confidence) in results:
                # 过滤掉置信度低和文字太短的结果
                text_stripped = text.strip()
                if confidence >= self.confidence_threshold and len(text_stripped) >= self.min_text_length:
                    current_frame_texts.append({
                        'text': text_stripped,
                        'bbox': bbox,
                        'confidence': confidence
                    })
            
            # 更新活跃文字块
            matched_indices = set()
            texts_to_remove = []
            
            for i, active_text in enumerate(active_texts):
                found_match = False
                for j, current_text in enumerate(current_frame_texts):
                    if j not in matched_indices and self.is_similar_text_block(
                        active_text['text'], active_text['bbox'],
                        current_text['text'], current_text['bbox']
                    ):
                        # 找到匹配，更新最后出现时间
                        active_text['last_seen_time'] = current_time
                        active_text['last_seen_frame'] = frame_count
                        matched_indices.add(j)
                        found_match = True
                        break
                
                # 如果没有找到匹配，说明文字消失了
                if not found_match:
                    # 计算结束时间：最后一次看到的时间 + 一帧的时间
                    # (因为要求是"immediately after the last letter becomes fully unreadable")
                    end_time = active_text['last_seen_time'] + (1.0 / fps)
                    
                    # 保存这个文字块
                    self.text_blocks.append({
                        'text': active_text['text'],
                        'start_time': active_text['start_time'],
                        'end_time': end_time,
                        'position': self.get_text_position_key(active_text['bbox'])
                    })
                    texts_to_remove.append(i)
            
            # 移除已消失的文字块
            active_texts = [t for i, t in enumerate(active_texts) if i not in texts_to_remove]
            
            # 添加新出现的文字块
            for j, current_text in enumerate(current_frame_texts):
                if j not in matched_indices:
                    # 开始时间就是当前时间（第一个字母变得可读的时刻）
                    active_texts.append({
                        'text': current_text['text'],
                        'bbox': current_text['bbox'],
                        'start_time': current_time,
                        'last_seen_time': current_time,
                        'first_frame': frame_count,
                        'last_seen_frame': frame_count
                    })
            
            frame_count += 1
        
        # 处理视频结束时仍活跃的文字块
        for active_text in active_texts:
            # 视频结束时，结束时间就是视频的结束时间
            end_time = min(duration, active_text['last_seen_time'] + (1.0 / fps))
            
            self.text_blocks.append({
                'text': active_text['text'],
                'start_time': active_text['start_time'],
                'end_time': end_time,
                'position': self.get_text_position_key(active_text['bbox'])
            })
        
        cap.release()
        print(f"\n提取完成！共识别 {len(self.text_blocks)} 个文字块")
    
    def group_texts_by_time(self) -> Dict[Tuple[float, float], List[Dict]]:
        """按时间段分组文字块"""
        time_groups = defaultdict(list)
        
        for block in self.text_blocks:
            time_key = (block['start_time'], block['end_time'])
            time_groups[time_key].append(block)
        
        return time_groups
    
    def generate_output(self, output_path: str = None):
        """
        生成输出文件
        按照要求：每个时间段内的文字从上到下、从左到右排序
        时间戳格式: [M:SS-M:SS]
        """
        if not self.text_blocks:
            print("没有识别到任何文字！")
            return
        
        # 按时间段分组
        time_groups = self.group_texts_by_time()
        
        # 按时间排序
        sorted_times = sorted(time_groups.keys())
        
        # 生成输出
        output_lines = []
        output_lines.append("=" * 60)
        output_lines.append("视频OCR文字提取结果")
        output_lines.append(f"视频文件: {os.path.basename(self.video_path)}")
        output_lines.append("时间戳格式: [M:SS-M:SS] (秒为单位)")
        output_lines.append("=" * 60)
        output_lines.append("")
        
        for start_time, end_time in sorted_times:
            texts = time_groups[(start_time, end_time)]
            
            # 按位置排序（从上到下，从左到右）
            texts.sort(key=lambda x: x['position'])
            
            # 输出时间戳 [M:SS-M:SS]
            start_ts = self.format_timestamp_seconds(start_time)
            end_ts = self.format_timestamp_seconds(end_time)
            
            # 每个文字块都独立显示时间戳
            for text_block in texts:
                output_lines.append(f"[{start_ts}-{end_ts}]")
                output_lines.append(text_block['text'])
            
            output_lines.append("")  # 空行分隔不同时间段
        
        result = "\n".join(output_lines)
        
        # 输出到控制台
        print("\n" + result)
        
        # 保存到文件
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result)
            print(f"\n结果已保存到: {output_path}")
        
        return result


def main():
    parser = argparse.ArgumentParser(
        description='从视频中提取所有可见文字，按秒级时间戳记录',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python video_ocr_extractor_v2.py video.mp4
  python video_ocr_extractor_v2.py video.mp4 -o output.txt
  python video_ocr_extractor_v2.py video.mp4 -l en -i 1
  python video_ocr_extractor_v2.py video.mp4 --confidence 0.5

说明:
  - 时间戳格式为秒: [0:00-0:01] 表示0秒到1秒
  - 开始时间: 第一个字母变得可读的时刻
  - 结束时间: 最后一个字母完全消失后的时刻
  - 建议使用 -i 1 以获得最精确的时间戳
        """
    )
    
    parser.add_argument('video_path', help='视频文件路径')
    parser.add_argument('-o', '--output', help='输出文件路径（默认: video_ocr_output.txt)')
    parser.add_argument('-l', '--languages', nargs='+', 
                       default=['en', 'ch_sim'],
                       help='OCR识别语言 (默认: en ch_sim)')
    parser.add_argument('-i', '--interval', type=int, default=1,
                       help='帧采样间隔 (默认: 1, 建议保持1以获得精确时间戳)')
    parser.add_argument('-c', '--confidence', type=float, default=0.3,
                       help='置信度阈值 0-1 (默认: 0.3)')
    parser.add_argument('--min-length', type=int, default=1,
                       help='最小文字长度，过滤太短的文字 (默认: 1)')
    
    args = parser.parse_args()
    
    # 检查视频文件是否存在
    if not os.path.exists(args.video_path):
        print(f"错误: 找不到视频文件 '{args.video_path}'")
        return
    
    # 设置输出路径
    if not args.output:
        video_name = os.path.splitext(os.path.basename(args.video_path))[0]
        args.output = f"{video_name}_ocr_seconds.txt"
    
    # 创建提取器并执行
    try:
        extractor = VideoOCRExtractor(
            video_path=args.video_path,
            languages=args.languages,
            frame_interval=args.interval,
            confidence_threshold=args.confidence,
            min_text_length=args.min_length
        )
        
        extractor.extract_text_from_video()
        extractor.generate_output(args.output)
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
