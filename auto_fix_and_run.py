#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import sys
import os
import re
import time

def run_command(cmd):
    """运行命令并返回结果"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
        return result.returncode, result.stdout, result.stderr or ""
    except Exception as e:
        return -1, "", str(e)

def analyze_error(stderr):
    """分析错误信息并返回修复建议"""
    if not stderr:
        return "unknown_error"
    
    if "AttributeError: module 'numpy' has no attribute 'float'" in stderr:
        return "numpy_compatibility"
    elif "numpy.AxisError: axis 2 is out of bounds" in stderr:
        return "axis_error"
    elif "No module named" in stderr:
        return "missing_module"
    elif "ModuleNotFoundError" in stderr:
        return "missing_module"
    else:
        return "unknown_error"

def fix_numpy_compatibility():
    """修复NumPy兼容性问题"""
    print("🔧 修复NumPy兼容性问题...")
    
    # 修复 my_awing_arch.py
    file_path = "src/face3d/util/my_awing_arch.py"
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 修复 np.float -> np.float64
            content = content.replace("np.float", "np.float64")
            content = content.replace("np.int", "np.int32")
            
            # 修复 axis 错误
            content = re.sub(r'np\.argmax\(heatline, axis=2\)', 'np.argmax(heatline, axis=1)', content)
            content = re.sub(r'np\.stack\(\(indexes % W, indexes // W\), axis=2\)', 'np.stack((indexes % W, indexes // W), axis=1)', content)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print("✓ 已修复 my_awing_arch.py")
        except Exception as e:
            print(f"✗ 修复 my_awing_arch.py 失败: {e}")
    
    # 修复 torch2onnx.py
    file_path = "src/face3d/models/arcface_torch/torch2onnx.py"
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            content = content.replace("np.float", "np.float32")
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print("✓ 已修复 torch2onnx.py")
        except Exception as e:
            print(f"✗ 修复 torch2onnx.py 失败: {e}")
    
    # 修复其他arcface文件
    arcface_files = [
        "src/face3d/models/arcface_torch/onnx_ijbc.py",
        "src/face3d/models/arcface_torch/eval_ijbc.py",
        "src/face3d/models/arcface_torch/utils/plot.py"
    ]
    
    for file_path in arcface_files:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                content = content.replace("np.int", "np.int32")
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✓ 已修复 {file_path}")
            except Exception as e:
                print(f"✗ 修复 {file_path} 失败: {e}")

def install_missing_modules():
    """安装缺失的模块"""
    print("📦 安装缺失的模块...")
    
    # 安装常用缺失模块
    modules_to_install = [
        "opencv-python",
        "torch",
        "torchvision", 
        "torchaudio",
        "face-alignment",
        "librosa",
        "scipy",
        "numpy",
        "pillow",
        "matplotlib"
    ]
    
    for module in modules_to_install:
        print(f"正在安装 {module}...")
        returncode, stdout, stderr = run_command(f"pip install {module}")
        if returncode == 0:
            print(f"✓ {module} 安装成功")
        else:
            print(f"✗ {module} 安装失败: {stderr}")

def main():
    """主函数"""
    print("🚀 开始自动修复和运行SadTalker...")
    
    max_attempts = 10
    attempt = 1
    
    while attempt <= max_attempts:
        print(f"\n{'='*50}")
        print(f"第 {attempt} 次尝试")
        print(f"{'='*50}")
        
        # 激活conda环境并运行
        cmd = "conda activate sadtalker && python .\\main.py --text \"欢迎来到神奈川\" --image .\\shenyanan.jpg"
        returncode, stdout, stderr = run_command(cmd)
        
        print("输出:", stdout[:500] + "..." if len(stdout) > 500 else stdout)
        if stderr:
            print("错误:", stderr[:500] + "..." if len(stderr) > 500 else stderr)
        
        if returncode == 0:
            print("🎉 成功！程序运行完成")
            break
        
        # 分析错误并修复
        error_type = analyze_error(stderr)
        print(f"检测到错误类型: {error_type}")
        
        if error_type == "numpy_compatibility":
            fix_numpy_compatibility()
        elif error_type == "axis_error":
            fix_numpy_compatibility()  # axis错误也在numpy兼容性修复中
        elif error_type == "missing_module":
            install_missing_modules()
        else:
            print("未知错误类型，尝试通用修复...")
            fix_numpy_compatibility()
            install_missing_modules()
        
        attempt += 1
        time.sleep(2)  # 等待2秒再试
    
    if attempt > max_attempts:
        print("❌ 达到最大尝试次数，请手动检查错误")
    else:
        print("✅ 自动修复完成！")

if __name__ == "__main__":
    main() 