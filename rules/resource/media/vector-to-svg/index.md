# 矢量图标转 SVG 媒体资源

agent 会看到什么：源 drawable 是 <vector>（android:pathData、viewportWidth / viewportHeight、fillColor 可能是 ?attr）或 <animated-vector>，Compose 用 Icons.Rounded.* 一类命名图标；产物里删掉矢量改用字符，SVG 的 viewBox 取了 dp 尺寸、fill 写成 none，路径凭记忆写，或动画矢量没在 resource-mapping 里标 unmappable

## 规矩

- rule-9da2bd7c6ed1｜Android 矢量 drawable 转成 SVG 媒体资源再引用，不删掉改用字符代替｜读到：源控件 android:src / android:background 引用的 drawable 是 <vector>（带 android:pathData）；写错：目标删掉复制来的矢量 XML，改用「⌫」之类字符；resources/base/media 里没有对应的 .svg
- rule-3b7e8f122e92｜VectorDrawable 转 SVG 时 viewBox 只取 viewport，宽高取去 dp 的显示尺寸｜读到：<vector> 的 android:width / android:height（dp 显示尺寸）和 android:viewportWidth / android:viewportHeight 不相等，如 48dp/24、12dp/24、24dp/960、20×30dp/3×4.5；写错：SVG 根元素的 viewBox 等于 width/height（如 viewBox="0 0 48 48"），path 的 d 仍是原 viewport 坐标；图标只占画布一角或近乎空白
- rule-cd7058d77020｜vector 的 fillColor 是 ?attr 且解析不出时，SVG 写可见默认色并登记，不写成透明｜读到：<path android:fillColor="?attr/…">，引用主题属性；写错：转换脚本的主题属性表没收这个属性，SVG 的 <path> 写成 `fill="none"`，未解析的记录只在转换清单的备注里，映射文档没写
- rule-2db028b72afe｜源端是 animated-vector 时，resource-mapping 记 unmappable，导出起始帧要注明｜读到：源 res/drawable 下根元素是 <animated-vector>，<target> 的 objectAnimator 用 valueFrom / valueTo 改 pathData；写错：resource-mapping 里没有这条的逐资源状态，或导出了同名静态 .svg 却没写 `unmappable`、没注明只含起始帧
- rule-7e4aaa2898bc｜源码引用 Icons.Rounded.* 等命名变体时，SVG 路径从可核来源取，不凭记忆写｜读到：Compose 源码用 Icons.Rounded.Check、Icons.AutoMirrored.Rounded.ArrowBack 这类命名变体引用 Material 图标，工程里没有对应的矢量文件；写错：media 下生成的 SVG 路径是 Filled / baseline 形状（如对勾是直角折线 M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.42z），资源映射表却标称「官方 Rounded」，且没写数据来源
- rule-7dbef480e13c｜给 Compose Icons.* 补 SVG 取 Material Icons，不取 Material Symbols｜读到：Compose 源里 Icons.Outlined.* / Icons.Filled.* 图标，res/drawable 里没有对应文件；资源参考给的下载地址是 materialsymbolsoutlined/{name}/default/24px.svg；写错：media 下补的 SVG 是 viewBox="0 -960 960 960"（Material Symbols 坐标系），或留着 fill="none" 的透明包围盒 path
- rule-c5f25a9fdec8｜从 AAR 字节码重建 Material 图标路径时，映射 PathBuilder 全部方法含 arcTo，未映射就报错｜读到：源码用 `Icons.Outlined.*` / `Icons.Filled.*` 引用 Compose material-icons 矢量，res 下没有对应 drawable；AAR 里的图标是编译进 class 的 PathBuilder 调用（moveTo、curveToRelative、reflectiveCurveTo、arcToRelative、close）；写错：转出的 SVG 里有只移动不绘制的子路径（如 `m-1.5,0` 后直接是下一个 M/m 或路径结束），图标只画出外框
- rule-6f91689cbc0d｜宣告图标转换通过前逐个产物做结构检查，抽样比对要覆盖含弧段的图标｜读到：AAR 里的图标路径是 PathBuilder 调用，转换靠自写字节码解析；写错：映射表写「bbox + 锚点 + 交叉比对 PASS」，抽样只用了不含弧段的图标；产物里有只含 `M`/`m` 的子路径
- rule-7d508dc55b3e｜vector 根带 android:tint 时，烘焙进每个可见 path 的 fill，字面色也换｜读到：<vector> 根写了 android:tint（如 @color/control_checkable_material），path 的 android:fillColor 是字面 #FF000000，另有 android:fillAlpha="0" 的动画用 path；写错：输出 SVG 的可见 path 仍是 fill="#000000"，只有以 @ 或 ? 开头的 fillColor 换成了解析色；映射表登记的颜色和文件里的 fill 不一致
- rule-ad6983f246e5｜源端用 AppCompat 默认返回箭头时，从 AAR 取 pathData 生成 media svg｜读到：源码 `setDisplayHomeAsUpEnabled(true)`，主题没覆盖 `homeAsUpIndicator`，用的是 AppCompat 默认的 `abc_ic_ab_back_material`；写错：目标 `resources/base/media` 里没有返回箭头的 svg，转换报告写「无箭头位图资产，用系统符号」
