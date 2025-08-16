#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DND跑团库 - 游戏数据分析器
分析战斗数据并提供平衡性建议
"""

import json
import os
from typing import Dict, List

class GameAnalyzer:
    """游戏数据分析器"""
    
    def __init__(self, data_path: str = "."):
        """初始化分析器"""
        self.data_path = data_path
        
    def analyze_combat_performance(self, combat_data: Dict) -> Dict:
        """分析单场战斗表现"""
        analysis = {
            "round_count": len(combat_data.get("rounds", [])),
            "player_damage_dealt": 0,
            "player_damage_taken": 0,
            "hit_rate": 0.0,
            "difficulty_assessment": "unknown"
        }
        
        rounds = combat_data.get("rounds", [])
        if not rounds:
            return analysis
        
        # 分析每回合数据
        total_player_attacks = 0
        total_player_hits = 0
        
        for round_data in rounds:
            player_actions = round_data.get("player_actions", [])
            for action in player_actions:
                if action.get("type") == "attack":
                    total_player_attacks += 1
                    if action.get("hit", False):
                        total_player_hits += 1
                        analysis["player_damage_dealt"] += action.get("damage", 0)
            
            enemy_actions = round_data.get("enemy_actions", [])
            for action in enemy_actions:
                if action.get("type") == "attack":
                    if action.get("hit", False):
                        analysis["player_damage_taken"] += action.get("damage", 0)
        
        # 计算命中率
        if total_player_attacks > 0:
            analysis["hit_rate"] = total_player_hits / total_player_attacks
        
        # 评估难度
        analysis["difficulty_assessment"] = self._assess_difficulty(analysis)
        
        return analysis
    
    def _assess_difficulty(self, analysis: Dict) -> str:
        """评估战斗难度"""
        round_count = analysis["round_count"]
        damage_ratio = analysis["player_damage_dealt"] / max(analysis["player_damage_taken"], 1)
        
        if round_count <= 3 and damage_ratio > 2.0:
            return "too_easy"
        elif round_count >= 8 or damage_ratio < 0.5:
            return "too_hard"
        elif 4 <= round_count <= 7 and 0.8 <= damage_ratio <= 1.5:
            return "balanced"
        else:
            return "needs_adjustment"
    
    def generate_balance_recommendations(self, analysis: Dict) -> List[Dict]:
        """生成平衡性调整建议"""
        recommendations = []
        difficulty = analysis["difficulty_assessment"]
        
        if difficulty == "too_easy":
            recommendations.append({
                "type": "enemy_enhancement",
                "description": "增加敌人数量或提升敌人属性",
                "suggestions": ["增加1-2个敌人", "提升敌人AC", "增加敌人HP"]
            })
        elif difficulty == "too_hard":
            recommendations.append({
                "type": "enemy_weakening",
                "description": "削弱敌人或提供优势",
                "suggestions": ["减少敌人数量", "降低敌人AC", "提供战术优势"]
            })
        
        return recommendations
    
    def generate_report(self) -> str:
        """生成分析报告"""
        report = []
        report.append("DND跑团库 - 游戏数据分析报告")
        report.append("=" * 40)
        report.append("系统已就绪，等待战斗数据...")
        return "\n".join(report)

# 使用示例
if __name__ == "__main__":
    analyzer = GameAnalyzer()
    report = analyzer.generate_report()
    print(report)
