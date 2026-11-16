# 卡片页用了不带 @form 的事件或组件（onAreaChange、Grid）时，改用带 @form 的写法

审的是：代码
触发（任一种）：
- 读到：规格写卡片内用 onSizeChange / 宽度判断驱动条件渲染；写错的样子：卡片页（form_config 的 src 指向的 .ets）上出现 .onAreaChange(...) 或 Grid(...)；编译报 `'onAreaChange' can't support form application`
适用范围：ArkTS 服务卡片的卡片页（FormExtensionAbility 对应的 @Entry 页面）里用到的组件、属性方法和事件
做法：
- 卡片页里用的每个组件、属性方法、事件，在鸿蒙 SDK 的 ets/component 声明里看它最后一段注释（当前版本）有没有 @form；没有的不写进卡片页
- onAreaChange 不带 @form：卡片尺寸改由 FormExtensionAbility 的 onSizeChanged / formProvider.getFormRect 取得，经 updateForm 下发，卡片页用 @LocalStorageProp 接收
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onAreaChange(event: (oldValue: Area, newValue: Area) => void): T（注释里没有 @form）：组件尺寸位置变化回调，不能用在卡片页（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.onAreaChange）
- (scroller?: Scroller, layoutOptions?: GridLayoutOptions): GridAttribute（注释里没有 @form）：Grid 组件，不能用在卡片页（出处：鸿蒙 SDK 的 ets/component/grid.d.ts，GridInterface）
- onClick(event: (event: ClickEvent) => void): T（注释带 @form）：对照：带 @form 的接口可用在卡片页（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.onClick）
- 编译器对卡片页里不带 @form 的接口报 `'onAreaChange' can't support form application`：看到这类报错就说明用了卡片不支持的接口（出处：卡里修好并验证过）
未核实：Grid 在卡片里改用什么写法卡里没有验证（编译门换成 Flex 后不能滚动，卡里未归因）
来源：1 张卡，1 个应用
- case-77c6596fcdf362f9e832（Jetsnack）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 1、建议 2；取值 4 ← 诊断
