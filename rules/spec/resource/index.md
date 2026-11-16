# 资源与应用配置

读到 res 下的 values-* / layout-* 限定词目录、按名引用的颜色和尺寸资源、AndroidManifest 的 application / activity 声明和 supportsRtl、BuildConfig 开关和多套 base URL，或目标 app.json5 的身份，规格里写资源表、配置值和身份项时

## 触发族

- [Manifest 里 application 和 activity 的声明](manifest-declarations/index.md)（9 条）：读过的 AndroidManifest 里 <application> / <activity> 的 allowBackup、screenOrientation、windowSoftInputMode、android:label、usesCleartextTraffic，或这些没写、依赖平台缺省；交回的规格没写它们的缺省语义、目标配置值和对应验收
- [supportsRtl 声明和 RTL 语言资源](rtl-direction/index.md)（5 条）：读过的 AndroidManifest 写没写 android:supportsRtl、res 下有 values-fa / values-ar 等 RTL 语言目录、源码用 Canvas.drawText 画文字；交回的规格里布局方向契约、画布文字方向和 RTL 验收条目
- [横屏限定词的布局和资源变体](landscape-variants/index.md)（4 条）：读过的源工程有 layout-land / layout-port 布局变体，或 values-land 覆盖了进几何公式的 R.integer、R.dimen；交回的规格只写了竖屏或 base 的值，没写横屏下的不同和运行期读取
- [按资源名引用的颜色和尺寸资源](resource-by-name/index.md)（2 条）：读过的源码用 getColor(R.color.名) / getDimension(R.dimen.名) 按资源 ID 取值，工程里另有名字含同一颜色词的近名 <color> 资源；交回的规格里色表、常量表或验收把近名资源合成一行、标错 hex，或只写颜色词
- [res 下的 values-* 语言和屏宽目录](values-qualifier-dirs/index.md)（4 条）：读过的源工程 res 下有多个 values-<语言> 目录或 values-w<N>dp / values-sw<N>dp 目录，自绘 View 用 getString 取文案画到画布；交回的规格自设只迁部分语言、漏了屏宽覆盖的 dimen，或语言切换的验收只看代码引用
- [构建配置决定的实现和接口环境（BuildConfig 开关、多套 base URL）](build-config-variants/index.md)（5 条）：读到源码按 BuildConfig 布尔开关在新旧两套实现间择一启动，或 API 清单的 base_urls 只给地址常量的键名；规格写「两路径取并集」、验收照停用实现写，或只列一个 Base URL、写没有出处的 dev/staging/prod
- [脚手架身份的 bundleName](scaffold-bundle-name/index.md)（1 条）：目标 app.json5 还是 com.example.myapplication 脚手架身份，源 applicationId 在 com.example.* 下；决策台账里的身份技术项
- [layout-* 限定符目录里的同名布局变体](layout-qualifier-variants/index.md)（1 条）：读到源 res 下 layout-sw600dp/、layout-land/、layout-w<N>dp/ 里有和主布局或 <include> 布局同名的 XML；页面 meta.json 的 layout_sources 和页面 spec 只列 base layout/ 下的文件，没写变体和断点语义
