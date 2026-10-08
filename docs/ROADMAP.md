# 路线图（ROADMAP）

> 状态会随开发推进更新。**世界观内容**见 [`../WORLDVIEW.md`](../WORLDVIEW.md)。

## 里程碑

### M0 · 引擎骨架（已完成）
- [x] 单例：Settings / LLMClient / Story / CharacterDB / MinigameHost / ModManager / SaveSystem
- [x] 场景流转：boot → title → setup_first_run / novel
- [x] 三个内置小游戏（memory / sequence / quickjudge）
- [x] 世界观包导入与安全校验
- [x] 程序化美术（`tools/make_art.py`）
- [x] 自检 `selftest`（55+ 项）与导入安全 `modtest`（25 项）

### M1 · 内容与体验打磨
- [ ] 第一章《苇汀的最后一小时》全量节点写入 `story.json`
- [ ] 送行对话的信息补全式玩法规则落地（见 `STORY_FORMAT.md` §4）
- [ ] 立绘情绪切换（neutral/happy/sad/…）与转场动画
- [ ] 存档 UI、章节选择、设置界面完善
- [ ] 听廊（角色日常对话）与「合音度」轻量系统

### M2 · 生态上线
- [ ] 世界观包索引站（`registry.json` + 审核后台）
- [ ] 审核流水线落地（硬规则 → 分类器 → LLM 灰区 → 人工）
- [ ] 投稿 / 申诉 / 举报入口
- [ ] 分级标签与触发警告在游戏内展示

### M3 · 玩法扩展
- [ ] 构演厅（玩家自制副本编辑器）
- [ ] 联演协议（包分发 / 订阅）
- [ ] 第二章、第三章主线
- [ ] 跨阵营声望、小队编成、战斗数值体系

### M4 · 长期
- [ ] 先声 / 循环 / 白页身世等总悬念逐章释放
- [ ] 默海地图扩展
- [ ] 白噪结社路线分裂（缓声派 / 消音派）
- [ ] 赛季机制（深响频段潮汐表）

## 待决项（Need Decision）

1. 包内 `README.md` 随 zip 分发 → 引擎白名单加入 `md`/`txt`（见 `PACK_FORMAT.md` §4）。
2. 索引站是否远程审核 + 自动收录，还是纯人工 PR。
3. 是否上架 Steam（涉及 loot box 概率公示）。
4. 战斗是纯塔防还是塔防 + 轻量 Roguelike。