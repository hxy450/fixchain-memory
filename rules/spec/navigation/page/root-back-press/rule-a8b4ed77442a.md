# 源端任务根页无返回处理时，规格把栈底退后台锚到栈底页 onBackPressed，不写“系统默认”

审的是：规格
触发（任一种）：
- 读到：源端任务根 Activity（首启引导、主菜单等）没有覆写 onBackPressed，或抽屉关闭时调 super.onBackPressed()；目标入口 @Entry 页是空内容的 Navigation 宿主，启动时 pushPathByName 压入首个 NavDestination；写错的样子：规格的 AC 或契约写“源端无返回拦截照搬”“系统返回默认”“抽屉关→false（走默认）＝退后台”，没写由哪个回调实现退后台
适用范围：规格提取时，源端任务根页没有返回处理、目标端该页是 Navigation 首次 push 的栈底 NavDestination
做法：
- AC 写成“栈深 ≤ 1 时按返回退到后台”，实现锚点写到每个可能成为栈底的页面（冷启首页、首启引导页等）的 NavDestination.onBackPressed，或它们转调的共享裁决函数
- 同时注明：ArkUI 默认会出栈露出空白宿主，@Entry 的 onBackPress 收不到；不写“系统返回默认”“默认退后台”
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onBackPressed 返回 false 表示回退到上一个页面：不写回调或返回 false，栈底页也会被出栈（出处：ts-basic-components-navdestination.md，onBackPressed）
- 栈深为 1 时返回先交栈顶 NavDestination，未消费就由 Navigation 出栈，露出空白宿主，@Entry 的 onBackPress 不会收到：“默认”不等于退后台（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-4da27202d292222a1bb5（Privacy Friendly 2048）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1、诊断；取值 2 ← 诊断
