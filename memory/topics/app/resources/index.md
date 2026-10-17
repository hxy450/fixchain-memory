# app/resources

应用身份与资源产物从源端换算：脚手架模板值的替换、element/media 转换格式、图标尺寸与产物校验

[上一级](../index.md)

## 本级经验

- [8 位颜色保持 #AARRGGBB，转换后逐项往返核对](lesson-783faf2767a952034514.lesson.md) · 阶段：execute/verify · 信号：colors.xml, color.json, #AARRGGBB, #RRGGBBAA
- [app.json5 的 icon 改指分层图标并补齐前景背景](lesson-feec63f65102f5396e51.lesson.md) · 阶段：execute · 信号：app.json5, $media:layered_image, $media:app_icon, layered-image
- [分层图标前景裁到可见区，前景背景同尺寸](lesson-d838f9236f7452b82738.lesson.md) · 阶段：execute/verify · 信号：adaptive-icon, layered-image, layered_image.json, mipmap
- [反编译资源的 $父名__N 片段单独分类，输出名校验字符](lesson-850dc758d337c4780ae9.lesson.md) · 阶段：execute · 信号：apktool, animated-vector, animation-list, __N
- [启动窗图标取自适应前景层，底色取源主题窗口背景](lesson-c4af68b3ee1456525e8e.lesson.md) · 阶段：execute · 信号：startWindowIcon, startWindowBackground, start_window_background, windowSplashScreen
- [小图标转规范尺寸时图形居中到显示区，低清源不放大](lesson-66e082374dc8992f48ae.lesson.md) · 阶段：execute · 信号：xxhdpi, 1024×1024, layered_image, mipmap
- [应用显示名同时改 AppScope 与入口 label 值](lesson-55f44e2efdc1a49ac387.lesson.md) · 阶段：plan/execute/repair · 信号：app_name, EntryAbility_label, string.json, app.json5
- [沿用脚手架包名前核对决策与签名；vendor 按源端落地](lesson-fb996956b33a1ba65861.lesson.md) · 阶段：spec/execute · 信号：bundleName, com.example, applicationId, app.json5
- [版本号经 bundleManager 运行时读取，不写成常量](lesson-a6ed8a9c6017ddb73beb.lesson.md) · 阶段：execute · 信号：BuildConfig.VERSION_NAME, BuildConfig.VERSION_CODE, bundleManager.getBundleInfoForSelfSync, GET_BUNDLE_INFO_DEFAULT
- [资源值按精确名查全部 values*，限定词写分支](lesson-0c9e222422d81871b464.lesson.md) · 阶段：spec/execute · 信号：getColor, getDimension, getInteger, values-land
- [颜色只写 hex 或 $color:，数组项写成对象](lesson-94a3f7a5ec5ad8f8a3e8.lesson.md) · 阶段：execute/verify · 信号：colors.xml, arrays.xml, @android:color, $color:
