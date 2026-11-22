# elevation 投影写入 ShadowOptions 时按 px 换算，并集中到一个按 elevation 推导的共享函数

## 何时使用

规格提取阶段写阴影配方，以及界面实现、收敛阶段把 Modifier.shadow(elevation) 或 Surface 的 elevation 写成 ArkUI .shadow() 时

## 适用情境

源端以 dp 表示阴影高度；目标 ShadowOptions 的 radius/offsetX/offsetY 数值按 px 解释，而 width、padding 等长度属性默认是 vp。工程可能已有共享的 elevation→shadow 映射函数，个别页面也可能用预置 ShadowStyle 或字面值。也包括源视图带 elevation 但 outlineProvider=background 且没有背景，实际不投影。

## 原因

“dp→vp 1:1”只适用于长度属性（SDK common.d.ts 注明 ShadowOptions 数值为 px）；把 dp 数值直写进 ShadowOptions，高密度屏上模糊只剩几分之一，阴影几乎不可见。偏差有两种来路：套用长度属性的换算规则，或写配方时 grep 只留了字段签名、过滤掉单位注释。预置 ShadowStyle 与源端高程没有对应关系，替代后既不随高程变化，也绕开了共享函数。

## 做法

1. radius、offsetX、offsetY 用 uiContext.vp2px(源 dp 值) 换算，把单位和换算写进公式本身，集中到一个按 elevation 推导的共享函数；各页面不另写与 elevation 无关的“视觉近似”常量，也不用预置 ShadowStyle 代替源端的具体高程。
2. 源端平台阴影由环境光和屏幕顶端主光两层组成，投影随元素位置变化，单层 ShadowOptions 只能近似：有源端截图时按多档高程实测校准共享函数的常量，没有时登记为需截图校准的视觉近似项，不在注释里写成等价映射。
3. 写 shadow 前先看源视图是否真的投影：elevation 需同时看 outlineProvider 与背景：outlineProvider 为默认的 background 且没有背景时不产生阴影；outlineProvider 设为 bounds 或 paddedBounds 时没有背景也照样投影，仍按映射写 shadow，不按映射表直译。

## 可选检查

- 收敛后有疑问时检索 '.shadow('，确认全工程只剩共享函数一条通路，每个数值字段都经过换算。

来源支持：3 张卡 · 3 次迁移 · 2 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-37.0 的平台资源；android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1 步〕ShadowOptions.radius 是阴影模糊半径，单位 px；offsetX、offsetY 是阴影沿 x、y 轴的偏移，单位 px，不写时为 0；这几项不像 width、padding 那样按 vp 解释
- 〔做法第 1 步〕半模态 SheetOptions.shadow、自定义弹窗 CustomDialogControllerOptions.shadow、Text 的 textShadow 收的也是 ShadowOptions，其中 radius、offsetX、offsetY 同样按 px 解释；SheetOptions.shadow 在 2-in-1 设备上不写时取 ShadowStyle.OUTER_FLOATING_SM
- 〔适用情境 / 做法第 1 步〕ShadowStyle 是系统预置的六档固定阴影（OUTER_DEFAULT_XS、SM、MD、LG，OUTER_FLOATING_SM、MD），传给 shadow() 时阴影外观由档位决定，不随源端 elevation 的数值变化
- 〔原因〕在约 3.5 px/vp 的设备上把源端 elevation 的 dp 数值直接写进 ShadowOptions 时，elevation 2 对应的模糊只剩约 0.6 vp，投影几乎看不见
- 〔适用情境 / 原因〕安卓 android:elevation 属性的格式是 dimension（带单位的尺寸，源码里通常以 dp 写），不是像素数
- 〔做法第 2 步〕安卓平台阴影由环境光和主光两层叠成：平台资源里 light_y 为 0dp、light_z 为 500dp、light_radius 为 800dp（主光在屏幕顶端上方），ambient_shadow_alpha 为 0.039、spot_shadow_alpha 为 0.19（电视配置下 ambient_shadow_alpha 为 0.15），所以投影随元素在屏幕上的位置变化；ArkUI 的 ShadowOptions 只有一层
- 〔做法第 2 步〕radius、offsetY 按 vp2px 换算成 px 的单层固定映射，在屏幕上部的投影仍比安卓源端偏重约 1.5–2.5 倍
- 〔做法第 2 步〕按三档安卓实测反推单层 ShadowOptions 的常量后，多数组件的阴影能对齐，但仍有组件的侧晕、顶晕只有安卓的约一半
- 〔适用情境 / 做法第 3 步〕安卓 View 没有另设 outlineProvider 时取 ViewOutlineProvider.BACKGROUND：有背景时从背景 drawable 取轮廓；没有背景时生成和 View 同尺寸、alpha 为 0 的矩形轮廓，elevation 不产生可见阴影
- 〔做法第 3 步〕ViewOutlineProvider.BOUNDS 按 View 的矩形边界生成 alpha 为 1.0 的轮廓，没有背景也投影
- 〔做法第 3 步〕源端图片写了 elevation、outlineProvider=background 且没有背景时，安卓上不投影
