# sub_component 子页转成 @Param 嵌入组件，由壳内容区承载，不包 NavDestination

审的是：代码
触发（任一种）：
- 读到：meta.page_type=sub_component，规格写「Fragment，宿主 Activity」「Toolbar 返回 = popBackStack 返回上级」，源码经 addToBackStack 压栈打开；写错的样子：页面写成 NavDestination(){…} 包裹、@Consumer 取 navPathStack、返回时 pop()，并在 pageMap 或路由表里注册了它
适用范围：页面转换阶段转换源端壳内压栈打开的子 Fragment 时
做法：
- 写成普通的 @ComponentV2 组件，参数用 @Param 传入，不包 NavDestination；返回调壳路由的弹出子页入口
- 从 pageMap / 路由表里去掉它的路由，由壳内容区按 tag 渲染这个组件
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- @Param 装饰的变量在初始化自定义组件时从外部传入；没有本地初始值时必须外部传入（配 @Require）：嵌入组件的参数写法（出处：arkts-new-param.md，概述；装饰器说明）
- 子页改为 @Param 嵌入组件，壳内容区按 tag 承载，返回走壳的弹出子页，pageMap 去掉对应路由：返修后的页面形态（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-05f3fb8501654bad9261（AntennaPod）：做法第 1 步 ← 建议 4、诊断；做法第 2 步 ← 诊断；取值 2 ← 诊断
