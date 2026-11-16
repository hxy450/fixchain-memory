# 列表适配器的条目绑定

agent 会看到什么：读到 RecyclerView.Adapter / BaseQuickAdapter 的 onBindViewHolder、convert()、afterBindViewHolder 里对子视图的 setText、图标、背景、颜色和按 viewType 的分支；产物里 ListItem / GridItem / ForEach 条目的文字、图标、样式和列数

## 通用查法

### 列表条目照源端写时，先追到实际的 item 适配器，逐个子视图读绑定再搬

审的是：代码
触发（任一种）：
- 读到：RecyclerView.Adapter / BaseQuickAdapter 的 onBindViewHolder、convert()、afterBindViewHolder 里对子视图调 setText、setImageResource、setBackgroundResource、setTextColor；写错的样子：目标 ListItem / GridItem 的文字、图标、背景和样式是自拟的或只取了接口字段，和源端绑定语句及其分支对不上
适用范围：按安卓列表适配器和 item 布局重建 ArkUI 的 List、Grid 条目时
做法：
- 沿适配器链追到实际渲染条目的适配器（外层适配器里构造的内层适配器、子类的 afterBindViewHolder 都算），打开它的绑定方法和它用的 item 布局 XML
- 逐个子视图读出绑定语句：setText 的模板和全部分支、图标或背景的取法、颜色，以及它调用的格式器和工具方法的实现，照样写进目标条目
针对本应用要查的：
- 条目各子视图实际绑定的值和条件：源工程里实际渲染条目的适配器类的 onBindViewHolder / convert()，以及它用的 item 布局 XML；读各条件分支里 setText、setTextColor、setBackgroundResource 等调用的参数；R.string、R.color、R.drawable 引用再到 res/values、res/drawable 按资源名取具体值
来源：2 张卡，1 个应用
- case-55bbad53c11b2d1b95e6（app_hnaccurateweather_live_android）：做法第 2 步 ← 建议 1
- case-d64f11b7100c739bb292（app_hnaccurateweather_live_android）：做法第 1 步 ← 建议 3；做法第 2 步 ← 诊断

## 规矩

- rule-2dfb65862c72｜Adapter 里 setText 用模板拼接文案时，目标照搬模板和全部分支，不只输出数值｜读到：RecyclerView.Adapter 的绑定方法里 setText 用字符串模板拼接文案（数值前后带固定文字），并按数据取值走不同模板分支（如几个计数都为 0 时换成另一句）；写错：目标里只写数值的 toString() 或只有 `${…}` 插值，缺了源端模板里的固定文字，或少了某个分支
- rule-16a50dc02b25｜按安卓重做列表项时逐个核对子视图绑定，专用时间格式器先读实现再移植｜读到：安卓适配器里时间 TextView 用专用格式器绑定：holder.setText(R.id.…, 格式器.format(startTime, endTime, viewDate, fallback))；写错：目标条目只显示开始时刻 HH:mm 拼出的 timeLabel（全天时显示固定文案），没有移植格式器的同日区间、跨天、昨天 / 明天等分支
- rule-5d752b2193d7｜目标行项新增地址副行时，主行名称为空的回退改成「未知设备」，不再回退到地址｜读到：源列表项只有一个名称 `TextView`：适配器里 name 非空显示 name、否则 `setText` 地址；布局里没有单独的地址行；写错：目标行项首行写 `Text(device.name.length > 0 ? device.name : device.address)`，次行又固定 `Text(device.address)`，名称为空时两行都是同一个 MAC
- rule-19f761f7571c｜源端 Adapter 按 ID 查本地表取图标时，宿主映射也按 ID 解析图标和颜色，不直接用接口 icon｜读到：源端 Adapter 绑定条目时调用显示工具传的是条目里关联对象的 ID（外键），由工具查本地表得到图标和颜色并着色，没有直接用接口返回的图标字段；写错：宿主把列表数据映射成子组件 UI 项时直接取接口返回的 .icon 字段（空值回退默认图），没按 ID 查本地表，也没给子组件传颜色
- rule-2932e9f66dd8｜同一选项在列表和主预览取自不同资源时分别映射，按尺寸选资源只落到主预览｜读到：列表项 Holder 的 onBindView 里 setBackgroundResource(res)，res 是固定的 R.drawable；主预览的 Drawable 另按组件尺寸经 getUrl 拼路径加载 .webp；写错：列表缩略图的 Image($rawfile(...)) 改成调和主预览相同的按尺寸取资源的函数
- rule-aa7f195c151c｜列表有多种 viewType 时逐类核对卡片样式，单一类型的背景不写进共用 Builder｜读到：RecyclerView.Adapter 有多个 getItemViewType 分支，只有某一类（如推广项）的 item 布局里有 android:background="@drawable/…" 的圆角描边背景，普通项布局没有背景；写错：目标端一个 @Builder 同时渲染各类卡片，背景层把那一类的白底 + .border(...) + .borderRadius(...) 写给所有分支
- rule-642835837f09｜列表或翻页网格的选中、当天、周末样式，沿适配器链追到 item 适配器的 convert() 取｜读到：`ViewPager` / `RecyclerView` 的外层适配器里构造内层适配器并传 `R.layout.` 的 item 布局，选中、当天、周末、节日的样式分支写在内层适配器的 `convert()` 里；写错：目标网格的选中态、当天、周末样式是自拟的（如统一灰色星期行、浅色圆形加红字），和 `convert()` 里的分支不符
- rule-a10a761db9f0｜返修重写界面时，列数按 Adapter 实际绑定项、背景按源码选图逻辑、尺寸按源布局｜读到：RecyclerView Adapter 的绑定方法只把列表第 1、2 项绑到两列控件；背景由按状态选图的方法设置；布局里 ImageView 写着 `android:scaleType="fitXY"` 和固定 dp 高度；写错：ArkTS 按截图写成 slice(1, 4) 三列概览，或把按状态切换的背景写成一张固定 Image(...)，高度和 ImageFit 与源布局不同
- rule-76aa9236dfd3｜Adapter 里自定义 View 的数据绑定被注释时，按未启用处理，只照 XML 静态属性实现｜读到：`RecyclerView.Adapter` 的绑定方法里，自定义 View 的 set…Value 一类数据绑定整段被注释，item 布局 XML 只给了颜色等静态自定义属性；写错：目标在 `@Builder` 里按注释掉的逻辑（或 ViewModel 的最大/最小值）用逐项数据算坐标，画出动态折线和实心点，颜色也不是 XML 给的值
- rule-fb135e91f74e｜子类 adapter 在 afterBindViewHolder 改配按钮时，图标、文案和点击一起迁｜读到：子类 adapter 的 afterBindViewHolder 里按条件用另一个 ActionButton 的 configure(按钮, 图标) 改配次级按钮；写错：目标只在 onClick 回调里改成新动作，共享行组件仍按默认画原来的图标和文案
- rule-d9f351c6eab8｜Adapter 有默认状态分支时，按默认分支实现首屏，切换要真的换渲染内容｜读到：Adapter 绑定代码里有默认选中（如趋势/列表切换默认选中趋势、用横向列表画折线），或数据为空时补默认项（如 GridLayoutManager(4) 的网格补 8 个默认项）；写错：目标切换只改文字颜色，两种状态都渲染同一份固定高度的列表；Grid 数据为空时不补默认项，显示空网格
