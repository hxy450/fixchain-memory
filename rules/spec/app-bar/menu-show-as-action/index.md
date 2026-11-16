# 菜单项的 android:showAsAction 和溢出菜单

agent 会看到什么：菜单 XML 的 <item> 用 android:showAsAction（ifRoom、never，带 tools:ignore="AppCompatResource"），溢出项由平台主题的下拉面板承载，规格写成 ActionBar 图标按钮、或只写「Menu + MenuItem」一行

## 规矩

- rule-b42ed5f3b85a｜AppCompat 菜单项用 android:showAsAction 时，规格写成溢出菜单，不写成图标｜读到：菜单 XML 的 <item> 用 android:showAsAction="ifRoom" 并带 tools:ignore="AppCompatResource"；写错：规格写「ActionBar 图标按钮形态，置于标题栏右侧」或「showAsAction=ifRoom 的图标按钮，等价 ActionBar」
- rule-606599fecd83｜框架 ActionBar 有 showAsAction=never 项时，规格给溢出面板写可见契约｜读到：菜单 XML 里有 android:showAsAction="never" 的项；Activity 用框架 ActionBar，主题 parent=android:Theme.Holo 一类平台主题，源码里没有面板样式；写错：规格只写「溢出菜单（Menu + MenuItem）」一行，没写面板底色与边线、宽度、行高、字号与左右内边距、行间分隔线、有无圆角、锚定位置，也没写点外部与返回键的模态语义
- rule-761f5febfd20｜要求一比一而源端是 Holo 下拉面板时，规格把溢出菜单定为页内浮层，不只写通用 Menu 映射｜读到：showAsAction="never" 的项由平台主题绘制的下拉面板（ListPopupWindow）承载；任务要求与源端逐屏一致；写错：转换决策沿用通用映射「PopupMenu → Menu + MenuItem」，没写系统 Menu 与 Holo 面板在形状、分隔线、定位上的差异，也没定替代承载方式
- rule-5e21794a263a｜源 ActionBar 菜单有 ifRoom 项时，规格按框架分配规则写上栏结果，不简写成进图标位｜读到：源 Activity 用平台主题的窗口 ActionBar（非 AppCompat，android:showAsAction 生效），菜单 XML 有 showAsAction="ifRoom" 项；写错：规格、feature-base 或派工写「always/ifRoom 带图标的项进图标位、never 进溢出」，没有名额、溢出钮预留、半屏宽度预算和横竖屏重算
- rule-cffd9244c1dc｜页面规格登记菜单时写明每项 showAsAction、缺省值、子菜单和宽度规则，不用 bindMenu 一句话代替｜读到：源菜单 XML 各项带 app:showAsAction、orderInCategory，有 <menu/> 子菜单，ActionMode 复用同一菜单；写错：页面规格只登记菜单 id 清单和显隐规则，用「标题栏 actions + bindMenu / Menu 组件」「自管多选状态 + 条件渲染操作栏」一句话代替，没有 showAsAction、缺省值、子菜单结构和宽度规则
