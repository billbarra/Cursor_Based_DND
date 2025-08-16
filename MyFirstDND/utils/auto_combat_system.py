#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DND跑团库 - 自动化战斗系统
整合战斗记录器和战利品管理器，提供完整的自动化战斗体验
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from .combat_recorder import CombatRecorder
from .loot_manager import LootManager
from rules.dice_roller import DiceRoller

class AutoCombatSystem:
    """自动化战斗系统 - 整合所有战斗相关功能"""
    
    def __init__(self, data_path: str = "."):
        """初始化系统"""
        self.data_path = data_path
        self.combat_recorder = CombatRecorder(data_path)
        self.loot_manager = LootManager(data_path)
        self.dice_roller = DiceRoller()
        
    def start_combat(self, enemies: List[Dict], environment: Dict = None) -> str:
        """开始新战斗"""
        try:
            # 创建战斗记录
            combat_id = f"combat_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # 初始化战斗数据
            combat_data = {
                "combat_id": combat_id,
                "start_time": datetime.now().isoformat(),
                "enemies": enemies,
                "environment": environment or {},
                "rounds": [],
                "current_round": 0,
                "player_hp_start": self._get_player_hp(),
                "player_hp_current": self._get_player_hp()
            }
            
            # 记录战斗开始
            self.combat_recorder.record_combat_round({
                "round": 0,
                "type": "combat_start",
                "data": combat_data
            })
            
            return combat_id
            
        except Exception as e:
            print(f"开始战斗时出错: {e}")
            return None
    
    def record_player_action(self, action: Dict) -> bool:
        """记录玩家行动"""
        try:
            round_data = {
                "round": action.get("round", 1),
                "type": "player_action",
                "player_action": action,
                "timestamp": datetime.now().isoformat()
            }
            
            return self.combat_recorder.record_combat_round(round_data)
            
        except Exception as e:
            print(f"记录玩家行动时出错: {e}")
            return False
    
    def record_enemy_action(self, enemy_name: str, action: Dict) -> bool:
        """记录敌人行动"""
        try:
            round_data = {
                "round": action.get("round", 1),
                "type": "enemy_action",
                "enemy_name": enemy_name,
                "enemy_action": action,
                "timestamp": datetime.now().isoformat()
            }
            
            return self.combat_recorder.record_combat_round(round_data)
            
        except Exception as e:
            print(f"记录敌人行动时出错: {e}")
            return False
    
    def end_combat(self, result: Dict) -> bool:
        """结束战斗"""
        try:
            # 计算最终统计数据
            final_result = self._calculate_combat_result(result)
            
            # 记录战斗结束
            self.combat_recorder.record_combat_round({
                "round": result.get("final_round", 1),
                "type": "combat_end",
                "result": final_result,
                "timestamp": datetime.now().isoformat()
            })
            
            # 结束战斗并更新所有相关数据
            return self.combat_recorder.end_combat(final_result)
            
        except Exception as e:
            print(f"结束战斗时出错: {e}")
            return False
    
    def _calculate_combat_result(self, result: Dict) -> Dict:
        """计算战斗结果统计"""
        try:
            # 获取战斗数据
            combat_history = self.combat_recorder.combat_history_file
            if os.path.exists(combat_history):
                with open(combat_history, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    current_combat = data.get("current_combat", {})
            else:
                current_combat = {}
            
            rounds = current_combat.get("rounds", [])
            
            # 计算统计数据
            player_damage_dealt = 0
            enemy_damage_dealt = 0
            total_rounds = len([r for r in rounds if r.get("type") in ["player_action", "enemy_action"]])
            
            # 分析每回合数据
            for round_data in rounds:
                if round_data.get("type") == "player_action":
                    action = round_data.get("player_action", {})
                    if action.get("type") == "attack" and action.get("hit"):
                        player_damage_dealt += action.get("damage", 0)
                        
                elif round_data.get("type") == "enemy_action":
                    action = round_data.get("enemy_action", {})
                    if action.get("type") == "attack" and action.get("hit"):
                        enemy_damage_dealt += action.get("damage", 0)
            
            # 构建结果
            final_result = {
                "victory": result.get("victory", False),
                "rounds": total_rounds,
                "player_damage_dealt": player_damage_dealt,
                "enemy_damage_dealt": enemy_damage_dealt,
                "enemies_defeated": result.get("enemies_defeated", []),
                "loot_gained": result.get("loot_gained", []),
                "summary": result.get("summary", ""),
                "combat_id": current_combat.get("combat_id", "unknown")
            }
            
            return final_result
            
        except Exception as e:
            print(f"计算战斗结果时出错: {e}")
            return result
    
    def _get_player_hp(self) -> int:
        """获取玩家当前生命值"""
        try:
            with open(self.combat_recorder.player_character_file, 'r', encoding='utf-8') as f:
                player_data = json.load(f)
                return player_data.get("combat_stats", {}).get("hit_points", {}).get("current", 12)
        except:
            return 12
    
    def auto_loot_distribution(self, combat_performance: Dict, player_level: int) -> List[Dict]:
        """自动战利品分配"""
        try:
            from .balance_adjuster import BalanceAdjuster
            
            adjuster = BalanceAdjuster(self.data_path)
            loot_recommendations = adjuster.generate_loot_recommendations(combat_performance, player_level)
            
            # 根据表现生成战利品
            loot_items = []
            performance_score = loot_recommendations.get("performance_score", 0.5)
            
            if performance_score >= 0.8:
                # 优秀表现 - 稀有物品
                loot_items.extend([
                    {
                        "name": "治疗药水",
                        "type": "consumable",
                        "quantity": 2,
                        "rarity": "common"
                    },
                    {
                        "name": "小宝石",
                        "type": "gem",
                        "value": 25,
                        "rarity": "common"
                    }
                ])
                
            elif performance_score >= 0.6:
                # 良好表现 - 标准物品
                loot_items.extend([
                    {
                        "name": "治疗药水",
                        "type": "consumable",
                        "quantity": 1,
                        "rarity": "common"
                    }
                ])
            
            # 基础战利品
            loot_items.extend([
                {
                    "name": "金币",
                    "type": "currency",
                    "gold": 10 + player_level * 5
                }
            ])
            
            return loot_items
            
        except Exception as e:
            print(f"自动战利品分配时出错: {e}")
            return []
    
    def quick_combat(self, enemies: List[Dict], player_actions: List[Dict]) -> Dict:
        """快速战斗模式"""
        try:
            # 开始战斗
            combat_id = self.start_combat(enemies)
            if not combat_id:
                return {"error": "无法开始战斗"}
            
            # 记录玩家行动
            for i, action in enumerate(player_actions, 1):
                action["round"] = i
                self.record_player_action(action)
            
            # 模拟敌人行动
            for i, enemy in enumerate(enemies):
                enemy_action = self._simulate_enemy_action(enemy, i+1)
                self.record_enemy_action(enemy["name"], enemy_action)
            
            # 计算结果
            result = {
                "victory": True,  # 简化版本，假设玩家获胜
                "final_round": len(player_actions),
                "enemies_defeated": [e["name"] for e in enemies],
                "loot_gained": self.auto_loot_distribution({"round_count": len(player_actions)}, 1),
                "summary": f"击败了{len(enemies)}个敌人"
            }
            
            # 结束战斗
            self.end_combat(result)
            
            return result
            
        except Exception as e:
            print(f"快速战斗时出错: {e}")
            return {"error": str(e)}
    
    def _simulate_enemy_action(self, enemy: Dict, round_num: int) -> Dict:
        """模拟敌人行动"""
        # 简化的敌人AI
        return {
            "round": round_num,
            "type": "attack",
            "target": "player",
            "attack_roll": self.dice_roller.roll_d20(),
            "damage": 0,  # 简化版本
            "hit": False
        }

# 便捷函数
def start_combat(enemies: List[Dict]) -> str:
    """开始新战斗"""
    system = AutoCombatSystem()
    return system.start_combat(enemies)

def record_player_action(action: Dict) -> bool:
    """记录玩家行动"""
    system = AutoCombatSystem()
    return system.record_player_action(action)

def end_combat(result: Dict) -> bool:
    """结束战斗"""
    system = AutoCombatSystem()
    return system.end_combat(result)

def quick_combat(enemies: List[Dict], player_actions: List[Dict]) -> Dict:
    """快速战斗模式"""
    system = AutoCombatSystem()
    return system.quick_combat(enemies, player_actions)
