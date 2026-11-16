# 源清单 supportsRtl=true 且有 RTL 语言资源时，ui-manifest 全局约定登记布局方向镜像

审的是：规格
触发（任一种）：
- 读到：AndroidManifest.xml 的 application 标签有 android:supportsRtl="true"，res 下有 values-ar、values-he、values-fa 等 RTL 语言目录；写错的样子：ui-manifest、feature-base 或页面规格的全局约定里没有布局方向镜像（RTL）要求，全文搜不到 RTL、supportsRtl、镜像
适用范围：规格提取阶段写 ui-manifest 全局约定时
做法：
- 在 ui-manifest 全局约定登记一条：布局随方向镜像；源端 Start/End 属性写成 start/end（LengthMetrics），只有源端是 Left/Right 才写 left/right；同一元素的对齐和边距用同一套键
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- supportsRtl 是 boolean，默认 false：没写就不支持 RTL 布局（出处：Android SDK 平台资源 data/res/values/attrs_manifest.xml，AndroidManifestApplication 的 supportsRtl（按应用的 compileSdk 取对应平台））
- 没有 supportsRtl 时 View 处于 RTL 兼容模式（isRtlCompatibilityMode 返回 !hasRtlSupport()）：只有声明了 supportsRtl，Start/End 才会随方向镜像（出处：android.view.View#isRtlCompatibilityMode）
针对本应用要查的：
- 源应用是否支持 RTL、带了哪些 RTL 语言资源：源工程 AndroidManifest.xml 的 application 标签按 android:supportsRtl 找；res 下按 values-<语言> 目录名找 ar、he、fa 等；supportsRtl 为 true 且至少有一个 RTL 语言目录，就在全局约定登记镜像要求
来源：1 张卡，1 个应用
- case-927e26bb7b18f83f2f38（omni-notes-hmos）：做法第 1 步 ← 建议 3
