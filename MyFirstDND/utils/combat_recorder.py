#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DND跑团库 - 战斗记录器
自动记录战斗数据并更新相关文件
"""

import json
import os
from datetime import datetime
from typing import Dict, List
from rules.dice_roller import DiceRoller

class CombatRecorder:
    """战斗记录器 - 自动记录和更新战斗数据"""
    
    def __init__(self, data_path: str = "."):
        """初始化记录器"""
        self.data_path = data_path
        self.combat_history_file = os.path.join(data_path, "combat/combat_history.json")
        self.player_character_file = os.path.join(data_path, "characters/player_character.json")
        self.balance_analysis_file = os.path.join(data_path, "combat/balance_analysis.json")
        self.adventure_log_file = os.path.join(data_path, "adventures/adventure_log.json")
        
    def record_combat_round(self, round_data: Dict) -> bool:
        """记录单回合战斗数据"""
        try:
            # 加载战斗历史
            if os.path.exists(self.combat_history_file):
                with open(self.combat_history_file, 'r', encoding='utf-8') as f:
                    combat_history = json.load(f)
            else:
                combat_history = {"combat_sessions": [], "statistics": {}}
            
            # 添加回合数据
            if "current_combat" not in combat_history:
                combat_history["current_combat"] = {
                    "combat_id": f"combat_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    "start_time": datetime.now().isoformat(),
                    "rounds": [],
                    "enemies": [],
                    "loot_gained": []
                }
            
            combat_history["current_combat"]["rounds"].append(round_data)
            
            # 保存战斗历史
            with open(self.combat_history_file, 'w', encoding='utf-8') as f:
                json.dump(combat_history, f, ensure_ascii=False, indent=2)
            
            return True
            
        except Exception as e:
            print(f"记录战斗回合时出错: {e}")
            return False
    
    def end_combat(self, combat_result: Dict) -> bool:
        """结束战斗并更新统计数据"""
        try:
            # 加载战斗历史
            with open(self.combat_history_file, 'r', encoding='utf-8') as f:
                combat_history = json.load(f)
            
            if "current_combat" in combat_history:
                # 完成当前战斗
                current_combat = combat_history["current_combat"]
                current_combat.update(combat_result)
                current_combat["end_time"] = datetime.now().isoformat()
                
                # 移动到已完成战斗列表
                combat_history["combat_sessions"].append(current_combat)
                combat_history["recent_combats"].append(current_combat)
                
                # 更新统计数据
                self._update_combat_statistics(combat_history, current_combat)
                
                # 清理当前战斗
                del combat_history["current_combat"]
                
                # 保存更新
                with open(self.combat_history_file, 'w', encoding='utf-8') as f:
                    json.dump(combat_history, f, ensure_ascii=False, indent=2)
                
                # 更新角色数据
                self._update_player_character(current_combat)
                
                # 更新平衡性分析
                self._update_balance_analysis(current_combat)
                
                # 更新冒险日志
                self._update_adventure_log(current_combat)
                
                return True
            
            return False
            
        except Exception as e:
            print(f"结束战斗时出错: {e}")
            return False
    
    def _update_combat_statistics(self, combat_history: Dict, combat_data: Dict):
        """更新战斗统计数据"""
        stats = combat_history.get("statistics", {})
        
        # 基础统计
        stats["total_combats"] = stats.get("total_combats", 0) + 1
        stats["total_rounds"] = stats.get("total_rounds", 0) + len(combat_data.get("rounds", []))
        
        # 胜负统计
        if combat_data.get("victory", False):
            stats["victories"] = stats.get("victories", 0) + 1
        else:
            stats["defeats"] = stats.get("defeats", 0) + 1
        
        # 计算平均回合数
        if stats["total_combats"] > 0:
            stats["average_rounds_per_combat"] = stats["total_rounds"] / stats["total_combats"]
        
        # 伤害统计
        player_damage = combat_data.get("player_damage_dealt", 0)
        enemy_damage = combat_data.get("enemy_damage_dealt", 0)
        
        stats["total_damage_dealt"] = stats.get("total_damage_dealt", 0) + player_damage
        stats["total_damage_taken"] = stats.get("total_damage_taken", 0) + enemy_damage
        
        # 计算战斗效率
        if enemy_damage > 0:
            stats["combat_efficiency"] = player_damage / enemy_damage
        else:
            stats["combat_efficiency"] = player_damage
    
    def _update_player_character(self, combat_data: Dict):
        """更新角色数据"""
        try:
            with open(self.player_character_file, 'r', encoding='utf-8') as f:
                player_data = json.load(f)
            
            # 更新战斗历史统计
            combat_history = player_data.get("combat_history", {})
            combat_history["total_combats"] = combat_history.get("total_combats", 0) + 1
            
            if combat_data.get("victory", False):
                combat_history["victories"] = combat_history.get("victories", 0) + 1
            else:
                combat_history["defeats"] = combat_history.get("defeats", 0) + 1
            
            # 更新伤害统计
            combat_history["total_damage_dealt"] = combat_history.get("total_damage_dealt", 0) + combat_data.get("player_damage_dealt", 0)
            combat_history["total_damage_taken"] = combat_history.get("total_damage_taken", 0) + combat_data.get("enemy_damage_dealt", 0)
            
            # 计算平均回合数
            rounds = len(combat_data.get("rounds", []))
            total_rounds = combat_history.get("total_rounds", 0) + rounds
            combat_history["total_rounds"] = total_rounds
            if combat_history["total_combats"] > 0:
                combat_history["average_rounds"] = total_rounds / combat_history["total_combats"]
            
            # 更新发展记录
            player_data["development_notes"]["last_updated"] = datetime.now().strftime("%Y-%m-%d")
            player_data["development_notes"]["notes"] = f"完成第{combat_history['total_combats']}场战斗！{combat_data.get('summary', '')}"
            
            # 保存更新
            with open(self.player_character_file, 'w', encoding='utf-8') as f:
                json.dump(player_data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"更新角色数据时出错: {e}")
    
    def _update_balance_analysis(self, combat_data: Dict):
        """更新平衡性分析"""
        try:
            if os.path.exists(self.balance_analysis_file):
                with open(self.balance_analysis_file, 'r', encoding='utf-8') as f:
                    balance_data = json.load(f)
            else:
                balance_data = {"combat_balance_analysis": {}}
            
            # 更新战斗计数
            overall = balance_data["combat_balance_analysis"].get("overall_performance", {})
            overall["combat_count"] = overall.get("combat_count", 0) + 1
            
            # 更新回合分析
            round_count = len(combat_data.get("rounds", []))
            round_analysis = balance_data["combat_balance_analysis"].get("round_analysis", {})
            
            if round_count <= 3:
                round_analysis["round_count_distribution"]["1-3_rounds"] = round_analysis["round_count_distribution"].get("1-3_rounds", 0) + 1
            elif round_count <= 6:
                round_analysis["round_count_distribution"]["4-6_rounds"] = round_analysis["round_count_distribution"].get("4-6_rounds", 0) + 1
            elif round_count <= 9:
                round_analysis["round_count_distribution"]["7-9_rounds"] = round_analysis["round_count_distribution"].get("7-9_rounds", 0) + 1
            else:
                round_analysis["round_count_distribution"]["10+_rounds"] = round_analysis["round_count_distribution"].get("10+_rounds", 0) + 1
            
            # 保存更新
            with open(self.balance_analysis_file, 'w', encoding='utf-8') as f:
                json.dump(balance_data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"更新平衡性分析时出错: {e}")
    
    def _update_adventure_log(self, combat_data: Dict):
        """更新冒险日志"""
        try:
            if os.path.exists(self.adventure_log_file):
                with open(self.adventure_log_file, 'r', encoding='utf-8') as f:
                    adventure_data = json.load(f)
            else:
                adventure_data = {"session_logs": []}
            
            # 添加战斗记录到当前会话
            if adventure_data["session_logs"]:
                current_session = adventure_data["session_logs"][-1]
                if "combat_encounters" not in current_session:
                    current_session["combat_encounters"] = []
                
                current_session["combat_encounters"].append({
                    "enemies": combat_data.get("enemies", []),
                    "result": "victory" if combat_data.get("victory", False) else "defeat",
                    "rounds": len(combat_data.get("rounds", [])),
                    "loot_gained": combat_data.get("loot_gained", [])
                })
                
                # 更新会话时间
                current_session["duration"] = "进行中"
                
                # 保存更新
                with open(self.adventure_log_file, 'w', encoding='utf-8') as f:
                    json.dump(adventure_data, f, ensure_ascii=False, indent=2)
                    
        except Exception as e:
            print(f"更新冒险日志时出错: {e}")

# 便捷函数
def start_combat(enemies: List[Dict]) -> str:
    """开始新战斗"""
    recorder = CombatRecorder()
    combat_id = f"combat_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    return combat_id

def record_round(round_data: Dict) -> bool:
    """记录战斗回合"""
    recorder = CombatRecorder()
    return recorder.record_combat_round(round_data)

def end_combat(combat_result: Dict) -> bool:
    """结束战斗"""
    recorder = CombatRecorder()
    return recorder.end_combat(combat_result)
