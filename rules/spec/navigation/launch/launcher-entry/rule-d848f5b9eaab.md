# 跳板带 FLAG_ACTIVITY_CLEAR_TOP 时，规格写明它生效的进入场景，不写成「根页天然唯一」

审的是：规格
触发（任一种）：
- 读到：LAUNCHER 跳板 Activity 按条件 startActivity 后 finish，跳往主页的 Intent 带 addFlags(FLAG_ACTIVITY_CLEAR_TOP)；写错的样子：规格把 CLEAR_TOP 映射成「主页是 Navigation 根页、天然栈内唯一，无需显式清栈即可满足语义」，没写它在哪种进入场景生效、生效后清掉哪些页面
适用范围：规格提取阶段，把路由跳板 Activity 的 Intent flag 映射成目标入口行为的那一节
做法：
- 跳板的每个 Intent flag 都写出可观察后果；CLEAR_TOP 写成「主页已在任务栈中时（运行中从桌面图标再次进入）清掉主页之上的页面并回到主页」
- 不用「冷启时根页天然唯一」消解只在目标页已在栈中才生效的 flag；写出目标端承载这一场景的位置（单例 UIAbility 的 onNewWant）
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- FLAG_ACTIVITY_CLEAR_TOP：被启动的 Activity 已在当前任务中运行时，不新建实例，而是关掉它上面的所有 Activity，Intent 交给这个旧实例：这个 flag 只在目标页已在栈中时才起作用，冷启时没有可清的页面（出处：android.content.Intent#FLAG_ACTIVITY_CLEAR_TOP）
来源：1 张卡，1 个应用
- case-41dfb6f341d11578323a（Privacy Friendly 2048）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1、建议 2
