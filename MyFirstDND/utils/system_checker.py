#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DND跑团库 - 系统检查器
验证系统完整性，确保所有组件正常工作
"""

import json
import os
import sys
from typing import Dict, List, Tuple

class SystemChecker:
    """系统检查器 - 验证DND跑团库完整性"""
    
    def __init__(self, data_path: str = "."):
        """初始化检查器"""
        self.data_path = data_path
        self.required_files = [
            "characters/player_character.json",
            "combat/combat_history.json",
            "combat/balance_analysis.json",
            "items/equipment_database.json",
            "monsters/monster_manual.json",
            "adventures/adventure_log.json",
            "config/game_config.json",
            "config/balance_rules.json",
            "rules/dnd_rules.json",
            "rules/dice_roller.py"
        ]
        
        self.required_directories = [
            "characters",
            "combat",
            "items",
            "monsters",
            "adventures",
            "config",
            "rules",
            "utils"
        ]
        
        self.required_utils = [
            "utils/combat_recorder.py",
            "utils/loot_manager.py",
            "utils/auto_combat_system.py",
            "utils/game_analyzer.py",
            "utils/balance_adjuster.py"
        ]
    
    def check_system_integrity(self) -> Dict:
        """检查系统完整性"""
        results = {
            "overall_status": "unknown",
            "file_checks": {},
            "directory_checks": {},
            "utility_checks": {},
            "data_validation": {},
            "recommendations": []
        }
        
        # 检查目录
        results["directory_checks"] = self._check_directories()
        
        # 检查必需文件
        results["file_checks"] = self._check_required_files()
        
        # 检查工具脚本
        results["utility_checks"] = self._check_utility_scripts()
        
        # 验证数据完整性
        results["data_validation"] = self._validate_data_files()
        
        # 确定整体状态
        results["overall_status"] = self._determine_overall_status(results)
        
        # 生成建议
        results["recommendations"] = self._generate_recommendations(results)
        
        return results
    
    def _check_directories(self) -> Dict:
        """检查必需目录"""
        results = {}
        
        for directory in self.required_directories:
            dir_path = os.path.join(self.data_path, directory)
            exists = os.path.exists(dir_path)
            is_dir = os.path.isdir(dir_path) if exists else False
            
            results[directory] = {
                "exists": exists,
                "is_directory": is_dir,
                "status": "✅" if exists and is_dir else "❌"
            }
        
        return results
    
    def _check_required_files(self) -> Dict:
        """检查必需文件"""
        results = {}
        
        for file_path in self.required_files:
            full_path = os.path.join(self.data_path, file_path)
            exists = os.path.exists(full_path)
            readable = os.access(full_path, os.R_OK) if exists else False
            
            results[file_path] = {
                "exists": exists,
                "readable": readable,
                "status": "✅" if exists and readable else "❌"
            }
        
        return results
    
    def _check_utility_scripts(self) -> Dict:
        """检查工具脚本"""
        results = {}
        
        for script_path in self.required_utils:
            full_path = os.path.join(self.data_path, script_path)
            exists = os.path.exists(full_path)
            readable = os.access(full_path, os.R_OK) if exists else False
            
            # 检查文件内容是否完整
            content_valid = False
            if exists and readable:
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # 检查是否包含基本的Python语法
                        content_valid = 'class' in content or 'def' in content
                except Exception:
                    content_valid = False
            
            results[script_path] = {
                "exists": exists,
                "readable": readable,
                "content_valid": content_valid,
                "status": "✅" if exists and readable and content_valid else "❌"
            }
        
        return results
    
    def _validate_data_files(self) -> Dict:
        """验证数据文件完整性"""
        results = {}
        
        # 检查角色数据
        character_file = os.path.join(self.data_path, "characters/player_character.json")
        if os.path.exists(character_file):
            try:
                with open(character_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                required_fields = ["character_info", "ability_scores", "combat_stats", "equipment"]
                validation = {}
                
                for field in required_fields:
                    validation[field] = field in data
                
                results["player_character"] = {
                    "valid_json": True,
                    "required_fields": validation,
                    "status": "✅" if all(validation.values()) else "⚠️"
                }
                
            except Exception as e:
                results["player_character"] = {
                    "valid_json": False,
                    "error": str(e),
                    "status": "❌"
                }
        else:
            results["player_character"] = {
                "valid_json": False,
                "error": "文件不存在",
                "status": "❌"
            }
        
        # 检查战斗历史
        combat_file = os.path.join(self.data_path, "combat/combat_history.json")
        if os.path.exists(combat_file):
            try:
                with open(combat_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                results["combat_history"] = {
                    "valid_json": True,
                    "has_sessions": "combat_sessions" in data,
                    "has_statistics": "statistics" in data,
                    "status": "✅"
                }
                
            except Exception as e:
                results["combat_history"] = {
                    "valid_json": False,
                    "error": str(e),
                    "status": "❌"
                }
        else:
            results["combat_history"] = {
                "valid_json": False,
                "error": "文件不存在",
                "status": "❌"
            }
        
        return results
    
    def _determine_overall_status(self, results: Dict) -> str:
        """确定整体状态"""
        # 计算各部分的通过率
        dir_count = len(results["directory_checks"])
        file_count = len(results["file_checks"])
        utility_count = len(results["utility_checks"])
        data_count = len(results["data_validation"])
        
        dir_passed = sum(1 for check in results["directory_checks"].values() if check["status"] == "✅")
        file_passed = sum(1 for check in results["file_checks"].values() if check["status"] == "✅")
        utility_passed = sum(1 for check in results["utility_checks"].values() if check["status"] == "✅")
        data_passed = sum(1 for check in results["data_validation"].values() if check["status"] == "✅")
        
        # 计算总体通过率
        total_checks = dir_count + file_count + utility_count + data_count
        total_passed = dir_passed + file_passed + utility_passed + data_passed
        pass_rate = total_passed / total_checks if total_checks > 0 else 0
        
        if pass_rate >= 0.9:
            return "🟢 系统正常"
        elif pass_rate >= 0.7:
            return "🟡 基本正常"
        elif pass_rate >= 0.5:
            return "🟠 部分正常"
        else:
            return "🔴 系统异常"
    
    def _generate_recommendations(self, results: Dict) -> List[str]:
        """生成修复建议"""
        recommendations = []
        
        # 检查目录问题
        for dir_name, check in results["directory_checks"].items():
            if not check["exists"]:
                recommendations.append(f"创建目录: {dir_name}")
            elif not check["is_directory"]:
                recommendations.append(f"确保 {dir_name} 是一个目录")
        
        # 检查文件问题
        for file_path, check in results["file_checks"].items():
            if not check["exists"]:
                recommendations.append(f"创建文件: {file_path}")
            elif not check["readable"]:
                recommendations.append(f"检查文件权限: {file_path}")
        
        # 检查工具问题
        for script_path, check in results["utility_checks"].items():
            if not check["exists"]:
                recommendations.append(f"创建脚本: {script_path}")
            elif not check["readable"]:
                recommendations.append(f"检查文件权限: {script_path}")
            elif not check["content_valid"]:
                recommendations.append(f"检查脚本内容: {script_path}")
        
        # 检查数据问题
        for data_name, check in results["data_validation"].items():
            if not check.get("valid_json", False):
                recommendations.append(f"修复JSON格式: {data_name}")
        
        if not recommendations:
            recommendations.append("系统状态良好，无需修复")
        
        return recommendations
    
    def generate_report(self) -> str:
        """生成系统检查报告"""
        results = self.check_system_integrity()
        
        report = []
        report.append("=" * 60)
        report.append("DND跑团库 - 系统完整性检查报告")
        report.append("=" * 60)
        report.append(f"检查时间: {self._get_timestamp()}")
        report.append(f"整体状态: {results['overall_status']}")
        
        # 添加通过率信息
        total_checks = len(results["directory_checks"]) + len(results["file_checks"]) + len(results["utility_checks"]) + len(results["data_validation"])
        total_passed = sum(1 for check in results["directory_checks"].values() if check["status"] == "✅")
        total_passed += sum(1 for check in results["file_checks"].values() if check["status"] == "✅")
        total_passed += sum(1 for check in results["utility_checks"].values() if check["status"] == "✅")
        total_passed += sum(1 for check in results["data_validation"].values() if check["status"] == "✅")
        pass_rate = (total_passed / total_checks * 100) if total_checks > 0 else 0
        
        report.append(f"通过率: {total_passed}/{total_checks} ({pass_rate:.1f}%)")
        report.append("")
        
        # 目录检查结果
        report.append("📁 目录检查:")
        for dir_name, check in results["directory_checks"].items():
            status = check["status"]
            report.append(f"  {status} {dir_name}")
        report.append("")
        
        # 文件检查结果
        report.append("📄 文件检查:")
        for file_path, check in results["file_checks"].items():
            status = check["status"]
            report.append(f"  {status} {file_path}")
        report.append("")
        
        # 工具检查结果
        report.append("🔧 工具检查:")
        for script_path, check in results["utility_checks"].items():
            status = check["status"]
            details = []
            if check["exists"]:
                details.append("存在")
                if check["readable"]:
                    details.append("可读")
                    if check["content_valid"]:
                        details.append("内容有效")
                    else:
                        details.append("内容无效")
                else:
                    details.append("不可读")
            else:
                details.append("不存在")
            
            report.append(f"  {status} {script_path} ({', '.join(details)})")
        report.append("")
        
        # 数据验证结果
        report.append("📊 数据验证:")
        for data_name, check in results["data_validation"].items():
            status = check["status"]
            report.append(f"  {status} {data_name}")
        report.append("")
        
        # 修复建议
        report.append("💡 修复建议:")
        for recommendation in results["recommendations"]:
            report.append(f"  • {recommendation}")
        report.append("")
        
        report.append("=" * 60)
        
        return "\n".join(report)
    
    def _get_timestamp(self) -> str:
        """获取当前时间戳"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 便捷函数
def check_system() -> Dict:
    """检查系统完整性"""
    checker = SystemChecker()
    return checker.check_system_integrity()

def generate_report() -> str:
    """生成系统检查报告"""
    checker = SystemChecker()
    return checker.generate_report()

# 命令行使用
if __name__ == "__main__":
    checker = SystemChecker()
    report = checker.generate_report()
    print(report)
