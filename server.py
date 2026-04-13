#!/usr/bin/env python3
"""
SBTI-Bench HTTP服务器
确保正确的UTF-8编码
"""

import http.server
import socketserver
import os
import json
from pathlib import Path

class UTF8HTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """自定义HTTP请求处理器，确保UTF-8编码"""

    def end_headers(self):
        # 添加UTF-8编码头
        self.send_header('Content-Type', f'{self.headers.get("Content-Type", "text/html")}; charset=utf-8')
        # 添加CORS支持（如果需要）
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def log_message(self, format, *args):
        # 改进日志输出
        print(f"[{self.log_date_time_string()}] {format % args}")

def start_server(port=8000):
    """启动HTTP服务器"""

    PORT = port
    DIRECTORY = os.path.dirname(os.path.abspath(__file__))

    os.chdir(DIRECTORY)

    # 检查数据文件
    data_file = Path("data/results.json")
    if data_file.exists():
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"✓ 找到数据文件: {data['total_evaluations']} 个评测结果")
        except Exception as e:
            print(f"⚠️ 数据文件读取错误: {e}")
    else:
        print("⚠️ 未找到数据文件 data/results.json")

    print(f"=" * 50)
    print(f"SBTI-Bench 前端服务器 (UTF-8)")
    print(f"=" * 50)
    print(f"项目目录: {DIRECTORY}")
    print(f"服务端口: {PORT}")
    print(f"")
    print(f"在浏览器中打开:")
    print(f"  http://localhost:{PORT}/frontend/index.html")
    print(f"")
    print(f"按 Ctrl+C 停止服务器")
    print(f"=" * 50)
    print(f"")

    with socketserver.TCPServer(("", PORT), UTF8HTTPRequestHandler) as httpd:
        httpd.allow_reuse_address = True
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n服务器已停止")

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    start_server(port)
