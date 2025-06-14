# 🚀 MCP Fast Feedback v2.5.0 简易安装指南

## 🎯 **问题解决**

原配置的问题：
- ❌ 硬编码用户路径
- ❌ 配置复杂
- ❌ 不便分享

## ✅ **推荐安装方案**

### **方案一：uv 工具安装 (最简单)**

```bash
# 1. 安装为全局工具
uv tool install git+https://github.com/kedaya2025/mcp_fast_feedback.git

# 2. MCP 配置 (超简单)
{
  "command": "mcp-fast-feedback",
  "timeout": 600,
  "autoApprove": ["interactive_feedback"],
  "env": {
    "MCP_UI_MODE": "auto"
  }
}
```

### **方案二：本地安装 (推荐)**

```bash
# 1. 安装到用户目录
git clone https://github.com/kedaya2025/mcp_fast_feedback.git ~/.mcp/mcp-fast-feedback
cd ~/.mcp/mcp-fast-feedback
uv sync

# 2. MCP 配置 (通用路径)
{
  "command": "uv",
  "args": [
    "run",
    "--directory",
    "~/.mcp/mcp-fast-feedback",
    "mcp-fast-feedback"
  ],
  "timeout": 600,
  "autoApprove": ["interactive_feedback"],
  "env": {
    "MCP_UI_MODE": "auto"
  }
}
```

### **方案三：Windows 一键安装**

```powershell
# 1. 运行安装脚本
irm https://raw.githubusercontent.com/kedaya2025/mcp_fast_feedback/main/install-global.ps1 | iex

# 2. 复制生成的 MCP 配置
# 脚本会自动生成适合您系统的配置
```

## 🎯 **最佳实践配置**

### **通用 MCP 配置模板**

```json
{
  "command": "uv",
  "args": [
    "run",
    "--directory",
    "%USERPROFILE%\\.mcp\\mcp-fast-feedback",
    "mcp-fast-feedback"
  ],
  "timeout": 600,
  "autoApprove": ["interactive_feedback"],
  "env": {
    "MCP_UI_MODE": "auto",
    "MCP_DEBUG": "false"
  }
}
```

### **环境变量说明**

| 变量 | 值 | 说明 |
|------|----|----|
| `MCP_UI_MODE` | `auto` | 智能选择界面模式 |
| `MCP_UI_MODE` | `gui` | 强制 GUI 模式 |
| `MCP_UI_MODE` | `web` | 强制 Web UI 模式 |
| `MCP_DEBUG` | `true/false` | 调试模式开关 |

## 🔧 **安装验证**

```bash
# 测试安装
mcp-fast-feedback version

# 测试混合架构
mcp-fast-feedback test --hybrid

# 查看环境信息
mcp-fast-feedback info
```

## 📋 **故障排除**

### **常见问题**

1. **路径问题**
   - 使用 `~` 或 `%USERPROFILE%` 代替硬编码路径
   - 确保路径中没有空格或特殊字符

2. **权限问题**
   - 确保安装目录有写权限
   - Windows 用户可能需要管理员权限

3. **依赖问题**
   - 确保 Python 3.11+ 已安装
   - 确保 uv 包管理器已安装

### **支持平台**

- ✅ Windows 10/11
- ✅ macOS 10.15+
- ✅ Linux (Ubuntu 20.04+)
- ✅ WSL 环境
- ✅ SSH 远程环境

## 🎊 **安装完成后**

1. **添加到 MCP 客户端**
2. **测试功能**
3. **享受智能界面选择**
4. **体验混合架构优势**

---

**推荐**: 使用方案一 (uv tool install) 获得最简单的安装体验！
