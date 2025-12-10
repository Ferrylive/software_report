# GitHub Pages 部署详细指南

## 📋 前置准备

- ✅ GitHub账号（如果没有，访问 https://github.com 注册）
- ✅ 准备好 `version3` 文件夹中的所有文件

---

## 🚀 完整操作流程

### 步骤1：创建GitHub仓库

1. **登录GitHub**
   - 访问 https://github.com
   - 使用你的账号登录

2. **创建新仓库**
   - 点击右上角的 **"+"** 按钮
   - 选择 **"New repository"**

3. **填写仓库信息**
   ```
   Repository name: dental-report
   Description: 口腔健康评估报告（可选）
   Visibility: ⚪ Public（必须选择Public，免费版GitHub Pages只支持公开仓库）
   ⬜ Add a README file（不要勾选）
   ⬜ Add .gitignore（可选）
   ⬜ Choose a license（可选）
   ```

4. **创建仓库**
   - 点击绿色的 **"Create repository"** 按钮

---

### 步骤2：上传文件

#### 方法A：网页上传（推荐，最简单）

1. **进入上传页面**
   - 创建仓库后，你会看到一个快速设置页面
   - 找到并点击 **"uploading an existing file"** 链接
   - 或者直接访问：`https://github.com/YOUR_USERNAME/dental-report/upload`

2. **上传文件**
   - **方式1：拖拽上传**
     - 打开文件管理器，找到 `version3` 文件夹
     - 将文件夹中的所有文件和文件夹拖拽到GitHub页面上
   
   - **方式2：点击选择**
     - 点击 **"choose your files"** 按钮
     - 选择 `version3` 文件夹中的所有文件
     - ⚠️ **注意**：需要选择所有文件，包括：
       - `report.html`
       - `result.json`
       - `images` 文件夹（整个文件夹）
       - 其他所有文件

3. **提交文件**
   - 滚动到页面底部
   - 在 **"Commit changes"** 部分：
     - **Commit message**：输入 `Initial commit - 上传报告文件`
   - 点击绿色的 **"Commit changes"** 按钮

4. **等待上传完成**
   - 上传大文件可能需要几分钟
   - 上传完成后，你会看到所有文件都在仓库中

#### 方法B：使用Git命令行（适合有经验的用户）

```bash
# 1. 打开命令行，进入version3文件夹
cd d:\D0_com\workplaceplus\C1_software_report\version3

# 2. 初始化Git仓库
git init

# 3. 添加所有文件
git add .

# 4. 提交文件
git commit -m "Initial commit - 上传报告文件"

# 5. 添加远程仓库（替换YOUR_USERNAME为你的GitHub用户名）
git remote add origin https://github.com/YOUR_USERNAME/dental-report.git

# 6. 推送到GitHub
git branch -M main
git push -u origin main
```

---

### 步骤3：启用GitHub Pages

1. **进入设置页面**
   - 在仓库页面，点击顶部的 **"Settings"** 标签
   - 如果没有看到Settings，检查仓库是否是Public（私有仓库需要付费版才能使用GitHub Pages）

2. **找到Pages设置**
   - 在左侧菜单中，向下滚动找到 **"Pages"** 选项
   - 点击 **"Pages"**

3. **配置Pages**
   - 在 **"Source"**（源）部分：
     - 选择 **"Deploy from a branch"**
     - **Branch**：选择 `main`（或 `master`，取决于你的默认分支）
     - **Folder**：选择 `/ (root)`（根目录）
   - 点击 **"Save"** 按钮

4. **等待部署**
   - GitHub会显示：`Your site is ready to be published at...`
   - 等待1-2分钟让GitHub完成部署

---

### 步骤4：访问你的网站

1. **获取网站地址**
   - 在Pages设置页面，你会看到：
     ```
     Your site is live at https://YOUR_USERNAME.github.io/dental-report/
     ```
   - 或者格式为：`https://YOUR_USERNAME.github.io/dental-report/`

2. **访问报告**
   - 由于主文件是 `report.html`，你需要访问：
     ```
     https://YOUR_USERNAME.github.io/dental-report/report.html
     ```
   - 或者创建 `index.html` 重定向（见步骤5）

---

### 步骤5：设置默认页面（可选，推荐）

如果你希望直接访问 `https://YOUR_USERNAME.github.io/dental-report/` 就能看到报告：

1. **创建index.html**
   - 在仓库页面，点击 **"Add file"** > **"Create new file"**
   - 文件名输入：`index.html`

2. **添加重定向代码**
   - 在文件内容中输入：
   ```html
   <!DOCTYPE html>
   <html lang="zh-CN">
   <head>
       <meta charset="UTF-8">
       <meta http-equiv="refresh" content="0; url=report.html">
       <title>口腔健康评估报告</title>
   </head>
   <body>
       <p>正在跳转到报告页面...</p>
       <script>
           window.location.href = 'report.html';
       </script>
   </body>
   </html>
   ```

3. **提交文件**
   - 滚动到底部
   - **Commit message**：输入 `添加index.html重定向`
   - 点击 **"Commit new file"**

4. **测试**
   - 现在可以直接访问：`https://YOUR_USERNAME.github.io/dental-report/`
   - 会自动跳转到报告页面

---

### 步骤6：手机测试

1. **在手机上打开浏览器**
   - 使用任何浏览器（Chrome、Safari、Edge等）

2. **访问网站**
   - 输入完整URL：`https://YOUR_USERNAME.github.io/dental-report/report.html`
   - 或者如果创建了index.html：`https://YOUR_USERNAME.github.io/dental-report/`

3. **测试功能**
   - ✅ 查看报告内容
   - ✅ 点击牙齿查看详情
   - ✅ 测试滑动和交互功能
   - ✅ 检查图片是否正常显示

---

## 🔧 常见问题解决

### Q1: 上传后网站显示404错误？

**解决方法：**
1. 检查文件是否都上传成功（在仓库页面查看）
2. 确保访问的是完整路径：`/dental-report/report.html`
3. 等待5-10分钟让GitHub Pages完成部署
4. 检查仓库设置中的Pages配置是否正确

### Q2: 图片无法显示？

**解决方法：**
1. 检查 `images` 文件夹是否完整上传
2. 在仓库中点击 `images` 文件夹，确认所有子文件夹都在
3. 检查图片路径（代码中已经是相对路径，应该没问题）
4. 清除浏览器缓存后重试

### Q3: 如何更新文件？

**方法1：网页更新**
1. 在仓库页面点击要更新的文件
2. 点击右上角的编辑按钮（铅笔图标）
3. 修改内容后，点击 "Commit changes"

**方法2：重新上传**
1. 删除旧文件（点击文件，然后点击删除按钮）
2. 按照步骤2重新上传新文件

**方法3：使用Git命令行**
```bash
git add .
git commit -m "更新文件"
git push
```

### Q4: 网站更新后没有变化？

**解决方法：**
1. 等待几分钟（GitHub Pages需要时间更新）
2. 清除浏览器缓存
3. 使用无痕模式打开网站
4. 在URL后添加参数：`?v=2` 强制刷新

### Q5: 如何查看部署状态？

1. 在仓库页面，点击 **"Actions"** 标签
2. 可以看到GitHub Pages的部署状态
3. 如果有错误，会在这里显示

---

## 📝 重要提示

1. **仓库必须是Public**：免费版GitHub Pages只支持公开仓库
2. **文件大小限制**：单个文件不超过100MB，仓库不超过1GB
3. **更新延迟**：文件更新后，网站可能需要几分钟才能看到变化
4. **HTTPS自动启用**：GitHub Pages自动提供HTTPS加密

---

## ✅ 检查清单

部署完成后，确认以下项目：

- [ ] 所有文件都已上传到仓库
- [ ] `images` 文件夹完整上传
- [ ] GitHub Pages已启用
- [ ] 网站可以正常访问
- [ ] 报告内容正常显示
- [ ] 图片可以正常显示
- [ ] 手机端可以正常访问和操作

---

## 🎉 完成！

现在你的报告已经部署到GitHub Pages了！

**网站地址**：`https://YOUR_USERNAME.github.io/dental-report/report.html`

可以在任何设备上访问和测试！

