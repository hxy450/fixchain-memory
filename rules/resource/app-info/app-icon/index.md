# 应用图标、分层图标和启动窗图标

agent 会看到什么：源 AndroidManifest 的 android:icon 指向 launcher 图标（mipmap、<adaptive-icon> 的 foreground / background），启动画面取图标前景；产物 AppScope / entry media 下的 layered_image、前景背景、startIcon.png 仍是模板图，尺寸不对或没裁可见区，app.json5 的 icon 没指向分层图标

## 通用查法

### 迁应用图标时顺着 android:icon 找源图标各层，生成分层图标和 startIcon

审的是：资源
触发（任一种）：
- 读到：AndroidManifest 的 android:icon 指向 mipmap-anydpi-v26 下的 <adaptive-icon>（<foreground>、<background>）；写错的样子：AppScope / entry media 下 layered_image 引用的前景、背景和 startIcon.png 仍是 DevEco 模板图
- 写错的样子：layered_image.json 引用的两层 PNG 尺寸不一，或前景是 mipmap 全层原样拷贝
适用范围：应用身份落地、资源迁移阶段生成鸿蒙分层图标和启动窗图标时
做法：
- 从 android:icon 顺着引用到 adaptive-icon XML，读 <foreground>、<background> 的 android:drawable：矢量、最高密度 mipmap 的 PNG 或 @color 值
- 前景 PNG 先裁中央 72/108 可见区，前景、背景都生成 1024×1024px（@color 背景填满整张），AppScope 和 entry 两处同名文件都换；startIcon.png 取前景层
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- { "layered-image": { "background": "$media:background", "foreground": "$media:foreground" } }：分层图标资源文件的写法，前景和背景各引用一张图（出处：layered-image.md，配置分层图标）
- 编译时 AppScope 下的资源会覆盖模块下同名资源：AppScope 与 entry 两处的同名图标都要换，否则 AppScope 的模板图生效（出处：layered-image.md，配置优先级和生成策略）
- 前景图：显示大小 450×450px、资源大小 1024×1024px 的透明图层；背景图：1024×1024px：文档推荐的分层图标规格（写在快捷方式 icon 一项里）（出处：module-configuration-file.md，shortcuts 标签的 icon）
- Both foreground and background layers should be sized at 108 x 108 dp；The inner 72 x 72 dp of the icon appears within the masked viewport：源端两层同尺寸，启动器只显示中央 72dp（出处：android.graphics.drawable.AdaptiveIconDrawable（类注释））
针对本应用要查的：
- 源 launcher 图标的前景和背景：源工程 AndroidManifest 的 application android:icon → res/mipmap-anydpi-v26（或 drawable-anydpi-v26）下的 adaptive-icon XML → <foreground>、<background> 引用的矢量、mipmap-*dpi 下的 PNG，或 res/values*/colors.xml 里的 @color；PNG 取最高密度那张，边长 × 2/3 为中央裁切边长（例：xxxhdpi 的 432px 取中央 288px）；@color 取它的色值填满背景
未核实：450/1024px 的推荐尺寸出自快捷方式图标的说明，应用图标是否同一规格未核；鸿蒙桌面整层显示前景是卡里的说法，文档里没有找到原文
来源：3 张卡，2 个应用
- case-0405ee7ad27947343068（2048）：做法第 2 步 ← 建议 1
- case-4f7163b95249e9ede2ca（Cofi）：做法第 1 步 ← 建议 3
- case-6f5f2cf84cd0ea025486（2048）：做法第 2 步 ← 建议 2、建议 1

## 规矩

- rule-debf8580409f｜AppScope 分层图标用安卓 launcher 图标生成，不留模板占位图｜读到：AndroidManifest 的 application android:icon 指向 launcher 图标（drawable 或 mipmap 资源）；写错：AppScope/resources/base/media 下分层图标的 foreground、background 仍是模板占位图
- rule-5480463645fc｜app.json5 用分层图标时，AppScope media 里要有分层图标文件和它引用的前景背景｜读到：资源迁移已在 entry 的 resources/base/media 产出前景、背景（svg 或位图）和 layered_image.json；迁移 skill 只描述从 PNG 提取，源 mipmap 是 webp；写错：app.json5 的 icon 是（或改成了）$media:layered_image，但 AppScope/resources/base/media 下没有 layered_image.json，或者缺它 "layered-image" 里 foreground、background 引用的文件
- rule-f7438d5023db｜app.json5 的 icon 停在脚手架值而 entry 已有分层图标时，改指分层图标｜读到：迁移 skill 或交接给出的 icon 目标值是 $media:layered_image（旁注「(不变)」）；entry 的 module.json5 已是 icon=$media:layered_image，entry media 下有 layered_image.json 和前景、背景文件；写错：AppScope/app.json5 仍是 "icon": "$media:app_icon"，AppScope media 里只有脚手架的 app_icon.png
- rule-507db010ba56｜源端是自适应图标时，layered_image 前景背景和 startIcon 由源图标生成，不留模板｜读到：源工程 mipmap-anydpi-v26/ic_launcher.xml 是 <adaptive-icon>：<foreground> 引用矢量、<background> 引用纯色；写错：AppScope 和 entry 的 media 下 layered_image 引用的 foreground / background PNG 仍是 DevEco 模板（蓝底背景层），startIcon.png 也是模板图；启动图标层只被当普通 drawable 转成 SVG
- rule-ca923192d419｜adaptive-icon 转 layered-image 时，前景和背景生成同尺寸 PNG，纯色底不用小图｜读到：源端 <adaptive-icon> 的 android:background 是 @color/… 纯色（或 108dp 图层），android:foreground 是 @mipmap/… PNG；写错：layered_image.json 引用的 background PNG 是 1×1、108×108 这类小尺寸纯色图，与 foreground PNG（如 432×432）尺寸不一
- rule-6a70f7c49615｜迁移 adaptive-icon 前景时先裁中央 72/108 可见区再缩放，不直接拷 mipmap 全层｜读到：源端 <adaptive-icon> 的 android:foreground 指向 mipmap-*dpi 下 108dp 全层的 PNG；写错：layered_image.json 的 foreground 引用的 PNG 是 mipmap 前景原样拷贝（如 xxxhdpi 的 432×432 没裁剪）
- rule-f502fb0a4ac9｜源 targetSdk≥31 且没写 windowSplashScreen* 时，启动窗图标取自适应图标前景层｜读到：AndroidManifest 的 android:icon 指向 anydpi-v26 下的 <adaptive-icon>（<foreground>、<background>），targetSdkVersion ≥ 31，主题里没有 android:windowSplashScreen* 属性；写错：module.json5 的 startWindowIcon 指向的 startIcon.png 换成了旧版栅格 launcher 图（如方形带底色的 logo），或仍是脚手架图
- rule-5c5421ed80ad｜启动窗图标按源端显示尺寸乘目标密度准备像素，不直接拷贝小尺寸栅格图｜读到：源端启动画面用自适应图标前景层（无底板），targetSdkVersion ≥ 31；写错：startIcon.png 直接拷贝 xxhdpi 的 144px 栅格图，像素远小于启动图标显示尺寸乘目标密度
- rule-e85b7ecd36bb｜adaptive icon 的分层图标前景取 <foreground>，不用 legacy 图标｜读到：源工程 res/mipmap-anydpi*/ 下的 launcher 图标是 <adaptive-icon>，含 <foreground android:drawable=…> 和 <background>；各密度目录另有 legacy 的 ic_launcher.png；写错：layered-image 的 foreground 指向从 legacy ic_launcher.png 拷来的合成图，叠在纯色 background 上
- rule-1e2eda17dbd5｜startWindowIcon 指向的 startIcon.png 仍是模板图时，换成安卓启动图标缩放的图｜读到：安卓有 `mipmap-*/ic_launcher`、`ic_launcher_round` 启动图标（AndroidManifest 的 android:icon / android:roundIcon）；写错：目标 module.json5 的 `startWindowIcon` 指向的 `startIcon.png` 仍是脚手架模板图（尺寸、哈希与模板相同）
