# MCP Fast Feedback v2.5.0

🚀 **高效的 MCP 交互式反馈工具 - 混合架构版本**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![PySide6](https://img.shields.io/badge/PySide6-6.8+-green.svg)](https://pypi.org/project/PySide6/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-2.5.0-red.svg)](https://github.com/kedaya2025/mcp_fast_feedback)

## 🎯 **项目简介**

MCP Fast Feedback 是一个增强版的 MCP (Model Context Protocol) 交互式反馈工具，专为 AI 辅助开发场景设计。本项目基于 [mcp-feedback-enhanced](https://github.com/Minidoracat/mcp-feedback-enhanced) 进行深度改进，实现了**混合架构**设计，支持 GUI 和 Web UI 双模式智能切换。

### 🌟 **核心特性**

- 🖥️ **混合架构** - 智能选择 GUI 或 Web UI 界面
- 🧠 **智能环境检测** - 自动识别本地、远程、WSL 等环境
- 🔄 **无缝降级机制** - GUI 不可用时自动切换到 Web UI
- 🌏 **完整中文支持** - 繁体中文、简体中文、英文多语言
- 📱 **响应式设计** - 适配不同屏幕尺寸和窗口大小
- ⚡ **高性能** - 异步处理，流畅的用户体验
- 🎨 **现代化界面** - 深色主题，美观易用

### 🆚 **版本对比**

| 特性 | v2.3.0 (GUI) | v2.4.2 (Web) | **v2.5.0 (混合)** |
|------|-------------|-------------|-----------------|
| GUI 界面 | ✅ | ❌ | ✅ |
| Web UI | ❌ | ✅ | ✅ |
| 智能选择 | ❌ | ❌ | ✅ |
| 环境检测 | ❌ | 部分 | ✅ |
| 降级机制 | ❌ | ❌ | ✅ |
| 中文支持 | ✅ | ✅ | ✅ |
| 响应式布局 | 部分 | ✅ | ✅ |

## 🚀 **快速开始**

### 📋 **系统要求**

- Python 3.11+
- Windows 10/11, macOS 10.15+, Linux (Ubuntu 20.04+)
- 支持 GUI 的桌面环境（可选）

### 🔧 **安装方法**

#### 方法一：使用 uv (推荐)
```bash
# 克隆仓库
git clone https://github.com/kedaya2025/mcp_fast_feedback.git
cd mcp_fast_feedback

# 安装依赖
uv sync

# 运行测试
uv run mcp-fast-feedback test --hybrid
```

#### 方法二：使用 pip
```bash
git clone https://github.com/kedaya2025/mcp_fast_feedback.git
cd mcp_fast_feedback
pip install -e .
```

### ⚙️ **MCP 配置**

在您的 MCP 配置文件中添加：

```json
{
  "mcpServers": {
    "mcp-fast-feedback": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/path/to/mcp_fast_feedback",
        "mcp-fast-feedback"
      ],
      "timeout": 600,
      "autoApprove": ["interactive_feedback"],
      "env": {
        "MCP_UI_MODE": "auto",
        "MCP_DEBUG": "false"
      }
    }
  }
}
```

## 🎛️ **配置选项**

### 环境变量

| 变量名 | 可选值 | 默认值 | 说明 |
|--------|--------|--------|------|
| `MCP_UI_MODE` | `auto`, `gui`, `web` | `auto` | 界面模式选择 |
| `MCP_FORCE_UI_MODE` | `gui`, `web` | - | 强制指定模式（无降级） |
| `MCP_DEBUG` | `true`, `false` | `false` | 调试模式 |
| `MCP_WEB_PORT` | 端口号 | `8080` | Web UI 端口 |

### 智能模式选择逻辑

- **本地环境** + GUI 可用 → GUI 模式
- **本地环境** + GUI 不可用 → Web UI 模式
- **远程环境** (SSH/容器) → Web UI 模式
- **WSL 环境** → 根据 GUI 可用性选择

## 🧪 **功能测试**

```bash
# 测试混合架构
uv run mcp-fast-feedback test --hybrid

# 测试 GUI 界面
uv run mcp-fast-feedback test --gui

# 测试 Web UI
uv run mcp-fast-feedback test --web

# 查看版本信息
uv run mcp-fast-feedback version

# 查看环境信息
uv run mcp-fast-feedback info
```

## 📸 **界面预览**

### GUI 界面
- 🖥️ 原生桌面应用体验
- 📋 多标签页设计
- ⚙️ 左右分栏设置页面
- 🎨 深色主题界面

### Web UI 界面
- 🌐 现代化 Web 界面
- 📱 响应式设计
- ⚡ 实时通信
- 🔧 丰富的功能选项

## 🛠️ **开发指南**

### 项目结构
```
mcp_fast_feedback/
├── src/mcp_feedback_enhanced/
│   ├── gui/                 # GUI 界面模块
│   ├── web/                 # Web UI 模块
│   ├── mode_selector.py     # 智能模式选择器
│   ├── launcher.py          # 统一启动器
│   ├── models.py           # 统一数据模型
│   └── server.py           # MCP 服务器
├── tests/                  # 测试文件
├── docs/                   # 文档
└── pyproject.toml         # 项目配置
```

### 本地开发
```bash
# 开发模式安装
uv sync --dev

# 运行测试
uv run pytest

# 代码格式化
uv run black src/
uv run isort src/

# 类型检查
uv run mypy src/
```

## 🤝 **致谢**

本项目基于 [mcp-feedback-enhanced](https://github.com/Minidoracat/mcp-feedback-enhanced) 进行改进开发，感谢原作者 **Minidoracat** 的优秀工作和开源贡献。

### 原项目特性
- 完整的 GUI 界面实现
- 多语言国际化支持
- 现代化的 Web UI 设计
- 丰富的配置选项

### 本项目改进
- 🔄 **混合架构设计** - 智能选择最适合的界面模式
- 🧠 **智能环境检测** - 自动识别运行环境类型
- 🛡️ **降级机制** - 确保在任何环境下都能正常工作
- 📐 **布局优化** - 改进设置页面为左右布局，防止重叠
- 🌏 **本地化修复** - 修复中文显示问题

## 📄 **许可证**

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🔗 **相关链接**

- 🏠 **项目主页**: https://github.com/kedaya2025/mcp_fast_feedback
- 📚 **原项目**: https://github.com/Minidoracat/mcp-feedback-enhanced
- 🐛 **问题反馈**: https://github.com/kedaya2025/mcp_fast_feedback/issues
- 💡 **功能建议**: https://github.com/kedaya2025/mcp_fast_feedback/discussions

## 📊 **版本历史**

- **v2.5.0** (2024-12) - 混合架构版本，智能模式选择
- **v2.4.2** - Web UI 增强版本 (基于原项目)
- **v2.3.0** - GUI 界面版本 (基于原项目)

---

⭐ **如果这个项目对您有帮助，请给我们一个 Star！**