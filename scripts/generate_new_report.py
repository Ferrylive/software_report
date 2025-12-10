#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""生成新的HTML报告"""

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
    problem_teeth = set()
    
    for tooth_data in result_data.get('diseased_teeth', []):
        tooth_num = tooth_data.get('tooth_fdi', '')
        if tooth_num:
            problem_teeth.add(tooth_num)
    
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
'''
    
    # 上颌牙齿位置 (1-16, 从右上到左上)
    upper_positions = [
        ('1', 50, 80), ('2', 90, 80), ('3', 130, 80),
        ('4', 170, 70), ('5', 200, 70),
        ('6', 230, 60),
        ('7', 255, 50), ('8', 275, 45),
        ('9', 295, 45), ('10', 315, 50),
        ('11', 340, 60),
        ('12', 370, 70), ('13', 400, 70),
        ('14', 440, 80), ('15', 480, 80), ('16', 520, 80),
    ]
    
    for tooth_num, x, y in upper_positions:
        is_problem = tooth_num in problem_teeth
        tooth_class = 'tooth-problem' if is_problem else 'tooth-normal'
        text_class = 'tooth-problem-text' if is_problem else 'tooth-text'
        w, h = (30, 25) if int(tooth_num) in [1,2,3,14,15,16] else (25, 20) if int(tooth_num) in [4,5,12,13] else (20, 18) if int(tooth_num) in [6,11] else (18, 15) if int(tooth_num) in [7,10] else (15, 12)
        
        svg += f'    <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" class="{tooth_class}"/>\n'
        svg += f'    <text x="{x+w/2}" y="{y+h/2+5}" text-anchor="middle" class="{text_class}">{tooth_num}</text>\n'
    
    svg += '''  </g>
  
  <!-- 下颌 -->
  <g id="lower-arch">
    <text x="400" y="350" text-anchor="middle" class="arch-label">下颌 (Mandibular)</text>
'''
    
    # 下颌牙齿位置 (17-32, 从左下到右下)
    lower_positions = [
        ('17', 50, 400), ('18', 90, 400), ('19', 130, 400),
        ('20', 170, 410), ('21', 200, 410),
        ('22', 230, 420),
        ('23', 255, 430), ('24', 275, 435),
        ('25', 295, 435), ('26', 315, 430),
        ('27', 340, 420),
        ('28', 370, 410), ('29', 400, 410),
        ('30', 440, 400), ('31', 480, 400), ('32', 520, 400),
    ]
    
    for tooth_num, x, y in lower_positions:
        is_problem = tooth_num in problem_teeth
        tooth_class = 'tooth-problem' if is_problem else 'tooth-normal'
        text_class = 'tooth-problem-text' if is_problem else 'tooth-text'
        w, h = (30, 25) if int(tooth_num) in [17,18,19,30,31,32] else (25, 20) if int(tooth_num) in [20,21,28,29] else (20, 18) if int(tooth_num) in [22,27] else (18, 15) if int(tooth_num) in [23,26] else (15, 12)
        
        svg += f'    <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" class="{tooth_class}"/>\n'
        svg += f'    <text x="{x+w/2}" y="{y+h/2+5}" text-anchor="middle" class="{text_class}">{tooth_num}</text>\n'
    
    svg += '''  </g>
  
  <!-- 图例 -->
  <g id="legend">
    <rect x="600" y="100" width="180" height="120" fill="#F5F5F5" stroke="#4CAF50" stroke-width="2" rx="5"/>
    <text x="690" y="125" text-anchor="middle" font-family="Arial" font-size="14" font-weight="bold" fill="#2E7D32">图例</text>
    <rect x="610" y="140" width="20" height="15" fill="#E8F5E9" stroke="#4CAF50" stroke-width="1"/>
    <text x="635" y="152" font-family="Arial" font-size="12" fill="#2E7D32">正常</text>
    <rect x="610" y="165" width="20" height="15" fill="#FFF9C4" stroke="#FBC02D" stroke-width="2"/>
    <text x="635" y="177" font-family="Arial" font-size="12" fill="#F57F17">有问题</text>
  </g>
</svg>'''
    
    return svg

# 生成病因分析HTML
def generate_cause_analysis_html(result_data):
    """生成病因分析HTML"""
    analysis = {
        'tooth_abrasion': {'count': 0, 'teeth': set()},
        'general_caries': {'count': 0, 'teeth': set()},
        'twisted_tooth': {'count': 0, 'teeth': set()}
    }
    
    disease_names = {
        'tooth abrasion': '牙齿磨损',
        'general_caries': '龋齿',
        'twisted tooth': '牙齿扭转'
    }
    
    disease_causes = {
        'tooth abrasion': [
            '刷牙方式不当（横向刷牙、用力过猛）',
            '使用硬毛牙刷或磨料过多的牙膏',
            '饮食习惯（酸性食物、硬质食物）',
            '夜磨牙或紧咬牙习惯',
            '年龄因素导致的生理性磨损'
        ],
        'general_caries': [
            '口腔卫生不良，牙菌斑堆积',
            '高糖饮食，频繁摄入含糖食物',
            '唾液分泌不足，口腔自洁能力下降',
            '牙齿结构缺陷或发育不良',
            '缺乏定期口腔检查和预防性治疗'
        ],
        'twisted tooth': [
            '遗传因素，家族性牙齿排列异常',
            '乳牙早失或滞留导致恒牙萌出异常',
            '牙弓空间不足，牙齿拥挤',
            '不良口腔习惯（咬唇、吐舌等）',
            '颌骨发育异常'
        ]
    }
    
    for tooth_data in result_data.get('diseased_teeth', []):
        tooth_num = tooth_data.get('tooth_fdi', '')
        diseases = tooth_data.get('diseases', [])
        
        for disease in diseases:
            label = disease.get('label', '')
            if label in analysis:
                analysis[label]['count'] += 1
                analysis[label]['teeth'].add(tooth_num)
    
    html = '<div class="section"><h3>🔬 病因分析</h3>'
    
    for disease_key, disease_name in disease_names.items():
        if analysis[disease_key]['count'] > 0:
            teeth_list = sorted(list(analysis[disease_key]['teeth']), key=lambda x: int(x))
            html += f'''
      <div style="margin-bottom: 20px; padding: 15px; background: #F9FBE7; border-left: 4px solid #8BC34A; border-radius: 5px;">
        <h4 style="margin: 0 0 10px 0; color: #558B2F; font-size: 18px;">{disease_name}</h4>
        <p style="margin: 5px 0; color: #555;"><strong>涉及牙齿：</strong>{', '.join(teeth_list)}号牙</p>
        <p style="margin: 5px 0; color: #555;"><strong>可能原因：</strong></p>
        <ul style="margin: 10px 0; padding-left: 20px; color: #666;">
'''
            for cause in disease_causes[disease_key]:
                html += f'          <li>{cause}</li>\n'
            html += '        </ul>\n      </div>\n'
    
    html += '</div>'
    return html

# 生成综合总结HTML
def generate_summary_html(result_data):
    """生成综合总结HTML"""
    total_problem_teeth = len(result_data.get('diseased_teeth', []))
    total_diseases = sum(len(t.get('diseases', [])) for t in result_data.get('diseased_teeth', []))
    
    disease_counts = {}
    for tooth_data in result_data.get('diseased_teeth', []):
        for disease in tooth_data.get('diseases', []):
            label = disease.get('label', '')
            disease_counts[label] = disease_counts.get(label, 0) + 1
    
    disease_names = {
        'tooth abrasion': '牙齿磨损',
        'general_caries': '龋齿',
        'twisted tooth': '牙齿扭转'
    }
    
    html = f'''
    <div class="section">
      <h3>📊 检测概况</h3>
      <p>本次检测共发现 <strong style="color: #FBC02D;">{total_problem_teeth}</strong> 颗牙齿存在健康问题，共检测到 <strong style="color: #FBC02D;">{total_diseases}</strong> 处病变。</p>
    </div>
    
    <div class="section">
      <h3>🔍 主要问题分布</h3>
      <ul style="line-height: 2;">
'''
    
    for label, count in disease_counts.items():
        name = disease_names.get(label, label)
        html += f'        <li><strong>{name}</strong>：{count} 处</li>\n'
    
    html += '''      </ul>
    </div>
    
    <div class="section">
      <h3>💡 健康建议</h3>
      <ul style="line-height: 2;">
        <li>建议尽快到专业口腔医疗机构进行详细检查和治疗</li>
        <li>改善口腔卫生习惯，使用正确的刷牙方法（建议使用巴氏刷牙法）</li>
        <li>定期进行口腔检查和清洁（建议每6个月一次）</li>
        <li>注意饮食健康，减少高糖食物和酸性饮料的摄入</li>
        <li>如有夜磨牙习惯，建议佩戴防护牙套</li>
        <li>使用含氟牙膏，增强牙齿抗龋能力</li>
      </ul>
    </div>
'''
    
    return html

# 读取原始照片并转换为base64
def image_file_to_base64_data_uri(image_path):
    """将图片文件转换为base64 data URI"""
    if not os.path.exists(image_path):
        return None
    ext = os.path.splitext(image_path)[1].lower()
    mime_types = {'.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg'}
    mime_type = mime_types.get(ext, 'image/png')
    
    with open(image_path, 'rb') as f:
        img_data = f.read()
        base64_str = base64.b64encode(img_data).decode('utf-8')
        return f"data:{mime_type};base64,{base64_str}"

# 生成完整HTML报告
def generate_html_report():
    """生成完整的HTML报告"""
    # 获取脚本所在目录的父目录的父目录（即D0_com目录）
    script_dir = Path(__file__).resolve().parent
    base_dir = script_dir.parent.parent
    logo1_path = base_dir / '商标' / 'd36e30836df4c84348b7eda21da5b003.png'
    logo2_path = base_dir / '商标' / '2170b51c9ac9a84ceef03a49c3de8690.png'
    
    logo1_base64 = image_to_base64(str(logo1_path))
    logo2_base64 = image_to_base64(str(logo2_path))
    
    result_data = load_result_json()
    
    # 读取图片
    overview_path = script_dir / '原始照片_overview.png'
    overview_data_uri = image_file_to_base64_data_uri(str(overview_path))
    
    # 生成牙齿图表
    tooth_chart_svg = generate_tooth_chart_svg(result_data)
    
    # 生成病因分析
    cause_analysis_html = generate_cause_analysis_html(result_data)
    
    # 生成总结
    summary_html = generate_summary_html(result_data)
    
    # 生成封面总结信息
    total_problem_teeth = len(result_data.get('diseased_teeth', []))
    total_diseases = sum(len(t.get('diseases', [])) for t in result_data.get('diseased_teeth', []))
    
    # 构建HTML
    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1"> 
  <title>口腔健康评估报告</title>
  <style>
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'PingFang SC', 'Microsoft YaHei', 'Helvetica Neue', Arial, 'Noto Sans SC', sans-serif; background:#ffffff; color:#222; }}
    .page {{ width: 100%; max-width: 1080px; margin: 24px auto 72px; background:#ffffff; padding: 28px 32px 40px; border-radius: 12px; box-shadow: 0 12px 36px rgba(0,0,0,.08);}} 
    .topbar {{ height: 10px; background: linear-gradient(90deg, #4CAF50 0%, #8BC34A 50%, #FFEB3B 100%); width: 50%; border-radius: 6px; margin-top: 4px; }}
    .header {{ display:flex; align-items: center; justify-content: space-between; margin: 18px 0 12px; }}
    .badge {{ display:inline-block; padding: 6px 12px; border-radius: 8px; background: linear-gradient(135deg, #4CAF50 0%, #8BC34A 100%); color:#fff; font-weight:600; margin-right: 12px; }}
    h1 {{ margin: 0; font-size: 48px; letter-spacing:1px; color: #2E7D32; }}
    .report-tag {{ color:#4CAF50; }}
    .logo {{ height: 80px; width: auto; display:block; object-fit: contain; }}
    .logo-large {{ height: 150px; width: auto; display:block; object-fit: contain; }}
    .cover {{ display:flex; flex-direction: column; align-items:center; justify-content:center; padding: 80px 32px 120px; text-align:center; background: linear-gradient(135deg, #E8F5E9 0%, #F1F8E9 50%, #FFF9C4 100%); border-radius: 12px; }}
    .cover h1 {{ font-size: 42px; margin: 18px 0 8px; color: #2E7D32; }}
    .cover .subtitle {{ color:#4CAF50; font-size: 18px; margin-top: 4px; }}
    .cover-summary {{ margin-top: 40px; padding: 30px; background: rgba(255,255,255,0.9); border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); max-width: 600px; }}
    .cover-summary h2 {{ color: #2E7D32; font-size: 24px; margin: 0 0 15px 0; }}
    .cover-summary .stat {{ display: flex; justify-content: space-around; margin: 20px 0; }}
    .cover-summary .stat-item {{ text-align: center; }}
    .cover-summary .stat-number {{ font-size: 36px; font-weight: bold; color: #FBC02D; margin: 5px 0; }}
    .cover-summary .stat-label {{ font-size: 14px; color: #666; }}
    .layout {{ display:grid; grid-template-columns: 1fr 460px; gap: 28px; margin-top: 10px; }}
    @media (max-width: 980px){{ .layout {{ grid-template-columns: 1fr; }} }}
    .section {{ margin-bottom: 18px; background:#ffffff; border:1px solid #C8E6C9; border-radius:10px; padding:14px 16px; }}
    .section h3 {{ margin: 0 0 6px; color:#2E7D32; font-size: 20px; display:flex; align-items:center; }}
    .section h3::before {{ content:""; display:inline-block; width: 12px; height: 12px; border:2px solid #4CAF50; border-radius:50%; margin-right: 8px; }}
    .section p {{ margin: 0; line-height: 1.8; color:#444; }}
    .right h3 {{ color:#4CAF50; margin: 6px 0; font-size: 20px; }}
    .chips {{ display:flex; flex-wrap:wrap; gap: 8px 10px; margin: 6px 0 12px; }}
    .chip {{ background: linear-gradient(135deg, #4CAF50 0%, #8BC34A 100%); color:#fff; border-radius: 999px; padding: 6px 12px; font-weight: 700; min-width: 42px; text-align:center; font-size: 14px; }}
    .grid {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; }}
    @media (max-width: 980px){{ .grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }} }}
    .cell {{ background:#ffffff; padding: 8px; border:1px solid #C8E6C9; border-radius: 10px; }}
    .cell img {{ width: 100%; aspect-ratio: 1 / 1; object-fit: cover; border-radius: 8px; display:block; }}
    .meta {{ font-size: 13px; color:#555; margin-top: 6px; line-height: 1.55; }}
    footer {{ margin-top: 24px; color:#666; font-size: 14px; }}
    .legend {{ margin-top: 6px; font-size: 12px; color:#4CAF50; }}
    .score {{ color:#4CAF50; font-size: 28px; font-weight: 800; }}
    .tooth-chart {{ width: 100%; max-width: 800px; margin: 20px auto; background: #F9FBE7; padding: 20px; border-radius: 10px; border: 2px solid #8BC34A; }}
    .tooth-chart svg {{ width: 100%; height: auto; }}
    /* Print layout for consistent A4 pagination */
    @page {{ size: A4; margin: 12mm; }}
    @media print {{
      body {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; font-size: 12px; }}
      .page {{ break-after: page; page-break-after: always; box-shadow: none; max-width: 100%; margin: 0; border-radius: 0; page-break-inside: avoid; }}
      .header h1 {{ font-size: 28px; }}
      .badge {{ padding: 4px 10px; font-size: 12px; }}
      .section {{ margin-bottom: 10px; padding: 10px 12px; }}
      .section h3 {{ font-size: 16px; }}
      .section p {{ line-height: 1.6; }}
      .right h3 {{ font-size: 16px; }}
      .chips {{ gap: 6px 8px; }}
      .logo {{ height: 60px; }}
    }}
  </style>
</head>
<body>
  <!-- 封面 -->
  <div class="page cover">
    <img class="logo-large" src="data:image/png;base64,{logo2_base64 if logo2_base64 else ''}" alt="Logo">
    <h1>口腔健康评估报告</h1>
    <p class="subtitle">Oral Health Assessment Report</p>
    
    <div class="cover-summary">
      <h2>📋 检测概览</h2>
      <div class="stat">
        <div class="stat-item">
          <div class="stat-number">{total_problem_teeth}</div>
          <div class="stat-label">问题牙齿</div>
        </div>
        <div class="stat-item">
          <div class="stat-number">{total_diseases}</div>
          <div class="stat-label">病变数量</div>
        </div>
      </div>
      <p style="margin: 15px 0 0 0; color: #555; line-height: 1.6;">
        本报告基于AI智能分析技术，对您的口腔健康状况进行了全面评估。
        建议您根据报告结果，及时咨询专业口腔医生，制定个性化的治疗方案。
      </p>
    </div>
  </div>

  <!-- 报告内容 -->
  <div class="page">
    <div class="topbar"></div>
    <div class="header">
      <div>
        <span class="badge">AI智能分析</span>
        <h1>口腔健康<span class="report-tag">评估报告</span></h1>
      </div>
      <div><img class="logo" src="data:image/png;base64,{logo1_base64 if logo1_base64 else ''}" alt="Logo"></div>
    </div>
    
    <div class="layout">
      <div class="left">
        {summary_html}
        
        {cause_analysis_html}
        
        <div class="section">
          <h3>🦷 牙齿问题分布图</h3>
          <div class="tooth-chart">
            {tooth_chart_svg}
          </div>
          <p class="legend">注：黄色标记表示存在问题的牙齿</p>
        </div>
        
        <div class="section">
          <h3>📸 整体视图</h3>
          <img src="{overview_data_uri}" alt="整体视图" style="width: 100%; border-radius: 8px; border: 2px solid #C8E6C9;">
        </div>
      </div>
      
      <div class="right">
        <h3>🔍 详细检测结果</h3>
        <div class="chips">
'''
    
    # 添加问题牙齿标签
    problem_teeth_set = set()
    for tooth_data in result_data.get('diseased_teeth', []):
        tooth_num = tooth_data.get('tooth_fdi', '')
        if tooth_num:
            problem_teeth_set.add(tooth_num)
    
    for tooth_num in sorted(problem_teeth_set, key=lambda x: int(x)):
        html_content += f'          <span class="chip">{tooth_num}</span>\n'
    
    html_content += '''        </div>
        
        <div class="grid">
'''
    
    # 添加牙齿详细图片
    for tooth_data in result_data.get('diseased_teeth', []):
        tooth_num = tooth_data.get('tooth_fdi', '')
        diseases = tooth_data.get('diseases', [])
        square_crop_path = tooth_data.get('square_crop_path', '')
        
        if square_crop_path:
            # 转换路径
            img_path = script_dir / Path(square_crop_path).name
            img_data_uri = image_file_to_base64_data_uri(str(img_path))
            
            if img_data_uri:
                disease_labels = [d.get('label', '') for d in diseases]
                disease_names_map = {
                    'tooth abrasion': '磨损',
                    'general_caries': '龋齿',
                    'twisted tooth': '扭转'
                }
                disease_text = '、'.join([disease_names_map.get(l, l) for l in disease_labels if l in disease_names_map])
                
                html_content += f'''          <div class="cell">
            <img src="{img_data_uri}" alt="牙齿 {tooth_num}">
            <div class="meta">
              <strong>{tooth_num}号牙</strong><br>
              {disease_text}
            </div>
          </div>
'''
    
    html_content += '''        </div>
      </div>
    </div>
    
    <footer>
      <p>本报告由AI智能分析系统生成，仅供参考。具体诊断和治疗方案请咨询专业口腔医生。</p>
      <p style="margin-top: 10px; color: #4CAF50;">© 渡生科技 - 专业口腔健康解决方案</p>
    </footer>
  </div>
</body>
</html>'''
    
    # 保存HTML文件（覆盖原文件）
    output_path = script_dir / 'report.html'
    with open(str(output_path), 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"新报告已生成: {output_path}")
    return output_path

if __name__ == '__main__':
    generate_html_report()

