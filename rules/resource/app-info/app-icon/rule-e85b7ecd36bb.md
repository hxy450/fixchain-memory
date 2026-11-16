# adaptive icon 的分层图标前景取 <foreground>，不用 legacy 图标

审的是：资源
触发（任一种）：
- 读到：源工程 res/mipmap-anydpi*/ 下的 launcher 图标是 <adaptive-icon>，含 <foreground android:drawable=…> 和 <background>；各密度目录另有 legacy 的 ic_launcher.png；写错的样子：layered-image 的 foreground 指向从 legacy ic_launcher.png 拷来的合成图，叠在纯色 background 上
适用范围：源端 launcher 用 adaptive icon、迁成鸿蒙分层图标（layered-image）时
做法：
- 前景取 <foreground> 引用的资源：矢量 drawable 转成 SVG，或按 108dp 视窗渲染成位图；背景取 <background> 引用的资源；放进 resources/base/media
- 分层图标 json 写 {"layered-image": {"background": "$media:<背景名>", "foreground": "$media:<前景名>"}}，app.json5 的 icon 引用它
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 前景层和背景层都按 108 x 108 dp，内圈 72 x 72 dp 出现在遮罩视窗里，四边各 18 dp 留给系统效果：adaptive icon 各层的尺寸约定，渲染前景时按这个视窗（出处：android.graphics.drawable.AdaptiveIconDrawable（类注释））
- {"layered-image": {"background": "$media:background", "foreground": "$media:foreground"}}：分层图标资源文件的写法，放在 resources/base/media 下（出处：layered-image.md，配置分层图标和应用名称）
- media 目录支持 .svg：矢量前景转成 SVG 可直接放进 media（出处：resource-categories-and-access.md，资源组目录（表3 图片资源类型说明））
针对本应用要查的：
- adaptive icon 的前景和背景资源：源工程 res/mipmap-anydpi* 下 launcher 图标 XML 的 <foreground>、<background> 的 android:drawable，顺着 @drawable/、@mipmap/、@color/ 找到文件或颜色；矢量 drawable 读 viewportWidth/Height 按 108dp 视窗转换；颜色背景写成纯色图层
来源：1 张卡，1 个应用
- case-d78a91fb9dfa366ec2ee（omni-notes-hmos）：做法第 1 步 ← 建议 5；做法第 2 步 ← 建议 5、诊断
