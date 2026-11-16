# 规格写模态抽屉时写成整区拖拽跟手，子组件返回键分支写进 @Entry 页规格

审的是：规格
触发（任一种）：
- 读到：源码 `ModalNavigationDrawer(gesturesEnabled = true)`；写错的样子：规格写成「抽屉手势从屏幕边缘滑出」「边缘右滑」，转换决策只给 SideBarContainer 或自定义滑出面板，没写开合行为
- 读到：源码子组件里有 `BackHandler(drawerState.isOpen) { … }`，目标合并成单 Navigation、只有 @Entry 页有 onBackPress；写错的样子：@Entry 页规格的 onBackPress 转换决策只列退出确认的几种模式，没有「抽屉开着先关抽屉」分支；这条要求只写在别的页面规格里，写给「宿主页 onBackPress」
适用范围：规格提取阶段描述模态抽屉和返回键处理时
做法：
- 描述 ModalNavigationDrawer(gesturesEnabled = true) 时写明：整个内容区横向拖拽跟手开合，子组件的横向手势优先；不写成边缘滑出
- 子组件拿不到返回键时，在 @Entry 页的规格里写出子组件 BackHandler 的分支和顺序：出栈 → 关抽屉 → 退出确认
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onBackPress?(): void | boolean 只对 @Entry 装饰的自定义组件生效，返回 true 表示页面自己处理：子组件里写 onBackPress 收不到返回键，分支要归到 @Entry 页（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CustomComponent.onBackPress）
- 出栈后、退出确认前加抽屉开合判断：修复后的返回键顺序（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-be2a579e8fcdcb8b0a16（jerboa）：做法第 1 步 ← 建议 4；做法第 2 步 ← 建议 4；取值 2 ← 诊断
