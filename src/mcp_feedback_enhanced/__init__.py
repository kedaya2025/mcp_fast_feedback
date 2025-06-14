#!/usr/bin/env python3
"""
MCP Interactive Feedback Enhanced
==================================

互動式用戶回饋 MCP 伺服器，提供 AI 輔助開發中的回饋收集功能。

作者: Fábio Ferreira
增強功能: 混合架構支援、GUI + Web UI 雙模式、智能環境檢測

特色：
- 🖥️ GUI 桌面介面支援 (PySide6)
- 🌐 Web UI 介面支援
- 🧠 智慧環境檢測與模式選擇
- 📝 智能提示詞管理系統
- ⏰ 自動定時提交功能
- 📊 會話管理與追踪
- 🖼️ 圖片上傳支援
- 🌏 多語言支援
- 🔧 命令執行功能
- 🎨 現代化界面設計
- 🏗️ 模組化架構
"""

__version__ = "2.5.0"
__author__ = "Minidoracat"
__email__ = "minidora0702@gmail.com"

import os

from .server import main as run_server

# 導入 Web UI 模組
from .web import WebUIManager, get_web_ui_manager, launch_web_feedback_ui, stop_web_ui

# 嘗試導入 GUI 模組（可選依賴）
try:
    from .gui import feedback_ui as gui_feedback_ui
    GUI_AVAILABLE = True
except ImportError:
    gui_feedback_ui = None
    GUI_AVAILABLE = False

# 保持向後兼容性
feedback_ui = gui_feedback_ui

# 主要導出介面
__all__ = [
    "WebUIManager",
    "__author__",
    "__version__",
    "feedback_ui",
    "gui_feedback_ui",
    "get_web_ui_manager",
    "launch_web_feedback_ui",
    "run_server",
    "stop_web_ui",
    "GUI_AVAILABLE",
]


def main():
    """主要入口點，用於 uvx 執行"""
    from .__main__ import main as cli_main

    return cli_main()
