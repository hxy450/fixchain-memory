# 入口 onCreate 里 super.onCreate 之前的调用，连同首帧前生效的时机写进规格

审的是：规格
触发（任一种）：
- 读到：入口 Activity.onCreate 在 super.onCreate / setContentView 之前调用 setTheme(...) 等；写错的样子：规格只写设置页保存后 setColorMode 即时生效，没写冷启动时首帧前恢复主题，也没指定目标承接位置；这一时机只留在设计参考里
适用范围：规格提取阶段读入口 Activity.onCreate、写功能契约时
做法：
- 把 super.onCreate / setContentView 之前的调用和「首帧前生效」写进功能契约，并指定目标承接位置：EntryAbility.onCreate，在 onWindowStageCreate 的 loadContent 之前
来源：1 张卡，1 个应用
- case-cc22f6cc1041c8cc1129（MifareClassicTool）：做法第 1 步 ← 建议 3
