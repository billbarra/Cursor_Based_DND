#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DND跑团库 - 战利品管理器
自动管理装备获得、消耗和更新
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional

class LootManager:
    """战利品管理器 - 自动管理装备和物品"""
    
    def __init__(self, data_path: str = "."):
        """初始化管理器"""
        self.data_path = data_path
        self.player_character_file = os.path.join(data_path, "characters/player_character.json")
        self.equipment_database_file = os.path.join(data_path, "items/equipment_database.json")
        
    def add_loot(self, loot_items: List[Dict]) -> bool:
        """添加战利品到角色装备"""
        try:
            # 加载角色数据
            with open(self.player_character_file, 'r', encoding='utf-8') as f:
                player_data = json.load(f)
            
            # 处理每个战利品
            for item in loot_items:
                self._add_single_item(player_data, item)
            
            # 保存更新
            with open(self.player_character_file, 'w', encoding='utf-8') as f:
                json.dump(player_data, f, ensure_ascii=False, indent=2)
            
            return True
            
        except Exception as e:
            print(f"添加战利品时出错: {e}")
            return False
    
    def _add_single_item(self, player_data: Dict, item: Dict):
        """添加单个物品"""
        item_type = item.get("type", "misc")
        item_name = item.get("name", "未知物品")
        
        if item_type == "weapon":
            # 添加到武器列表
            if "weapons" not in player_data["equipment"]:
                player_data["equipment"]["weapons"] = []
            
            # 检查是否已存在
            existing_weapon = next((w for w in player_data["equipment"]["weapons"] if w["name"] == item_name), None)
            if existing_weapon:
                # 更新现有武器
                existing_weapon.update(item)
            else:
                # 添加新武器
                player_data["equipment"]["weapons"].append(item)
                
        elif item_type == "armor":
            # 添加到护甲
            player_data["equipment"]["armor"] = item
            
        elif item_type == "shield":
            # 添加到盾牌
            player_data["equipment"]["shield"] = item
            
        elif item_type == "consumable":
            # 添加到消耗品列表
            if "items" not in player_data["equipment"]:
                player_data["equipment"]["items"] = []
            
            # 查找现有消耗品
            existing_item = next((i for i in player_data["equipment"]["items"] if i["name"] == item_name), None)
            if existing_item and "quantity" in existing_item:
                existing_item["quantity"] += item.get("quantity", 1)
            else:
                player_data["equipment"]["items"].append(item)
                
        elif item_type == "ammunition":
            # 添加到弹药
            if "items" not in player_data["equipment"]:
                player_data["equipment"]["items"] = []
            
            existing_ammo = next((i for i in player_data["equipment"]["items"] if i["name"] == item_name), None)
            if existing_ammo:
                existing_ammo["quantity"] += item.get("quantity", 1)
            else:
                player_data["equipment"]["items"].append(item)
        
        # 更新库存
        self._update_inventory(player_data, item)
    
    def _update_inventory(self, player_data: Dict, item: Dict):
        """更新库存信息"""
        inventory = player_data.get("inventory", {})
        
        # 更新金币
        if "gold" in item:
            inventory["gold"] = inventory.get("gold", 0) + item["gold"]
        
        # 更新宝石
        if "gems" in item:
            if "gems" not in inventory:
                inventory["gems"] = []
            inventory["gems"].extend(item["gems"])
        
        # 更新魔法物品
        if item.get("rarity") in ["uncommon", "rare", "very_rare", "legendary"]:
            if "magic_items" not in inventory:
                inventory["magic_items"] = []
            inventory["magic_items"].append({
                "name": item["name"],
                "type": item.get("type", "unknown"),
                "rarity": item.get("rarity", "common")
            })
    
    def remove_item(self, item_name: str, quantity: int = 1) -> bool:
        """移除物品"""
        try:
            with open(self.player_character_file, 'r', encoding='utf-8') as f:
                player_data = json.load(f)
            
            # 从装备中移除
            if "weapons" in player_data["equipment"]:
                player_data["equipment"]["weapons"] = [
                    w for w in player_data["equipment"]["weapons"] 
                    if w["name"] != item_name
                ]
            
            # 从物品中移除
            if "items" in player_data["equipment"]:
                for item in player_data["equipment"]["items"]:
                    if item["name"] == item_name:
                        if "quantity" in item:
                            item["quantity"] -= quantity
                            if item["quantity"] <= 0:
                                player_data["equipment"]["items"].remove(item)
                        else:
                            player_data["equipment"]["items"].remove(item)
                        break
            
            # 保存更新
            with open(self.player_character_file, 'w', encoding='utf-8') as f:
                json.dump(player_data, f, ensure_ascii=False, indent=2)
            
            return True
            
        except Exception as e:
            print(f"移除物品时出错: {e}")
            return False
    
    def use_consumable(self, item_name: str) -> Optional[Dict]:
        """使用消耗品"""
        try:
            with open(self.player_character_file, 'r', encoding='utf-8') as f:
                player_data = json.load(f)
            
            # 查找消耗品
            if "items" in player_data["equipment"]:
                for item in player_data["equipment"]["items"]:
                    if item["name"] == item_name and item.get("type") == "药水":
                        # 使用消耗品
                        if self.remove_item(item_name, 1):
                            return item
                        break
            
            return None
            
        except Exception as e:
            print(f"使用消耗品时出错: {e}")
            return None
    
    def equip_item(self, item_name: str, slot: str) -> bool:
        """装备物品"""
        try:
            with open(self.player_character_file, 'r', encoding='utf-8') as f:
                player_data = json.load(f)
            
            # 查找物品
            item = self._find_item(player_data, item_name)
            if not item:
                return False
            
            # 装备到指定槽位
            if slot == "weapon":
                # 装备武器
                if "equipped_weapon" not in player_data["equipment"]:
                    player_data["equipment"]["equipped_weapon"] = {}
                player_data["equipment"]["equipped_weapon"] = item
                
            elif slot == "armor":
                # 装备护甲
                player_data["equipment"]["armor"] = item
                
            elif slot == "shield":
                # 装备盾牌
                player_data["equipment"]["shield"] = item
            
            # 保存更新
            with open(self.player_character_file, 'w', encoding='utf-8') as f:
                json.dump(player_data, f, ensure_ascii=False, indent=2)
            
            return True
            
        except Exception as e:
            print(f"装备物品时出错: {e}")
            return False
    
    def _find_item(self, player_data: Dict, item_name: str) -> Optional[Dict]:
        """查找物品"""
        # 在武器中查找
        if "weapons" in player_data["equipment"]:
            for weapon in player_data["equipment"]["weapons"]:
                if weapon["name"] == item_name:
                    return weapon
        
        # 在物品中查找
        if "items" in player_data["equipment"]:
            for item in player_data["equipment"]["items"]:
                if item["name"] == item_name:
                    return item
        
        return None
    
    def get_equipment_summary(self) -> Dict:
        """获取装备摘要"""
        try:
            with open(self.player_character_file, 'r', encoding='utf-8') as f:
                player_data = json.load(f)
            
            equipment = player_data.get("equipment", {})
            inventory = player_data.get("inventory", {})
            
            summary = {
                "weapons": len(equipment.get("weapons", [])),
                "armor": equipment.get("armor", {}).get("name", "无"),
                "shield": equipment.get("shield", {}).get("name", "无"),
                "items": len(equipment.get("items", [])),
                "gold": inventory.get("gold", 0),
                "magic_items": len(inventory.get("magic_items", [])),
                "gems": len(inventory.get("gems", []))
            }
            
            return summary
            
        except Exception as e:
            print(f"获取装备摘要时出错: {e}")
            return {}
    
    def auto_organize_inventory(self) -> bool:
        """自动整理库存"""
        try:
            with open(self.player_character_file, 'r', encoding='utf-8') as f:
                player_data = json.load(f)
            
            # 整理物品分类
            if "items" in player_data["equipment"]:
                organized_items = []
                consumables = []
                ammunition = []
                tools = []
                
                for item in player_data["equipment"]["items"]:
                    item_type = item.get("type", "misc")
                    if item_type == "药水":
                        consumables.append(item)
                    elif item_type == "弹药":
                        ammunition.append(item)
                    elif item_type == "工具":
                        tools.append(item)
                    else:
                        organized_items.append(item)
                
                # 重新组织物品列表
                player_data["equipment"]["items"] = organized_items + consumables + ammunition + tools
            
            # 保存更新
            with open(self.player_character_file, 'w', encoding='utf-8') as f:
                json.dump(player_data, f, ensure_ascii=False, indent=2)
            
            return True
            
        except Exception as e:
            print(f"自动整理库存时出错: {e}")
            return False

# 便捷函数
def add_loot(loot_items: List[Dict]) -> bool:
    """添加战利品"""
    manager = LootManager()
    return manager.add_loot(loot_items)

def remove_item(item_name: str, quantity: int = 1) -> bool:
    """移除物品"""
    manager = LootManager()
    return manager.remove_item(item_name, quantity)

def use_consumable(item_name: str) -> Optional[Dict]:
    """使用消耗品"""
    manager = LootManager()
    return manager.use_consumable(item_name)

def equip_item(item_name: str, slot: str) -> bool:
    """装备物品"""
    manager = LootManager()
    return manager.equip_item(item_name, slot)
