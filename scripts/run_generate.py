#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""运行生成报告的脚本"""
import os
import sys

# 设置工作目录
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# 导入并运行生成函数
from generate_new_report import generate_html_report

if __name__ == '__main__':
    try:
        generate_html_report()
        print("报告生成成功！")
    except Exception as e:
        print(f"生成报告时出错: {e}")
        import traceback
        traceback.print_exc()

