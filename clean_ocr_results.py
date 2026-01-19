#!/usr/bin/env python3
"""
整理OCR结果 - 清理重复和错误识别
"""

def clean_and_merge_results(input_file, output_file):
    """读取OCR结果并清理"""
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 解析结果
    time_segments = {}
    current_timestamp = None
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('='):
            continue
        
        if line.startswith('['):
            # 时间戳行
            current_timestamp = line
            if current_timestamp not in time_segments:
                time_segments[current_timestamp] = []
        elif current_timestamp:
            # 文字内容
            time_segments[current_timestamp].append(line)
    
    # 按时间排序
    sorted_timestamps = sorted(time_segments.keys())
    
    # 生成清理后的输出
    output_lines = []
    output_lines.append("=" * 60)
    output_lines.append("视频OCR文字提取结果 (已清理)")
    output_lines.append("时间戳格式: [M:SS-M:SS] (秒为单位)")
    output_lines.append("=" * 60)
    output_lines.append("")
    
    for timestamp in sorted_timestamps:
        texts = time_segments[timestamp]
        
        # 去重 - 保持原始顺序
        unique_texts = []
        seen = set()
        for text in texts:
            if text not in seen:
                unique_texts.append(text)
                seen.add(text)
        
        output_lines.append(timestamp)
        for text in unique_texts:
            output_lines.append(text)
        output_lines.append("")
    
    # 保存结果
    result = "\n".join(output_lines)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result)
    
    print(f"清理完成！")
    print(f"原始文字块数: {sum(len(texts) for texts in time_segments.values())}")
    print(f"清理后文字块数: {sum(len(set(texts)) for texts in time_segments.values())}")
    print(f"输出文件: {output_file}")
    
    return result


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python clean_ocr_results.py <input_file> [output_file]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file.replace('.txt', '_cleaned.txt')
    
    clean_and_merge_results(input_file, output_file)
