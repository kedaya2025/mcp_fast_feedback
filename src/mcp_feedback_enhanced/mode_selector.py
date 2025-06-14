#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能模式选择器
==============

自动检测环境并选择最适合的界面模式（GUI 或 Web UI）。
支持用户配置和降级机制。

作者: Minidoracat
版本: v2.5.0
"""

import os
import sys
import platform
from typing import Optional, Literal, Dict, Any
from enum import Enum
import logging

# 设置日志
logger = logging.getLogger(__name__)

class UIMode(Enum):
    """界面模式枚举"""
    GUI = "gui"
    WEB = "web"
    AUTO = "auto"

class EnvironmentType(Enum):
    """环境类型枚举"""
    LOCAL = "local"
    SSH_REMOTE = "ssh_remote"
    WSL = "wsl"
    CONTAINER = "container"
    UNKNOWN = "unknown"

class ModeSelector:
    """智能模式选择器"""
    
    def __init__(self):
        self.environment_type = self._detect_environment()
        self.gui_available = self._check_gui_availability()
        
    def _detect_environment(self) -> EnvironmentType:
        """检测当前运行环境"""
        try:
            # 检测 WSL 环境
            if self._is_wsl():
                return EnvironmentType.WSL
            
            # 检测 SSH Remote 环境
            if self._is_ssh_remote():
                return EnvironmentType.SSH_REMOTE
            
            # 检测容器环境
            if self._is_container():
                return EnvironmentType.CONTAINER
            
            # 默认为本地环境
            return EnvironmentType.LOCAL
            
        except Exception as e:
            logger.warning(f"环境检测失败: {e}")
            return EnvironmentType.UNKNOWN
    
    def _is_wsl(self) -> bool:
        """检测是否为 WSL 环境"""
        try:
            # 检查 /proc/version 文件
            if os.path.exists('/proc/version'):
                with open('/proc/version', 'r') as f:
                    version_info = f.read().lower()
                    return 'microsoft' in version_info or 'wsl' in version_info
            
            # 检查环境变量
            return 'WSL_DISTRO_NAME' in os.environ or 'WSLENV' in os.environ
            
        except Exception:
            return False
    
    def _is_ssh_remote(self) -> bool:
        """检测是否为 SSH Remote 环境"""
        try:
            # 检查 SSH 相关环境变量
            ssh_indicators = [
                'SSH_CLIENT', 'SSH_CONNECTION', 'SSH_TTY',
                'VSCODE_REMOTE_CONTAINERS_SESSION',
                'REMOTE_CONTAINERS', 'CODESPACES'
            ]
            
            for indicator in ssh_indicators:
                if indicator in os.environ:
                    return True
            
            # 检查是否在远程会话中
            if os.environ.get('TERM_PROGRAM') == 'vscode' and 'VSCODE_IPC_HOOK_CLI' in os.environ:
                return True
                
            return False
            
        except Exception:
            return False
    
    def _is_container(self) -> bool:
        """检测是否为容器环境"""
        try:
            # 检查容器相关文件
            container_files = [
                '/.dockerenv',
                '/run/.containerenv'
            ]
            
            for file_path in container_files:
                if os.path.exists(file_path):
                    return True
            
            # 检查 cgroup 信息
            if os.path.exists('/proc/1/cgroup'):
                with open('/proc/1/cgroup', 'r') as f:
                    cgroup_info = f.read().lower()
                    return 'docker' in cgroup_info or 'containerd' in cgroup_info
            
            return False
            
        except Exception:
            return False
    
    def _check_gui_availability(self) -> bool:
        """检查 GUI 是否可用"""
        try:
            # 检查是否安装了 PySide6
            try:
                import PySide6
                gui_installed = True
            except ImportError:
                gui_installed = False
            
            if not gui_installed:
                return False
            
            # 检查显示环境
            if platform.system() == "Linux":
                # Linux 环境检查 DISPLAY 或 WAYLAND_DISPLAY
                return bool(os.environ.get('DISPLAY') or os.environ.get('WAYLAND_DISPLAY'))
            elif platform.system() == "Darwin":
                # macOS 通常支持 GUI
                return True
            elif platform.system() == "Windows":
                # Windows 通常支持 GUI
                return True
            else:
                return False
                
        except Exception as e:
            logger.warning(f"GUI 可用性检查失败: {e}")
            return False
    
    def select_mode(self, 
                   user_preference: Optional[UIMode] = None,
                   force_mode: Optional[UIMode] = None) -> UIMode:
        """
        选择最适合的界面模式
        
        Args:
            user_preference: 用户偏好设置
            force_mode: 强制指定模式
            
        Returns:
            UIMode: 选择的界面模式
        """
        # 强制模式优先级最高
        if force_mode and force_mode != UIMode.AUTO:
            logger.info(f"使用强制指定模式: {force_mode.value}")
            return force_mode
        
        # 用户偏好次之
        if user_preference and user_preference != UIMode.AUTO:
            if self._can_use_mode(user_preference):
                logger.info(f"使用用户偏好模式: {user_preference.value}")
                return user_preference
            else:
                logger.warning(f"用户偏好模式 {user_preference.value} 不可用，使用自动选择")
        
        # 自动选择模式
        return self._auto_select_mode()
    
    def _can_use_mode(self, mode: UIMode) -> bool:
        """检查指定模式是否可用"""
        if mode == UIMode.GUI:
            return self.gui_available
        elif mode == UIMode.WEB:
            return True  # Web UI 总是可用
        else:
            return True
    
    def _auto_select_mode(self) -> UIMode:
        """自动选择最适合的模式"""
        # 远程环境优先使用 Web UI
        if self.environment_type in [EnvironmentType.SSH_REMOTE, EnvironmentType.CONTAINER]:
            logger.info(f"检测到远程环境 ({self.environment_type.value})，选择 Web UI")
            return UIMode.WEB
        
        # WSL 环境根据 GUI 可用性选择
        if self.environment_type == EnvironmentType.WSL:
            if self.gui_available:
                logger.info("WSL 环境检测到 GUI 支持，选择 GUI 模式")
                return UIMode.GUI
            else:
                logger.info("WSL 环境无 GUI 支持，选择 Web UI")
                return UIMode.WEB
        
        # 本地环境优先使用 GUI
        if self.environment_type == EnvironmentType.LOCAL:
            if self.gui_available:
                logger.info("本地环境检测到 GUI 支持，选择 GUI 模式")
                return UIMode.GUI
            else:
                logger.info("本地环境无 GUI 支持，选择 Web UI")
                return UIMode.WEB
        
        # 未知环境默认使用 Web UI
        logger.info(f"未知环境类型 ({self.environment_type.value})，默认选择 Web UI")
        return UIMode.WEB
    
    def get_environment_info(self) -> Dict[str, Any]:
        """获取环境信息"""
        return {
            "environment_type": self.environment_type.value,
            "gui_available": self.gui_available,
            "platform": platform.system(),
            "python_version": sys.version,
            "display": os.environ.get('DISPLAY'),
            "wayland_display": os.environ.get('WAYLAND_DISPLAY'),
            "ssh_client": os.environ.get('SSH_CLIENT'),
            "wsl_distro": os.environ.get('WSL_DISTRO_NAME'),
        }

# 全局实例
_mode_selector = None

def get_mode_selector() -> ModeSelector:
    """获取全局模式选择器实例"""
    global _mode_selector
    if _mode_selector is None:
        _mode_selector = ModeSelector()
    return _mode_selector

def select_ui_mode(user_preference: Optional[str] = None,
                  force_mode: Optional[str] = None) -> str:
    """
    便捷函数：选择界面模式
    
    Args:
        user_preference: 用户偏好 ("gui", "web", "auto")
        force_mode: 强制模式 ("gui", "web", "auto")
        
    Returns:
        str: 选择的模式 ("gui" 或 "web")
    """
    selector = get_mode_selector()
    
    # 转换字符串参数为枚举
    user_pref = None
    if user_preference:
        try:
            user_pref = UIMode(user_preference.lower())
        except ValueError:
            logger.warning(f"无效的用户偏好: {user_preference}")
    
    force = None
    if force_mode:
        try:
            force = UIMode(force_mode.lower())
        except ValueError:
            logger.warning(f"无效的强制模式: {force_mode}")
    
    selected_mode = selector.select_mode(user_pref, force)
    return selected_mode.value
