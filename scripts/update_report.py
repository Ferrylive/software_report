#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""更新HTML报告：添加logo、修改配色、添加新功能"""

import json
import base64
import os
from pathlib import Path

# 读取logo图片并转换为base64
def image_to_base64(image_path):
    """将图片转换为base64字符串"""
    if not os.path.exists(image_path):
        return None
    with open(image_path, 'rb') as f:
        img_data = f.read()
        return base64.b64encode(img_data).decode('utf-8')

# 读取result.json
def load_result_json():
    """加载result.json数据"""
    json_path = Path(__file__).parent / 'result.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# 生成牙齿问题二维图SVG
def generate_tooth_chart_svg(result_data):
    """生成牙齿问题二维图SVG"""
    # 提取有问题的牙齿
    problem_teeth = {}
    disease_types = {}
    
    for tooth_data in result_data.get('diseased_teeth', []):
        tooth_num = tooth_data.get('tooth_fdi', '')
        diseases = tooth_data.get('diseases', [])
        
        if tooth_num not in problem_teeth:
            problem_teeth[tooth_num] = []
        
        for disease in diseases:
            label = disease.get('label', '')
            confidence = disease.get('confidence', 0)
            if label not in disease_types:
                disease_types[label] = []
            problem_teeth[tooth_num].append({
                'label': label,
                'confidence': confidence
            })
    
    # 定义疾病类型颜色映射
    disease_colors = {
        'tooth abrasion': '#FFD700',  # 黄色 - 磨损
        'general_caries': '#FF6B6B',  # 红色 - 龋齿
        'twisted tooth': '#4ECDC4',   # 青色 - 扭转牙
    }
    
    # 生成SVG
    svg = '''<svg width="800" height="600" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      .tooth-normal { fill: #E8F5E9; stroke: #4CAF50; stroke-width: 2; }
      .tooth-problem { fill: #FFF9C4; stroke: #FBC02D; stroke-width: 3; }
      .tooth-text { font-family: Arial, sans-serif; font-size: 14px; font-weight: bold; fill: #2E7D32; }
      .tooth-problem-text { font-family: Arial, sans-serif; font-size: 14px; font-weight: bold; fill: #F57F17; }
      .arch-label { font-family: Arial, sans-serif; font-size: 16px; font-weight: bold; fill: #2E7D32; }
    </style>
  </defs>
  
  <!-- 上颌 -->
  <g id="upper-arch">
    <text x="400" y="30" text-anchor="middle" class="arch-label">上颌 (Maxillary)</text>
    <!-- 右上象限 -->
    <g id="upper-right">
'''
    
    # 上颌牙齿位置 (1-16)
    upper_teeth_positions = {
        '1': (50, 80, 30, 25), '2': (90, 80, 30, 25), '3': (130, 80, 30, 25),
        '4': (170, 70, 25, 20), '5': (200, 70, 25, 20),
        '6': (230, 60, 20, 18),
        '7': (255, 50, 18, 15), '8': (275, 45, 15, 12),
        '9': (295, 45, 15, 12), '10': (315, 50, 18, 15),
        '11': (340, 60, 20, 18),
        '12': (370, 70, 25, 20), '13': (400, 70, 25, 20),
        '14': (440, 80, 30, 25), '15': (480, 80, 30, 25), '16': (520, 80, 30, 25),
    }
    
    for tooth_num, (x, y, w, h) in upper_teeth_positions.items():
        is_problem = tooth_num in problem_teeth
        tooth_class = 'tooth-problem' if is_problem else 'tooth-normal'
        text_class = 'tooth-problem-text' if is_problem else 'tooth-text'
        
        svg += f'      <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" class="{tooth_class}"/>\n'
        svg += f'      <text x="{x+w/2}" y="{y+h/2+5}" text-anchor="middle" class="{text_class}">{tooth_num}</text>\n'
    
    svg += '''    </g>
  </g>
  
  <!-- 下颌 -->
  <g id="lower-arch">
    <text x="400" y="350" text-anchor="middle" class="arch-label">下颌 (Mandibular)</text>
    <!-- 左下象限 -->
    <g id="lower-left">
'''
    
    # 下颌牙齿位置 (17-32)
    lower_teeth_positions = {
        '17': (50, 400, 30, 25), '18': (90, 400, 30, 25), '19': (130, 400, 30, 25),
        '20': (170, 410, 25, 20), '21': (200, 410, 25, 20),
        '22': (230, 420, 20, 18),
        '23': (255, 430, 18, 15), '24': (275, 435, 15, 12),
        '25': (295, 435, 15, 12), '26': (315, 430, 18, 15),
        '27': (340, 420, 20, 18),
        '28': (370, 410, 25, 20), '29': (400, 410, 25, 20),
        '30': (440, 400, 30, 25), '31': (480, 400, 30, 25), '32': (520, 400, 30, 25),
    }
    
    for tooth_num, (x, y, w, h) in lower_teeth_positions.items():
        is_problem = tooth_num in problem_teeth
        tooth_class = 'tooth-problem' if is_problem else 'tooth-normal'
        text_class = 'tooth-problem-text' if is_problem else 'tooth-text'
        
        svg += f'      <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" class="{tooth_class}"/>\n'
        svg += f'      <text x="{x+w/2}" y="{y+h/2+5}" text-anchor="middle" class="{text_class}">{tooth_num}</text>\n'
    
    svg += '''    </g>
  </g>
  
  <!-- 图例 -->
  <g id="legend">
    <rect x="600" y="100" width="180" height="120" fill="#F5F5F5" stroke="#4CAF50" stroke-width="2" rx="5"/>
    <text x="690" y="125" text-anchor="middle" font-family="Arial" font-size="14" font-weight="bold" fill="#2E7D32">图例</text>
    <rect x="610" y="140" width="20" height="15" fill="#E8F5E9" stroke="#4CAF50" stroke-width="1"/>
    <text x="635" y="152" font-family="Arial" font-size="12" fill="#2E7D32">正常</text>
    <rect x="610" y="165" width="20" height="15" fill="#FFF9C4" stroke="#FBC02D" stroke-width="2"/>
    <text x="635" y="177" font-family="Arial" font-size="12" fill="#F57F17">有问题</text>
    <rect x="610" y="190" width="20" height="15" fill="#FFD700" stroke="#FBC02D" stroke-width="1"/>
    <text x="635" y="202" font-family="Arial" font-size="12" fill="#2E7D32">磨损</text>
    <rect x="610" y="215" width="20" height="15" fill="#FF6B6B" stroke="#D32F2F" stroke-width="1"/>
    <text x="635" y="227" font-family="Arial" font-size="12" fill="#2E7D32">龋齿</text>
  </g>
</svg>'''
    
    return svg

# 生成病因分析
def generate_cause_analysis(result_data):
    """生成病因分析"""
    analysis = {
        'tooth_abrasion': {
            'count': 0,
            'teeth': [],
            'causes': [
                '刷牙方式不当（横向刷牙、用力过猛）',
                '使用硬毛牙刷或磨料过多的牙膏',
                '饮食习惯（酸性食物、硬质食物）',
                '夜磨牙或紧咬牙习惯',
                '年龄因素导致的生理性磨损'
            ]
        },
        'general_caries': {
            'count': 0,
            'teeth': [],
            'causes': [
                '口腔卫生不良，牙菌斑堆积',
                '高糖饮食，频繁摄入含糖食物',
                '唾液分泌不足，口腔自洁能力下降',
                '牙齿结构缺陷或发育不良',
                '缺乏定期口腔检查和预防性治疗'
            ]
        },
        'twisted_tooth': {
            'count': 0,
            'teeth': [],
            'causes': [
                '遗传因素，家族性牙齿排列异常',
                '乳牙早失或滞留导致恒牙萌出异常',
                '牙弓空间不足，牙齿拥挤',
                '不良口腔习惯（咬唇、吐舌等）',
                '颌骨发育异常'
            ]
        }
    }
    
    for tooth_data in result_data.get('diseased_teeth', []):
        tooth_num = tooth_data.get('tooth_fdi', '')
        diseases = tooth_data.get('diseases', [])
        
        for disease in diseases:
            label = disease.get('label', '')
            if label == 'tooth abrasion':
                analysis['tooth_abrasion']['count'] += 1
                if tooth_num not in analysis['tooth_abrasion']['teeth']:
                    analysis['tooth_abrasion']['teeth'].append(tooth_num)
            elif label == 'general_caries':
                analysis['general_caries']['count'] += 1
                if tooth_num not in analysis['general_caries']['teeth']:
                    analysis['general_caries']['teeth'].append(tooth_num)
            elif label == 'twisted tooth':
                analysis['twisted_tooth']['count'] += 1
                if tooth_num not in analysis['twisted_tooth']['teeth']:
                    analysis['twisted_tooth']['teeth'].append(tooth_num)
    
    return analysis

# 生成综合总结
def generate_comprehensive_summary(result_data, cause_analysis):
    """生成综合总结"""
    total_problem_teeth = len(result_data.get('diseased_teeth', []))
    total_diseases = sum(len(t.get('diseases', [])) for t in result_data.get('diseased_teeth', []))
    
    summary = f"""
    <div class="summary-section">
      <h3>📊 检测概况</h3>
      <p>本次检测共发现 <strong>{total_problem_teeth}</strong> 颗牙齿存在健康问题，共检测到 <strong>{total_diseases}</strong> 处病变。</p>
    </div>
    
    <div class="summary-section">
      <h3>🔍 主要问题分布</h3>
      <ul>
"""
    
    if cause_analysis['tooth_abrasion']['count'] > 0:
        summary += f"        <li><strong>牙齿磨损</strong>：影响 {len(cause_analysis['tooth_abrasion']['teeth'])} 颗牙齿（{', '.join(cause_analysis['tooth_abrasion']['teeth'])}号牙）</li>\n"
    
    if cause_analysis['general_caries']['count'] > 0:
        summary += f"        <li><strong>龋齿</strong>：影响 {len(cause_analysis['general_caries']['teeth'])} 颗牙齿（{', '.join(cause_analysis['general_caries']['teeth'])}号牙）</li>\n"
    
    if cause_analysis['twisted_tooth']['count'] > 0:
        summary += f"        <li><strong>牙齿扭转</strong>：影响 {len(cause_analysis['twisted_tooth']['teeth'])} 颗牙齿（{', '.join(cause_analysis['twisted_tooth']['teeth'])}号牙）</li>\n"
    
    summary += """      </ul>
    </div>
    
    <div class="summary-section">
      <h3>💡 健康建议</h3>
      <ul>
        <li>建议尽快到专业口腔医疗机构进行详细检查和治疗</li>
        <li>改善口腔卫生习惯，使用正确的刷牙方法</li>
        <li>定期进行口腔检查和清洁（建议每6个月一次）</li>
        <li>注意饮食健康，减少高糖食物摄入</li>
        <li>如有夜磨牙习惯，建议佩戴防护牙套</li>
      </ul>
    </div>
"""
    
    return summary

if __name__ == '__main__':
    # 读取logo
    base_dir = Path(__file__).parent.parent.parent
    logo1_path = base_dir / '商标' / 'd36e30836df4c84348b7eda21da5b003.png'
    logo2_path = base_dir / '商标' / '2170b51c9ac9a84ceef03a49c3de8690.png'
    
    logo1_base64 = image_to_base64(logo1_path)
    logo2_base64 = image_to_base64(logo2_path)
    
    print(f"Logo1 loaded: {logo1_base64 is not None}")
    print(f"Logo2 loaded: {logo2_base64 is not None}")
    
    # 读取result.json
    result_data = load_result_json()
    
    # 生成牙齿图表SVG
    tooth_chart_svg = generate_tooth_chart_svg(result_data)
    
    # 生成病因分析
    cause_analysis = generate_cause_analysis(result_data)
    
    # 生成综合总结
    comprehensive_summary = generate_comprehensive_summary(result_data, cause_analysis)
    
    print("数据准备完成！")


