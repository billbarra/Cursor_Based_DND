#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DND跑团库 - AI指令加载器
让AI自动获取系统指令和配置
"""

import json
import os
from typing import Dict, List

class AIInstructionLoader:
    """AI指令加载器 - 为AI提供系统指令"""
    
    def __init__(self, data_path: str = "."):
        """初始化加载器"""
        self.data_path = data_path
        
    def get_system_instructions(self) -> str:
        """获取系统指令"""
        instructions = """
🎯 系统概述
你是一个专业的DND跑团游戏主持人(DM)，拥有一个完整的DND跑团库系统。

🏗️ 系统架构
- characters/player_character.json - 玩家角色数据
- combat/combat_history.json - 战斗历史记录
- items/equipment_database.json - 装备数据库
- monsters/monster_manual.json - 怪物图鉴
- utils/ - 自动化工具

🎮 核心功能
1. 自动化战斗系统 - 自动记录每回合数据
2. 智能平衡调整 - 根据表现自动调整难度
3. 完整数据追踪 - 记录所有游戏决策

📋 操作指令
- 当玩家描述行动时：运行骰子系统，记录数据，提供结果
- 当战斗发生时：启动战斗记录器，自动记录回合，计算结果
- 当获得装备时：自动更新角色数据，管理库存

🔧 技术实现
- 使用 utils/auto_combat_system.py 处理战斗
- 使用 utils/loot_manager.py 管理装备
- 使用 rules/dice_roller.py 处理骰子
- 自动更新所有JSON文件，不要手动编辑

⚠️ 重要提醒
1. 永远不要手动编辑JSON文件
2. 始终使用提供的Python工具
3. 自动记录所有重要事件
4. 实时更新所有相关数据
5. 给玩家选项时使用序号标号(1. 2. 3.)
6. 玩家回复序号时，直接执行对应选项

🎯 成功标准
- 玩家专注于游戏体验，AI处理技术细节
- 所有数据更新自动完成
- 提供流畅的游戏体验
"""
        return instructions
    
    def get_character_data(self) -> Dict:
        """获取角色数据"""
        try:
            character_file = os.path.join(self.data_path, "characters/player_character.json")
            if os.path.exists(character_file):
                with open(character_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return {"error": "角色文件未找到"}
        except Exception as e:
            return {"error": f"读取角色文件失败: {e}"}
    
    def get_combat_history(self) -> Dict:
        """获取战斗历史"""
        try:
            combat_file = os.path.join(self.data_path, "combat/combat_history.json")
            if os.path.exists(combat_file):
                with open(combat_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return {"error": "战斗历史文件未找到"}
        except Exception as e:
            return {"error": f"读取战斗历史失败: {e}"}
    
    def get_equipment_database(self) -> Dict:
        """获取装备数据库"""
        try:
            equipment_file = os.path.join(self.data_path, "items/equipment_database.json")
            if os.path.exists(equipment_file):
                with open(equipment_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return {"error": "装备数据库文件未找到"}
        except Exception as e:
            return {"error": f"读取装备数据库失败: {e}"}
    
    def get_monster_manual(self) -> Dict:
        """获取怪物图鉴"""
        try:
            monster_file = os.path.join(self.data_path, "monsters/monster_manual.json")
            if os.path.exists(monster_file):
                with open(monster_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return {"error": "怪物图鉴文件未找到"}
        except Exception as e:
            return {"error": f"读取怪物图鉴失败: {e}"}
    
    def get_adventure_log(self) -> Dict:
        """获取冒险日志"""
        try:
            adventure_file = os.path.join(self.data_path, "adventures/adventure_log.json")
            if os.path.exists(adventure_file):
                with open(adventure_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return {"error": "冒险日志文件未找到"}
        except Exception as e:
            return {"error": f"读取冒险日志失败: {e}"}
    
    def get_system_status(self) -> Dict:
        """获取系统状态摘要"""
        status = {
            "character_loaded": False,
            "combat_history_loaded": False,
            "equipment_loaded": False,
            "monsters_loaded": False,
            "adventure_loaded": False
        }
        
        # 检查各个组件
        if not self.get_character_data().get("error"):
            status["character_loaded"] = True
        
        if not self.get_combat_history().get("error"):
            status["combat_history_loaded"] = True
        
        if not self.get_equipment_database().get("error"):
            status["equipment_loaded"] = True
        
        if not self.get_monster_manual().get("error"):
            status["monsters_loaded"] = True
        
        if not self.get_adventure_log().get("error"):
            status["adventure_loaded"] = True
        
        return status
    
    def format_options_with_numbers(self, options: List[str]) -> str:
        """格式化选项，添加序号"""
        formatted = []
        for i, option in enumerate(options, 1):
            formatted.append(f"{i}. {option}")
        return "\n".join(formatted)
    
    def parse_number_response(self, response: str, options: List[str]) -> int:
        """解析数字回复，返回选项索引"""
        try:
            number = int(response.strip())
            if 1 <= number <= len(options):
                return number - 1  # 返回0-based索引
            else:
                return -1  # 无效数字
        except ValueError:
            return -1  # 不是数字

# 便捷函数
def get_system_instructions() -> str:
    """获取系统指令"""
    loader = AIInstructionLoader()
    return loader.get_system_instructions()

def get_character_data() -> Dict:
    """获取角色数据"""
    loader = AIInstructionLoader()
    return loader.get_character_data()

def format_options(options: List[str]) -> str:
    """格式化选项"""
    loader = AIInstructionLoader()
    return loader.format_options_with_numbers(options)

def parse_response(response: str, options: List[str]) -> int:
    """解析回复"""
    loader = AIInstructionLoader()
    return loader.parse_number_response(response, options)
