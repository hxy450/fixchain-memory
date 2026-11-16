# Adapter 里自定义 View 的数据绑定被注释时，按未启用处理，只照 XML 静态属性实现

审的是：代码
触发（任一种）：
- 读到：`RecyclerView.Adapter` 的绑定方法里，自定义 View 的 set…Value 一类数据绑定整段被注释，item 布局 XML 只给了颜色等静态自定义属性；写错的样子：目标在 `@Builder` 里按注释掉的逻辑（或 ViewModel 的最大/最小值）用逐项数据算坐标，画出动态折线和实心点，颜色也不是 XML 给的值
适用范围：把 RecyclerView item 里的自定义绘制 View 迁成 ArkUI 组件，源端绑定代码被注释掉时
做法：
- 按「dead/注释代码不迁移」把被注释的绑定视为未启用行为：只照 item XML 的静态属性实现（颜色、位置、尺寸），不根据注释代码或 ViewModel 字段重建动态绘制
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- XML 颜色的水平线加空心节点，温度文本放在顶部块：修复后照静态属性实现的样子（出处：卡里修好并验证过）
针对本应用要查的：
- 自定义 View 在 XML 里配的静态属性：源工程 item 布局 XML 里这个自定义 View 标签上 app: 前缀的属性，以及 res/values/attrs.xml 里它的 declare-styleable 默认值；读出颜色、线宽等值照写；没在 XML 里配的取 declare-styleable 或 View 构造里的默认
来源：1 张卡，1 个应用
- case-04bf2dcacf8602ede15e（app_hnaccurateweather_live_android）：做法第 1 步 ← 建议 1、诊断；取值 1 ← 诊断
