# -*- coding: utf-8 -*-
import sys
import os
from pathlib import Path

# 添加当前目录到路径
current_dir = Path(__file__).parent.resolve()
sys.path.insert(0, str(current_dir))

# 切换到当前目录
os.chdir(str(current_dir))

# 导入并运行
try:
    from generate_new_report import generate_html_report
    result = generate_html_report()
    print(f"成功生成报告: {result}")
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()

