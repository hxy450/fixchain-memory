# 未声明 supportsRtl 时，规格写明布局恒 LTR，有顺序语义的容器逐个设 Direction.Ltr

审的是：规格
触发（任一种）：
- 读到：AndroidManifest.xml 的 `<application>` 没有 `android:supportsRtl`；写错的样子：规格里没有布局方向契约，按钮条、靠起点对齐的容器没要求显式方向；或只写「Canvas 不镜像」就当 RTL 已处理
适用范围：规格提取阶段，源端 manifest 未声明 supportsRtl 的应用
做法：
- 规格里写：源端布局方向恒 LTR；目标端有顺序或对齐语义的容器（按钮条 Row、alignItems(HorizontalAlign.Start) 的 Column）显式设 .direction(Direction.Ltr)
- 注明子组件默认 Direction.Auto 跟随系统语言、不继承父容器，要逐个容器设
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- supportsRtl 默认 false：manifest 不写时应用不处理 RTL 布局，布局方向恒 LTR（出处：Android SDK 平台资源 data/res/values/attrs_manifest.xml，AndroidManifestApplication 的 supportsRtl（按应用的 compileSdk 取对应平台））
- direction(value: Direction): T，默认 Direction.Auto：组件主轴方向上的布局方向（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.direction）
- 配置为 auto 时按照系统语言方向布局：Auto 不看父容器，阿拉伯语等 RTL 系统语言下就镜像（出处：ts-universal-attributes-location.md，direction）
来源：1 张卡，1 个应用
- case-e485c29b5b8cabfc9f01（2048）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2
