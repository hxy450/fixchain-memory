# 共享组件表的行指向安卓 item 布局时，组件按该布局逐项还原，缺材料就不生成

审的是：代码
触发（任一种）：
- 读到：共享组件表的行写着安卓来源：某个 Adapter 类及其 item 布局（layout/item_*.xml），或页面规格里的 UI 锚点；写错的样子：公共组件里的行组件只是 Row/Column 套几段 Text，字号、颜色、内边距是自拟的固定值，缺 item 布局里的容器尺寸、背景图、标签文字、复制或编辑删除这类图标按钮
适用范围：基础层按共享组件表生成公共组件（列表行、卡片、弹窗、表单、头部）时，表里给了安卓布局或页面规格来源的那些行
做法：
- 按表逐行打开所列 item 布局和页面规格的 UI 锚点，把容器尺寸（dp 写成数值，即 vp）、背景图（$r('app.media.…')）、标签文字（$r('app.string.…')）、字号（sp 写成 fontSize 的数值，即 fp）和颜色、图标按钮逐项写进组件
- 没打开或材料缺失的行不生成组件，在缺口登记里记下这一行，不写简化占位；已写下的无依据组件整份删掉
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 数值不带单位时默认单位是 vp（屏幕密度相关像素）：安卓 dp 尺寸写成不带单位的数值即可（出处：ts-pixel-units.md，基本像素单位）
- fontSize(value: number | string | Resource): TextAttribute；传 number 时单位是 fp：安卓 sp 字号写成 fontSize 的数值；fp 随系统字体大小设置变化（出处：鸿蒙 SDK 的 ets/component/text.d.ts，TextAttribute.fontSize；ts-pixel-units.md，基本像素单位）
- $r(value: string, ...params: any[]): Resource；value 写成 'app.string.名' 或 'app.media.名'：文案和图片引用已迁入的正式资源（出处：鸿蒙 SDK 的 ets/component/common.d.ts，$r）
针对本应用要查的：
- 每个组件对应的安卓结构和取值：共享组件表这一行写的 Adapter 所用的 item 布局 XML，和页面规格里同一组件的 UI 锚点；逐个读出根容器的高度和背景、每个 TextView 的文字/字号/颜色、每个 ImageView/按钮的图标，一项对一项写进组件
未核实：dp 写成 vp 数值、sp 写成 fp 数值是按单位定义推的，卡里没有上机比对
来源：1 张卡，1 个应用
- case-8f39b7ae0d79870e9ad8（掌上燃气管家）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1、诊断
