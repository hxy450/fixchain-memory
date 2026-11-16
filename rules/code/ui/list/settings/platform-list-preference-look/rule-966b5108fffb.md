# 可滚动的 GridView/ListView 迁成 Grid/List 时，显式设滚动条和越界效果

审的是：代码
触发（任一种）：
- 读到：源 GridView / ListView 没写 android:scrollbars、android:overScrollMode，内容超过一屏（行高 × 行数大于可视高度）；写错的样子：Grid 上没有 .scrollBar(...)、.scrollBarWidth(...)、.scrollBarColor(...)、.edgeEffect(...)，沿用 BarState.Auto 和 EdgeEffect.None
适用范围：源列表或网格会滚动、滚动指示和越界效果来自主题与框架默认时
做法：
- 按源端行高 × 行数判断会不会滚动，不按「全部条目应可见」推测
- 逐项显式设置：onPageShow 时 .scrollBar(BarState.On)，约 1200ms 后切回 BarState.Auto（对应进页先亮再淡出）；.scrollBarWidth、.scrollBarColor 按源主题滚动条取；.edgeEffect(EdgeEffect.Spring) 对应安卓 12 起的拉伸回弹
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- scrollBar(value: BarState)：默认 BarState.Auto；scrollBarWidth：默认 4 vp；scrollBarColor：默认 '#182431'（40% opacity）：Grid 的滚动条默认值，进页不亮（出处：鸿蒙 SDK 的 ets/component/grid.d.ts，GridAttribute.scrollBar / scrollBarWidth / scrollBarColor）
- edgeEffect(value: EdgeEffect, options?: EdgeEffectOptions): GridAttribute，默认 EdgeEffect.None：Grid 默认没有越界效果（出处：鸿蒙 SDK 的 ets/component/grid.d.ts，GridAttribute.edgeEffect）
- edgeEffect(value: EdgeEffect, options?: EdgeEffectOptions): ListAttribute，默认 EdgeEffect.Spring；scrollBar 默认 BarState.Auto：同族接口：List 的默认越界已是 Spring，和 Grid 不同（出处：鸿蒙 SDK 的 ets/component/list.d.ts，ListAttribute.edgeEffect / scrollBar）
- initialAwakenScrollBars()：awakenScrollBars(scrollBarDefaultDelayBeforeFade * 4, true)，SCROLL_BAR_DEFAULT_DELAY = 300（ms）：源端视图显示时滚动条先亮 1200ms 再淡出（出处：android.view.View#initialAwakenScrollBars；android.view.ViewConfiguration#SCROLL_BAR_DEFAULT_DELAY）
- mEdgeEffectType = isChangeEnabled(USE_STRETCH_EDGE_EFFECT_BY_DEFAULT) ? TYPE_STRETCH : TYPE_GLOW，该开关 @EnabledSince(targetSdkVersion = BASE)：新平台上越界默认是拉伸（出处：android.widget.EdgeEffect#EdgeEffect）
- Holo 主题下取 scrollBarWidth(4)、scrollBarColor('#7B808080')、onPageShow 先 BarState.On、1200ms 后切回 Auto、edgeEffect(EdgeEffect.Spring)，与安卓录屏一致：修好的写法（色值只对 Holo 主题成立）（出处：卡里修好并验证过）
针对本应用要查的：
- 源主题滚动条的颜色和粗细：Android SDK 平台资源 themes*.xml 里该主题的 scrollbarSize、scrollbarThumbVertical，后者指向 data/res/drawable* 下的图；scrollbarSize 是 dip 数值；滚动条图是九宫格图片，取样读出颜色（例：Holo 下取样为 #7B808080）
来源：1 张卡，1 个应用
- case-ecf6bf1e97fdf99c99a3（Bubble Shooter）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3、诊断；取值 6 ← 诊断、建议 3
