#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一启动器
==========

提供统一的界面启动接口，支持 GUI 和 Web UI 的智能选择和降级机制。

作者: Minidoracat
版本: v2.5.0
"""

import os
import logging
from typing import Optional, List, Dict, Any, Union
from .mode_selector import get_mode_selector, UIMode, select_ui_mode
from .models import FeedbackResult

# 设置日志
logger = logging.getLogger(__name__)

class FeedbackLauncher:
    """统一反馈界面启动器"""
    
    def __init__(self):
        self.mode_selector = get_mode_selector()
        self._gui_available = None
        self._web_available = None
    
    @property
    def gui_available(self) -> bool:
        """检查 GUI 是否可用"""
        if self._gui_available is None:
            # 使用模式选择器的检查结果
            self._gui_available = self.mode_selector.gui_available
        return self._gui_available
    
    @property
    def web_available(self) -> bool:
        """检查 Web UI 是否可用"""
        if self._web_available is None:
            try:
                from .web import WebUIManager
                self._web_available = True
            except ImportError:
                self._web_available = False
        return self._web_available
    
    async def launch_feedback_ui(self,
                                 project_directory: str,
                                 summary: str,
                                 timeout: int = 600,
                                 user_preference: Optional[str] = None,
                                 force_mode: Optional[str] = None,
                                 **kwargs) -> Optional[FeedbackResult]:
        """
        启动反馈界面
        
        Args:
            project_directory: 项目目录
            summary: AI 工作摘要
            timeout: 超时时间（秒）
            user_preference: 用户偏好模式 ("gui", "web", "auto")
            force_mode: 强制指定模式 ("gui", "web")
            **kwargs: 其他参数
            
        Returns:
            Optional[FeedbackResult]: 用户反馈结果
        """
        # 选择界面模式
        selected_mode = select_ui_mode(user_preference, force_mode)
        
        logger.info(f"启动反馈界面，模式: {selected_mode}")
        
        # 尝试启动选定的模式
        try:
            if selected_mode == "gui":
                return await self._launch_gui(project_directory, summary, timeout, **kwargs)
            else:
                return await self._launch_web(project_directory, summary, timeout, **kwargs)

        except Exception as e:
            logger.error(f"启动 {selected_mode} 模式失败: {e}")

            # 降级机制
            if selected_mode == "gui" and self.web_available:
                logger.info("GUI 启动失败，降级到 Web UI")
                return await self._launch_web(project_directory, summary, timeout, **kwargs)
            elif selected_mode == "web" and self.gui_available:
                logger.info("Web UI 启动失败，降级到 GUI")
                return await self._launch_gui(project_directory, summary, timeout, **kwargs)
            else:
                logger.error("所有界面模式都不可用")
                raise
    
    async def _launch_gui(self,
                         project_directory: str,
                         summary: str,
                         timeout: int,
                         **kwargs) -> Optional[FeedbackResult]:
        """启动 GUI 界面"""
        if not self.gui_available:
            raise RuntimeError("GUI 不可用")
        
        try:
            from .gui import feedback_ui_with_timeout
            import asyncio
            import concurrent.futures

            logger.info("启动 GUI 界面")

            # 在线程池中运行 GUI（因为 GUI 是同步的）
            loop = asyncio.get_event_loop()
            with concurrent.futures.ThreadPoolExecutor() as executor:
                result = await loop.run_in_executor(
                    executor,
                    feedback_ui_with_timeout,
                    project_directory,
                    summary,
                    timeout
                )

            # 转换结果格式
            if result:
                return FeedbackResult.from_gui_result(result)
            return None

        except ImportError as e:
            logger.error(f"GUI 模块导入失败: {e}")
            raise RuntimeError("GUI 模块不可用")
    
    async def _launch_web(self,
                         project_directory: str,
                         summary: str,
                         timeout: int,
                         **kwargs) -> Optional[FeedbackResult]:
        """启动 Web UI 界面"""
        if not self.web_available:
            raise RuntimeError("Web UI 不可用")
        
        try:
            from .web import launch_web_feedback_ui
            logger.info("启动 Web UI 界面")
            
            # 调用 Web UI 界面
            result = await launch_web_feedback_ui(project_directory, summary, timeout)
            if result:
                return FeedbackResult.from_web_result(result)
            return None
            
        except ImportError as e:
            logger.error(f"Web UI 模块导入失败: {e}")
            raise RuntimeError("Web UI 模块不可用")
    

    
    def get_available_modes(self) -> List[str]:
        """获取可用的界面模式"""
        modes = []
        if self.gui_available:
            modes.append("gui")
        if self.web_available:
            modes.append("web")
        return modes
    
    def get_environment_info(self) -> Dict[str, Any]:
        """获取环境信息"""
        info = self.mode_selector.get_environment_info()
        info.update({
            "gui_available": self.gui_available,
            "web_available": self.web_available,
            "available_modes": self.get_available_modes()
        })
        return info

# 全局启动器实例
_launcher = None

def get_launcher() -> FeedbackLauncher:
    """获取全局启动器实例"""
    global _launcher
    if _launcher is None:
        _launcher = FeedbackLauncher()
    return _launcher

async def launch_feedback_ui(project_directory: str,
                            summary: str,
                            timeout: int = 600,
                            user_preference: Optional[str] = None,
                            force_mode: Optional[str] = None,
                            **kwargs) -> Optional[FeedbackResult]:
    """
    便捷函数：启动反馈界面
    
    Args:
        project_directory: 项目目录
        summary: AI 工作摘要
        timeout: 超时时间（秒）
        user_preference: 用户偏好模式
        force_mode: 强制指定模式
        **kwargs: 其他参数
        
    Returns:
        Optional[FeedbackResult]: 用户反馈结果
    """
    launcher = get_launcher()
    return await launcher.launch_feedback_ui(
        project_directory=project_directory,
        summary=summary,
        timeout=timeout,
        user_preference=user_preference,
        force_mode=force_mode,
        **kwargs
    )

def get_environment_info() -> Dict[str, Any]:
    """获取环境信息"""
    launcher = get_launcher()
    return launcher.get_environment_info()

def get_available_modes() -> List[str]:
    """获取可用的界面模式"""
    launcher = get_launcher()
    return launcher.get_available_modes()
