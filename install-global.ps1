# MCP Fast Feedback v2.5.0 全局安装脚本
# 创建用户友好的全局安装

param(
    [string]$InstallPath = "$env:USERPROFILE\.mcp\mcp-fast-feedback"
)

Write-Host "🚀 MCP Fast Feedback v2.5.0 全局安装" -ForegroundColor Green
Write-Host "安装路径: $InstallPath" -ForegroundColor Cyan

# 检查依赖
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "❌ 需要先安装 uv: https://docs.astral.sh/uv/" -ForegroundColor Red
    exit 1
}

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "❌ 需要先安装 Git: https://git-scm.com/" -ForegroundColor Red
    exit 1
}

# 创建安装目录
New-Item -ItemType Directory -Force -Path $InstallPath | Out-Null

# 克隆或更新仓库
if (Test-Path "$InstallPath\.git") {
    Write-Host "🔄 更新现有安装..." -ForegroundColor Yellow
    Set-Location $InstallPath
    git pull origin main
} else {
    Write-Host "📥 克隆仓库..." -ForegroundColor Cyan
    git clone https://github.com/kedaya2025/mcp_fast_feedback.git $InstallPath
    Set-Location $InstallPath
}

# 安装依赖
Write-Host "📦 安装依赖..." -ForegroundColor Cyan
uv sync

# 创建启动脚本
$LauncherScript = @"
@echo off
cd /d "$InstallPath"
uv run python -m mcp_feedback_enhanced %*
"@

$LauncherPath = "$InstallPath\mcp-fast-feedback.bat"
$LauncherScript | Out-File -FilePath $LauncherPath -Encoding ASCII

# 测试安装
Write-Host "🧪 测试安装..." -ForegroundColor Cyan
& $LauncherPath version

# 生成 MCP 配置
$McpConfig = @{
    command = $LauncherPath
    args = @()
    timeout = 600
    autoApprove = @("interactive_feedback")
    env = @{
        MCP_UI_MODE = "auto"
        MCP_DEBUG = "false"
    }
} | ConvertTo-Json -Depth 10

Write-Host ""
Write-Host "✅ 安装完成！" -ForegroundColor Green
Write-Host ""
Write-Host "📋 MCP 配置 (复制到您的 MCP 客户端):" -ForegroundColor Yellow
Write-Host $McpConfig -ForegroundColor White
Write-Host ""
Write-Host "🎯 服务器名称建议: mcp-fast-feedback-v25" -ForegroundColor Cyan
