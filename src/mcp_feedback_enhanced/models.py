#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一数据模型
============

定义混合架构中使用的统一数据结构。

作者: Minidoracat
版本: v2.5.0
"""

from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass, field


@dataclass
class FeedbackResult:
    """统一的反馈结果数据模型"""
    
    feedback_text: str = ""
    """用户提供的反馈文本"""
    
    command_logs: str = ""
    """命令执行日志"""
    
    images: List[Dict[str, Any]] = field(default_factory=list)
    """上传的图片列表"""
    
    metadata: Dict[str, Any] = field(default_factory=dict)
    """元数据，包含界面模式、时间戳等信息"""
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FeedbackResult':
        """从字典创建 FeedbackResult 对象"""
        return cls(
            feedback_text=data.get("interactive_feedback", ""),
            command_logs=data.get("command_logs", ""),
            images=data.get("images", []),
            metadata=data.get("metadata", {})
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式（向后兼容）"""
        return {
            "interactive_feedback": self.feedback_text,
            "command_logs": self.command_logs,
            "images": self.images,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_gui_result(cls, gui_result: Union[Dict[str, Any], Any]) -> 'FeedbackResult':
        """从 GUI 结果创建 FeedbackResult 对象"""
        if isinstance(gui_result, dict):
            return cls.from_dict(gui_result)
        
        # 处理 GUI 特定的结果对象
        feedback_text = ""
        command_logs = ""
        images = []
        
        if hasattr(gui_result, 'feedback_text'):
            feedback_text = gui_result.feedback_text
        elif hasattr(gui_result, 'interactive_feedback'):
            feedback_text = gui_result.interactive_feedback
        else:
            feedback_text = str(gui_result)
        
        if hasattr(gui_result, 'command_logs'):
            command_logs = gui_result.command_logs
        
        if hasattr(gui_result, 'images'):
            images = gui_result.images or []
        
        return cls(
            feedback_text=feedback_text,
            command_logs=command_logs,
            images=images,
            metadata={
                "ui_mode": "gui",
                "source": "gui_interface"
            }
        )
    
    @classmethod
    def from_web_result(cls, web_result: Union[Dict[str, Any], Any]) -> 'FeedbackResult':
        """从 Web UI 结果创建 FeedbackResult 对象"""
        if isinstance(web_result, dict):
            result = cls.from_dict(web_result)
            result.metadata.update({
                "ui_mode": "web",
                "source": "web_interface"
            })
            return result
        
        # 处理 Web UI 特定的结果对象
        if hasattr(web_result, 'to_dict'):
            return cls.from_dict(web_result.to_dict())
        
        return cls(
            feedback_text=str(web_result),
            metadata={
                "ui_mode": "web",
                "source": "web_interface"
            }
        )
    
    def is_empty(self) -> bool:
        """检查是否为空结果"""
        return not (self.feedback_text.strip() or self.command_logs.strip() or self.images)
    
    def get_ui_mode(self) -> str:
        """获取界面模式"""
        return self.metadata.get("ui_mode", "unknown")
    
    def add_metadata(self, key: str, value: Any) -> None:
        """添加元数据"""
        self.metadata[key] = value


@dataclass
class EnvironmentInfo:
    """环境信息数据模型"""
    
    environment_type: str
    """环境类型：local, ssh_remote, wsl, container, unknown"""
    
    gui_available: bool
    """GUI 是否可用"""
    
    web_available: bool
    """Web UI 是否可用"""
    
    platform: str
    """操作系统平台"""
    
    python_version: str
    """Python 版本"""
    
    available_modes: List[str] = field(default_factory=list)
    """可用的界面模式列表"""
    
    environment_variables: Dict[str, Optional[str]] = field(default_factory=dict)
    """相关环境变量"""
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "environment_type": self.environment_type,
            "gui_available": self.gui_available,
            "web_available": self.web_available,
            "platform": self.platform,
            "python_version": self.python_version,
            "available_modes": self.available_modes,
            "environment_variables": self.environment_variables
        }


@dataclass
class LaunchConfig:
    """启动配置数据模型"""
    
    project_directory: str
    """项目目录路径"""
    
    summary: str
    """AI 工作摘要"""
    
    timeout: int = 600
    """超时时间（秒）"""
    
    user_preference: Optional[str] = None
    """用户偏好模式"""
    
    force_mode: Optional[str] = None
    """强制指定模式"""
    
    additional_params: Dict[str, Any] = field(default_factory=dict)
    """额外参数"""
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "project_directory": self.project_directory,
            "summary": self.summary,
            "timeout": self.timeout,
            "user_preference": self.user_preference,
            "force_mode": self.force_mode,
            "additional_params": self.additional_params
        }


# 向后兼容的类型别名
FeedbackDict = Dict[str, Any]
"""向后兼容的字典类型别名"""
