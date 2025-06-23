#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import sys
import os

# 添加src目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_calculate_points():
    """测试calculate_points函数"""
    try:
        from face3d.util.my_awing_arch import calculate_points
        
        # 创建一个模拟的heatmaps数组
        B, N, H, W = 1, 68, 64, 64  # 批次大小=1, 关键点数量=68, 高度=64, 宽度=64
        heatmaps = np.random.random((B, N, H, W))
        
        # 测试函数
        result = calculate_points(heatmaps)
        
        print("✓ calculate_points函数测试通过")
        print(f"输入形状: {heatmaps.shape}")
        print(f"输出形状: {result.shape}")
        print(f"输出类型: {result.dtype}")
        
        return True
        
    except Exception as e:
        print(f"✗ calculate_points函数测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_calculate_points()
    sys.exit(0 if success else 1) 