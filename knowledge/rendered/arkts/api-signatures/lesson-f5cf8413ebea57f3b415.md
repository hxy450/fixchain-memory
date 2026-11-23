# 依赖 API 的单位、默认行为或作用范围时，源端与目标端都读到语义说明：行为级契约写出源 API 实际的作用区域与度量，不只抄字面参数，也不以签名存在推定等价

## 何时使用

规格提取、实现或接线阶段，准备依赖某个 API（源端或目标端）的单位、默认行为、作用范围或字段含义写映射契约或代码时

## 适用情境

当前疑点涉及数值单位（px 还是 vp）、默认是否占位、对子节点的作用、单行与多行的排版语义等；查询只返回同名签名、字段声明行或接口前言，或 grep 过滤掉了紧邻的注释行。也包括同名接口的多个重载（如按 Resource 对象与按数字 id 取资源字符串），查询只证明它们都存在。也包括源端在 Button/AppCompatButton 子类或带 style 的 TextView 上调用 setAutoSizeTextTypeUniformWithConfiguration，规格行只写字号区间与“自适应块宽”；以及目标用 measureTextSize 一类测量 API，参数与返回值单位不同。

## 例外与边界

- 当前输入已有适用版本下的明确规则或已成立实现时，直接复用，无需重复查证或补写证明材料。
- 同名的阴影参数单位不一定相同：ShadowOptions（含 shadow、textShadow、弹窗与半模态的 shadow）按 px，要 vp2px；DataPanel、Gauge 的阴影选项（MultiShadowOptions）按 vp，已按 vp 写的数值保留，不套 vp2px。

## 原因

签名相同不等于语义相同：把 ShadowOptions 的数值当 vp（注释写明 px）、把 HitTestMode.Block 当作只挡兄弟、把 Compose lineHeight 当作 ArkUI .lineHeight 的等价物、认为根 Navigation 不设 title 就不占位，都是只看到签名或凭记忆定稿。grep 截取字段行时，单位说明常在紧邻的注释行里被过滤掉。源 API 的作用范围同样要读：TextView 自动字号在“控件尺寸减内边距”的内容区内按宽高两向、按控件字体测量，按钮子类换背景后样式内边距与字体仍生效，只抄字号区间就写成了“在整块内自适应”。目标端 measureTextSize 的 constraintWidth 数值按 vp 解析，返回的 width/height 是 px，把 vp 宽先 vp2px 会让约束放大数倍、永远测成一行。

## 做法

1. 写映射契约前同时读源 API 的作用区域与度量：如 TextView 自动字号作用于控件尺寸减内边距、按控件 textAppearance 的字体测量；契约写出这些，不只写字面参数，API 形态再留给实现期对目标 .d.ts。
2. 只针对当前疑点，打开所用 API 或字段的声明及紧邻注释、所在接口的说明或交互映射参考的对应表；返回停在签名或前言时接着读相邻行，直到能回答该疑点，不必重读整个 SDK。
3. 把查到的单位、作用范围或默认行为写进当前表达式和映射契约（如 radius: uiContext.vp2px(e)；measureTextSize 的 constraintWidth 直接传 vp 数值或带单位字符串，返回值 px2vp 后再与 vp 常量比较）；关键换算留一句依据即可。
4. 文档措辞仍不足以确定行为时，改用不依赖该行为的写法，或沿用已成立路径并在正常回报里标出具体未决点，不把推断写成等价。

## 可选检查

- 只有实现与声明仍有冲突时，局部对照实际用到的字段与结果。

来源支持：15 张卡 · 已知 5 次迁移（部分未记录） · 已知 4 个应用（部分未记录）

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-37.0 的平台资源；android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因〕两端双端布局 dump 量得：同一排版令牌的单行 Text，ArkUI 按 .lineHeight 直译后盒高 28vp，Compose 一侧约 19dp（接近字体自然高）；ArkUI 的 .lineHeight 对单行文本同样撑高
- 〔原因 / 做法第 3 步〕Text 的 lineHeight 取 number 时单位是 fp；设置值不大于 0 时不限制行高，按字号自适应；与 lineHeightMultiple（API 22 起）同时设置且后者有效时 lineHeight 不生效
- 〔原因 / 做法第 3 步〕LineSpacingOptions.onlyBetweenLines（API 20 起）默认 false：首行上方和尾行下方也有行间距；为 true 时行间距只在行与行之间
- 〔原因 / 做法第 3 步〕ShadowOptions 的 radius（模糊半径）、offsetX、offsetY 单位都是 px，offsetX、offsetY 没写时为 0
- 〔原因 / 做法第 3 步〕SheetOptions.shadow、CustomDialogControllerOptions.shadow 和 Text 的 textShadow 接收的也是 ShadowOptions，数值同样按 px 解释
- 〔原因〕DataPanel、Gauge 的阴影选项继承的 MultiShadowOptions 与 ShadowOptions 不同：radius、offsetX、offsetY 单位是 vp，没写时 radius 为 20、偏移为 5
- 〔原因 / 做法第 3 步〕安卓 android:elevation 是 dimension 量纲（布局里按 dp 写），不是像素数
- 〔原因〕在 3.5 px/vp 的设备上，把 elevation 2 的 dp 数直接当 px 写进 ShadowOptions 时，模糊只剩约 0.6vp，投影几乎看不见
- 〔做法第 3 步〕Length 为 number 时默认单位 vp；string 不带单位时也按 vp，要 px 须显式写 'Npx'，也可写百分比字符串
- 〔做法第 3 步〕px 是屏幕物理像素；vp 按屏幕像素密度换算成物理像素，vp 与 px 的比例随屏幕密度变化
- 〔原因 / 做法第 3 步〕MeasureUtils.measureTextSize 返回的文本宽和高都是 px
- 〔原因 / 做法第 3 步〕MeasureOptions.constraintWidth 默认单位 vp，不支持百分比字符串，取值范围 [0, +∞)，只在 measureTextSize 中生效；不设置时按单行布局的最大宽度测量
- 〔原因〕MeasureUtils.measureText 的结果始终是单行文本宽度（px），constraintWidth、maxLines 等布局约束对它没有影响
- 〔原因〕设备上 measureTextSize 的 constraintWidth 传 vp2px 换算后的数时，约束宽度按 vp 被放大数倍，本该折行的标签测成一行；直接传 vp 列宽时同一标签测得两行
- 〔原因〕HitTestMode.Default 时自身和子节点响应触摸测试、只阻塞兄弟节点；HitTestMode.Block 时自身响应，并阻塞子节点、兄弟节点和祖先节点的触摸测试
- 〔原因 / 做法第 1 步〕安卓 TextView 自动字号的可用区域是测量宽高减去两侧总内边距（宽用 getTotalPaddingLeft/Right，高用 getExtendedPaddingTop/Bottom），在这个区域里按宽高两向找能放下的最大字号；水平滚动时宽度不设限
