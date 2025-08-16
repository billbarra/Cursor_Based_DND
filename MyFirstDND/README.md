# 🎮 Cursor_Based_DND - 与Cursor对话式跑团

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![DND 5e](https://img.shields.io/badge/DND-5e-red.svg)](https://dnd.wizards.com/)

**简单开始：告诉AI "我想开始DND跑团" 即可开始冒险！**

这是一个专为与Cursor AI助手进行DND跑团而设计的完整系统。AI会自动处理所有技术细节，你只需要专注于游戏体验。

## 🌟 项目特色

- 🎯 **完全开源** - MIT许可证，自由使用和修改
- 🤖 **AI驱动** - 专为Cursor AI优化，自动化程度高
- 🌍 **多语言支持** - 中文和英文版本
- 🎲 **DND 5e标准** - 遵循官方规则，兼容性强
- 📊 **数据驱动** - 智能平衡系统，动态调整难度

## 🎯 系统特色

- **智能战斗平衡**：自动分析战斗数据，动态调整难度
- **完整角色管理**：属性、装备、技能、buff一体化管理
- **回合历史追踪**：详细记录每回合操作，便于回顾和分析
- **动态物品系统**：根据战斗表现智能分配装备和法术
- **数据驱动设计**：所有游戏数据都基于实际表现进行调整

## 📁 文件结构

```
MyFirstDND/
├── README.md                 # 项目说明文档
├── config/
│   ├── game_config.json     # 游戏基础配置
│   └── balance_rules.json   # 平衡性规则配置
├── characters/
│   ├── player_character.json # 玩家角色数据
│   └── character_templates/  # 角色模板
├── combat/
│   ├── combat_history.json  # 战斗历史记录
│   ├── balance_analysis.json # 战斗平衡性分析
│   └── encounter_logs/      # 遭遇战详细记录
├── items/
│   ├── equipment_database.json # 装备数据库
│   ├── spell_database.json    # 法术数据库
│   └── loot_tables.json       # 战利品表
├── monsters/
│   ├── monster_manual.json    # 怪物图鉴
│   └── encounter_builder.json # 遭遇战构建器
├── adventures/
│   ├── adventure_log.json     # 冒险日志
│   └── quest_tracker.json     # 任务追踪器
├── rules/
│   ├── dnd_rules.json        # DND规则引擎
│   └── dice_roller.py        # 骰子系统
└── utils/
    ├── game_analyzer.py      # 游戏数据分析器
    └── balance_adjuster.py   # 平衡性调整器
```

## 🚀 使用方法

1. **开始游戏**：告诉AI "我想开始DND跑团"
2. **描述行动**：用自然语言描述你想做什么
3. **选择选项**：AI会提供带序号的选项，回复数字即可
4. **享受游戏**：AI自动处理所有数据更新和记录

**示例：**
- 你："我想开始DND跑团"
- AI：提供选项（1. 创建角色 2. 开始冒险 3. 查看状态）
- 你："1"
- AI：自动创建角色并开始游戏

## 🎲 核心机制

### 战斗平衡系统
- 记录每场战斗的回合数、伤害输出、难度感受
- 分析玩家表现，自动调整后续遭遇战难度
- 智能分配战利品，确保游戏体验的平衡性

### 角色成长系统
- 基于战斗表现解锁新技能和装备
- 动态调整角色能力，保持挑战性
- 个性化发展路径，适应不同游戏风格

### 数据追踪系统
- 详细记录所有游戏决策和结果
- 提供数据可视化，帮助理解游戏进程
- 支持多角色、多冒险的数据管理

## 🔧 技术特性

- **完全自动化**：AI自动处理所有数据更新和记录
- **智能平衡**：根据表现自动调整游戏难度
- **序号选项**：AI提供带序号的选项，你只需回复数字
- **无需手动编辑**：所有文件由AI自动管理

## 🎯 现在开始

**只需要说：**
> "我想开始DND跑团！"

**AI会自动：**
- ✅ 创建你的角色
- ✅ 设置初始装备  
- ✅ 开始冒险世界
- ✅ 处理所有数据

**开始你的DND冒险之旅吧！** 🗡️⚔️🛡️

## 🚀 快速开始

### 方法1：直接下载
```bash
# 克隆仓库
git clone https://github.com/billbarra/Cursor_Based_DND.git

# 进入目录
cd Cursor_Based_DND

# 检查系统完整性
python utils/system_checker.py
```

### 方法2：下载ZIP
1. 点击右上角绿色 "Code" 按钮
2. 选择 "Download ZIP"
3. 解压到本地目录
4. 运行系统检查

## 🤝 贡献

我们欢迎所有形式的贡献！

- 🐛 **报告Bug** - [创建Issue](https://github.com/billbarra/Cursor_Based_DND/issues)
- 💡 **建议功能** - [参与讨论](https://github.com/billbarra/Cursor_Based_DND/discussions)
- 🔧 **提交代码** - [查看贡献指南](CONTRIBUTING.md)
- 📚 **改进文档** - 帮助完善说明文档
- 🌍 **翻译支持** - 添加更多语言版本

## 📄 许可证

本项目采用 [MIT许可证](LICENSE) - 详见LICENSE文件。

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者！

## 📞 支持

- **问题反馈**: [GitHub Issues](https://github.com/billbarra/Cursor_Based_DND/issues)
- **功能讨论**: [GitHub Discussions](https://github.com/billbarra/Cursor_Based_DND/discussions)
- **项目Wiki**: [详细使用指南](https://github.com/billbarra/Cursor_Based_DND/wiki)

---

**⭐ 如果这个项目对你有帮助，请给我们一个星标！**
