@echo off
cd /d "%~dp0.."
echo ==========================================
echo 正在启动本地服务器...
echo 当前目录: %CD%
echo ==========================================
echo.
echo 本地访问地址:
echo   http://localhost:8000/report.html
echo.
echo 手机访问地址（需要替换为您的实际IP）:
echo   http://[您的IP]:8000/report.html
echo.
echo 提示：
echo - 图片文件应该在 images/ 文件夹中
echo - result.json 文件应该在当前目录
echo - 按 Ctrl+C 停止服务器
echo ==========================================
echo.
python -m http.server 8000
