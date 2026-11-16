# 源端返回键按来源标志分支时，返回按钮和 onBackPressed 共用同一分支，不默认 pop

审的是：代码
触发（任一种）：
- 读到：Activity 里返回按钮点击和 onBackPressed() 按启动来源标志分支：标志为真时执行别的动作（如添加默认项并进入主页），否则 finish()；写错的样子：目标返回按钮无条件 navPathStack.pop()，NavDestination 上没有 .onBackPressed(...)，来源标志分支丢失
适用范围：把 Activity 的返回键、onBackPressed 迁成 ArkUI NavDestination 时
做法：
- 先列出源端返回键点击、onBackPressed 和各成功、失败回调的去向（finish、跳主页、Toast）
- 写一个 handleBack()：来源标志为真时照源码执行，否则 pop；标题栏返回按钮调它，NavDestination 写 .onBackPressed(() => { this.handleBack(); return true; })
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onBackPressed(callback: () => boolean): NavDestinationAttribute：NavDestination 拦截系统返回（出处：鸿蒙 SDK 的 ets/component/nav_destination.d.ts，NavDestinationAttribute.onBackPressed）
- 回调返回 true 表示重写返回键逻辑，返回 false 表示回退到上一个页面：自己处理了返回就要返回 true（出处：ts-basic-components-navdestination.md，onBackPressed）
- 新增来源标志状态和 handleBack，返回按钮与 onBackPressed 共用：修好的写法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-766f31f27e3feb426eb4（app_hnaccurateweather_live_android）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1、诊断；取值 3 ← 诊断
