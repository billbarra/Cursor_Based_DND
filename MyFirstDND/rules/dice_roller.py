#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DND跑团库 - 骰子系统
提供各种骰子功能和随机数生成
"""

import random
import re
from typing import Dict
import json

class DiceRoller:
    """骰子系统主类"""
    
    def __init__(self):
        """初始化骰子系统"""
        self.roll_history = []
        self.critical_hits = 0
        self.critical_failures = 0
        
    def roll_dice(self, dice_notation: str) -> Dict:
        """解析骰子表达式并掷骰"""
        try:
            pattern = r'^(\d*)d(\d+)([+-]\d+)?$'
            match = re.match(pattern, dice_notation.lower())
            
            if not match:
                raise ValueError(f"无效的骰子表达式: {dice_notation}")
            
            count = int(match.group(1)) if match.group(1) else 1
            sides = int(match.group(2))
            modifier = int(match.group(3)) if match.group(3) else 0
            
            rolls = [random.randint(1, sides) for _ in range(count)]
            total = sum(rolls) + modifier
            
            result = {
                "notation": dice_notation,
                "count": count,
                "sides": sides,
                "modifier": modifier,
                "rolls": rolls,
                "total": total
            }
            
            self.roll_history.append(result)
            return result
            
        except Exception as e:
            return {"error": str(e), "notation": dice_notation}
    
    def roll_d20(self, advantage: str = "none") -> Dict:
        """掷d20，支持优势/劣势"""
        if advantage == "advantage":
            roll1 = random.randint(1, 20)
            roll2 = random.randint(1, 20)
            rolls = [roll1, roll2]
            total = max(rolls)
            advantage_type = "优势"
        elif advantage == "disadvantage":
            roll1 = random.randint(1, 20)
            roll2 = random.randint(1, 20)
            rolls = [roll1, roll2]
            total = min(rolls)
            advantage_type = "劣势"
        else:
            roll1 = random.randint(1, 20)
            rolls = [roll1]
            total = roll1
            advantage_type = "无"
        
        is_critical = roll1 == 20
        is_critical_failure = roll1 == 1
        
        if is_critical:
            self.critical_hits += 1
        if is_critical_failure:
            self.critical_failures += 1
        
        result = {
            "type": "d20",
            "advantage": advantage_type,
            "rolls": rolls,
            "total": total,
            "is_critical": is_critical,
            "is_critical_failure": is_critical_failure
        }
        
        self.roll_history.append(result)
        return result
    
    def roll_ability_check(self, ability_modifier: int, proficiency_bonus: int = 0, 
                          advantage: str = "none", dc: int = None) -> Dict:
        """进行属性检定"""
        d20_result = self.roll_d20(advantage)
        total = d20_result["total"] + ability_modifier + proficiency_bonus
        
        success = None
        if dc is not None:
            success = total >= dc
            if d20_result["is_critical"]:
                success = True
            elif d20_result["is_critical_failure"]:
                success = False
        
        result = {
            "type": "ability_check",
            "d20_result": d20_result,
            "ability_modifier": ability_modifier,
            "proficiency_bonus": proficiency_bonus,
            "total": total,
            "dc": dc,
            "success": success
        }
        
        self.roll_history.append(result)
        return result
    
    def roll_attack(self, attack_bonus: int, target_ac: int, 
                   advantage: str = "none", weapon_damage: str = None) -> Dict:
        """进行攻击检定"""
        d20_result = self.roll_d20(advantage)
        attack_total = d20_result["total"] + attack_bonus
        hit = attack_total >= target_ac
        
        if d20_result["is_critical"]:
            hit = True
        if d20_result["is_critical_failure"]:
            hit = False
        
        damage_result = None
        if hit and weapon_damage:
            damage_result = self.roll_dice(weapon_damage)
            if d20_result["is_critical"]:
                damage_result["total"] *= 2
                damage_result["is_critical"] = True
        
        result = {
            "type": "attack",
            "d20_result": d20_result,
            "attack_bonus": attack_bonus,
            "attack_total": attack_total,
            "target_ac": target_ac,
            "hit": hit,
            "damage": damage_result
        }
        
        self.roll_history.append(result)
        return result
    
    def get_statistics(self) -> Dict:
        """获取骰子统计信息"""
        if not self.roll_history:
            return {"message": "暂无掷骰记录"}
        
        total_rolls = len(self.roll_history)
        d20_rolls = [r for r in self.roll_history if r.get("type") == "d20" or "d20" in str(r.get("type"))]
        
        stats = {
            "total_rolls": total_rolls,
            "d20_rolls": len(d20_rolls),
            "critical_hits": self.critical_hits,
            "critical_failures": self.critical_failures,
            "critical_rate": self.critical_hits / max(len(d20_rolls), 1)
        }
        
        return stats

# 便捷函数
def roll(dice_notation: str) -> Dict:
    """快速掷骰函数"""
    roller = DiceRoller()
    return roller.roll_dice(dice_notation)

def roll_d20(advantage: str = "none") -> Dict:
    """快速掷d20函数"""
    roller = DiceRoller()
    return roller.roll_d20(advantage)
