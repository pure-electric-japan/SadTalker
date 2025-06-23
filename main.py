import argparse
import os
import subprocess
from gtts import gTTS


def text_to_speech(text, output_path):
    tts = gTTS(text, lang='zh-cn')
    tts.save(output_path)
    print(f"[INFO] 语音已保存到: {output_path}")

def run_sadtalker(image_path, audio_path, result_dir):
    os.makedirs(result_dir, exist_ok=True)
    # 假设SadTalker已安装，且inference.py在PATH或当前目录
    cmd = [
        'python', 'inference.py',
        '--driven_audio', audio_path,
        '--source_image', image_path,
        '--result_dir', result_dir
    ]
    print(f"[INFO] 正在调用SadTalker生成视频...")
    subprocess.run(cmd, check=True)
    # 查找生成的视频
    for file in os.listdir(result_dir):
        if file.endswith('.mp4'):
            return os.path.join(result_dir, file)
    raise FileNotFoundError('未找到生成的视频文件')

def main():
    parser = argparse.ArgumentParser(description='文本转数字人视频 (gTTS + SadTalker)')
    parser.add_argument('--text', type=str, required=True, help='要朗读的文本')
    parser.add_argument('--image', type=str, required=True, help='人物照片路径')
    parser.add_argument('--output', type=str, default='output.mp4', help='输出视频路径')
    parser.add_argument('--tmpdir', type=str, default='tmp', help='临时文件目录')
    parser.add_argument('--resultdir', type=str, default='results', help='SadTalker输出目录')
    args = parser.parse_args()

    os.makedirs(args.tmpdir, exist_ok=True)
    audio_path = os.path.join(args.tmpdir, 'output.wav')
    text_to_speech(args.text, audio_path)

    video_path = run_sadtalker(args.image, audio_path, args.resultdir)

    # 移动/重命名输出视频
    final_output = args.output
    os.replace(video_path, final_output)
    print(f"[SUCCESS] 数字人视频已生成: {final_output}")

if __name__ == "__main__":
    main()
