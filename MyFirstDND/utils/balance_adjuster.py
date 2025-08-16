#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DND跑团库 - 平衡性调整器
根据战斗数据自动调整游戏难度
"""

import json
import os
from typing import Dict, List

class BalanceAdjuster:
    """平衡性调整器"""
    
    def __init__(self, data_path: str = "."):
        """初始化调整器"""
        self.data_path = data_path
        
    def adjust_encounter_difficulty(self, current_difficulty: str, 
                                  combat_performance: Dict) -> Dict:
        """根据战斗表现调整遭遇战难度"""
        adjustment = {
            "current_difficulty": current_difficulty,
            "recommended_difficulty": current_difficulty,
            "adjustments": [],
            "reasoning": ""
        }
        
        difficulty_assessment = combat_performance.get("difficulty_assessment", "unknown")
        
        if difficulty_assessment == "too_easy":
            adjustment["recommended_difficulty"] = self._increase_difficulty(current_difficulty)
            adjustment["adjustments"] = [
                "增加敌人数量",
                "提升敌人AC",
                "增加敌人HP",
                "添加特殊能力"
            ]
            adjustment["reasoning"] = "战斗过于简单，需要增加挑战性"
            
        elif difficulty_assessment == "too_hard":
            adjustment["recommended_difficulty"] = self._decrease_difficulty(current_difficulty)
            adjustment["adjustments"] = [
                "减少敌人数量",
                "降低敌人AC",
                "减少敌人HP",
                "提供战术优势"
            ]
            adjustment["reasoning"] = "战斗过于困难，需要降低难度"
            
        else:
            adjustment["adjustments"] = ["保持当前难度"]
            adjustment["reasoning"] = "战斗难度适中，无需调整"
        
        return adjustment
    
    def _increase_difficulty(self, current: str) -> str:
        """提升难度等级"""
        difficulty_progression = ["easy", "normal", "hard", "deadly"]
        try:
            current_index = difficulty_progression.index(current)
            if current_index < len(difficulty_progression) - 1:
                return difficulty_progression[current_index + 1]
        except ValueError:
            pass
        return current
    
    def _decrease_difficulty(self, current: str) -> str:
        """降低难度等级"""
        difficulty_progression = ["easy", "normal", "hard", "deadly"]
        try:
            current_index = difficulty_progression.index(current)
            if current_index > 0:
                return difficulty_progression[current_index - 1]
        except ValueError:
            pass
        return current
    
    def generate_loot_recommendations(self, combat_performance: Dict, 
                                    player_level: int) -> Dict:
        """生成战利品建议"""
        performance_score = self._calculate_performance_score(combat_performance)
        
        loot_recommendations = {
            "performance_score": performance_score,
            "loot_tier": "common",
            "gold_amount": 0,
            "special_items": [],
            "reasoning": ""
        }
        
        # 根据表现确定战利品等级
        if performance_score >= 0.8:
            loot_recommendations["loot_tier"] = "uncommon"
            loot_recommendations["gold_amount"] = 50 + player_level * 10
            loot_recommendations["special_items"] = ["魔法武器", "稀有装备"]
            loot_recommendations["reasoning"] = "优秀表现，奖励稀有物品"
            
        elif performance_score >= 0.6:
            loot_recommendations["loot_tier"] = "common"
            loot_recommendations["gold_amount"] = 25 + player_level * 5
            loot_recommendations["special_items"] = ["标准装备", "治疗药水"]
            loot_recommendations["reasoning"] = "良好表现，标准奖励"
            
        else:
            loot_recommendations["loot_tier"] = "common"
            loot_recommendations["gold_amount"] = 10 + player_level * 2
            loot_recommendations["special_items"] = ["基础装备"]
            loot_recommendations["reasoning"] = "需要改进，基础奖励"
        
        return loot_recommendations
    
    def _calculate_performance_score(self, combat_performance: Dict) -> float:
        """计算战斗表现分数"""
        score = 0.0
        
        # 回合数评分 (4-7回合最佳)
        round_count = combat_performance["round_count"]
        if 4 <= round_count <= 7:
            score += 0.3
        elif 3 <= round_count <= 8:
            score += 0.2
        else:
            score += 0.1
        
        # 伤害效率评分
        damage_ratio = combat_performance["player_damage_dealt"] / max(combat_performance["player_damage_taken"], 1)
        if 0.8 <= damage_ratio <= 1.5:
            score += 0.4
        elif 0.5 <= damage_ratio <= 2.0:
            score += 0.3
        else:
            score += 0.1
        
        # 命中率评分
        hit_rate = combat_performance["hit_rate"]
        if hit_rate >= 0.6:
            score += 0.3
        elif hit_rate >= 0.4:
            score += 0.2
        else:
            score += 0.1
        
        return min(score, 1.0)
    
    def suggest_encounter_modifications(self, base_encounter: Dict, 
                                     target_difficulty: str) -> Dict:
        """建议遭遇战修改方案"""
        modifications = {
            "base_encounter": base_encounter,
            "target_difficulty": target_difficulty,
            "modifications": [],
            "modified_encounter": base_encounter.copy()
        }
        
        current_difficulty = base_encounter.get("difficulty", "normal")
        
        if target_difficulty == "hard" and current_difficulty == "normal":
            modifications["modifications"] = [
                "增加1-2个敌人",
                "提升敌人AC 1-2点",
                "增加敌人HP 20-30%"
            ]
            
        elif target_difficulty == "easy" and current_difficulty == "normal":
            modifications["modifications"] = [
                "减少1个敌人",
                "降低敌人AC 1点",
                "减少敌人HP 15-20%"
            ]
            
        elif target_difficulty == "deadly" and current_difficulty == "hard":
            modifications["modifications"] = [
                "增加1个强力敌人",
                "提升敌人AC 2-3点",
                "增加敌人HP 30-40%",
                "添加特殊能力"
            ]
        
        return modifications
    
    def generate_balance_report(self, combat_data: List[Dict]) -> str:
        """生成平衡性报告"""
        if not combat_data:
            return "暂无战斗数据"
        
        report = []
        report.append("平衡性调整报告")
        report.append("=" * 30)
        
        total_combats = len(combat_data)
        easy_combats = sum(1 for c in combat_data if c.get("difficulty_assessment") == "too_easy")
        hard_combats = sum(1 for c in combat_data if c.get("difficulty_assessment") == "too_hard")
        balanced_combats = sum(1 for c in combat_data if c.get("difficulty_assessment") == "balanced")
        
        report.append(f"总战斗次数: {total_combats}")
        report.append(f"过于简单: {easy_combats}")
        report.append(f"过于困难: {hard_combats}")
        report.append(f"平衡良好: {balanced_combats}")
        report.append("")
        
        if easy_combats > hard_combats:
            report.append("建议: 整体提升难度")
            report.append("- 增加敌人数量")
            report.append("- 提升敌人属性")
            report.append("- 添加环境挑战")
        elif hard_combats > easy_combats:
            report.append("建议: 整体降低难度")
            report.append("- 减少敌人数量")
            report.append("- 降低敌人属性")
            report.append("- 提供更多帮助")
        else:
            report.append("建议: 保持当前难度设置")
        
        return "\n".join(report)

# 使用示例
if __name__ == "__main__":
    adjuster = BalanceAdjuster()
    
    # 模拟战斗数据
    sample_combat = {
        "round_count": 3,
        "player_damage_dealt": 45,
        "player_damage_taken": 8,
        "hit_rate": 0.8
    }
    
    # 生成调整建议
    adjustment = adjuster.adjust_encounter_difficulty("normal", sample_combat)
    print("难度调整建议:")
    print(json.dumps(adjustment, ensure_ascii=False, indent=2))
    
    # 生成战利品建议
    loot = adjuster.generate_loot_recommendations(sample_combat, 1)
    print("\n战利品建议:")
    print(json.dumps(loot, ensure_ascii=False, indent=2))
