# 例子

都取自库里经验的知识文件和它的前几稿。每个例子写：候选或前一稿怎么写 → 定稿怎么写 → 用的是哪条规则（`rules.md` 的编号）。「初稿」指核实那一步的工作稿，「统一稿」指统一（U）之后、清理（T）之前的那一稿。

例 1–18 的出处是旧写法（「文档 xxx.md，小节名」，`sdk` 只有两个键）；新写的文件出处和版本照 `sources.md` 写，例 19 是同一条换成新写法的样子。

## 一 留下的

**例 1 候选写错了，重核后照声明改，正文跟着改（V3、U1、U3 改错）** — `73894333`

- 候选：`- API 9 及之前默认 false，API 10 及之后默认 true；为 true 时绑定的长按手势不生效……（出处：ts-basic-components-image.md，draggable）`
- 初稿：「ImageAttribute.draggable(value: boolean)：Image 自己的默认拖拽开关；文档写 API 9 及之前默认 false、API 10 及之后默认 true」，另记一处 doubt：声明里写默认 true 的注释块标 @since 11，和文档差一位。
- 定稿条目：〔原因〕ImageAttribute.draggable(value: boolean)：Image 自己的默认拖拽开关，自 API 11 起默认 true（API 9 默认 false）｜鸿蒙 SDK 的 ets/component/image.d.ts，ImageAttribute.draggable｜鸿蒙接口｜沿用并复核
- 定稿改句（原因，改错）：「（API 10 起 Image 自身的 draggable 默认为 true，与通用属性的默认值不同）」→「（Image 自身的 draggable 自 API 11 起默认为 true，API 9 为 false，与通用属性的默认值不同）」，basis：「鸿蒙 SDK 的 ets/component/image.d.ts，ImageAttribute.draggable（@since 9 注释默认 false，@since 11 起注释默认 true）」。

**例 2 候选核过，原意留下，出处换成能核的写法（V3、V7）** — `73894333`

- 候选：`- 默认支持拖出的组件：Search、TextInput、TextArea、RichEditor、Text、Image、Hyperlink：这些组件用 draggable 控制默认拖拽（出处：ts-universal-events-drag-drop.md，页首说明）`；另一行候选「draggable(value: boolean): TextAttribute，默认 false：同族接口：Text 的拖拽开关，要配合 copyOption 使用」。
- 定稿：〔原因〕默认支持拖出的组件：Search、TextInput、TextArea、RichEditor、Text、Image、Hyperlink，用 draggable 控制默认拖拽（Text 还要配 copyOption）｜文档 ts-universal-events-drag-drop.md，页首说明｜鸿蒙接口｜沿用并复核（「Text 还要配 copyOption」见于另一行候选；Text 的 draggable 签名没有单独成条）

**例 3 候选里没有，自己查（V5）** — `73894333`、`bdc493f5`

- 〔原因〕长按触发拖拽：对默认可拖出且 draggable 为 true 的组件，长按达到 500ms 即触发拖拽，800ms 时开始预览图浮起动效｜文档 arkts-common-events-drag-event.md，拖拽流程（手势长按触发拖拽）｜鸿蒙接口｜新查
- 〔做法第 1 步〕资源位图经 ImageDecoder 解码：目录 dpi 高于设备时解码成 (int)(px × 设备dpi/目录dpi + 0.5)；低于设备且 targetSdk ≥ 28 时解码期不放大，固有尺寸由 BitmapDrawable 按上式换算。两种取整都是四舍五入｜android.content.res.ResourcesImpl#loadDrawableForCookie；android.graphics.ImageDecoder#computeDensity｜安卓平台｜新查（初稿记的未核实「BitmapFactory 解码时的密度缩放……取整没核到」，统一时查到，转成条目：U5）

## 二 改写的

**例 4 卡里验证的条目：甲类，改写成平台表现（T1）** — `bdc493f5`

- 初稿 / 统一稿：「只设 objectFit、不设宽高的密度目录位图在设备上比源端大、越出容器；按 px × 160 ÷ 目录 dpi 写出宽高后（如 xxhdpi 72×72px → 24×24vp）与源端一致」｜卡里修好并验证过
- 定稿：「ArkUI Image 只设 objectFit、不设宽高时，从安卓密度目录搬来、放在 base/media 或 xldpi、xxldpi/media 的位图，在设备上显示得比源端固有 dp 大，可越出容器」｜卡里上机实测
- 去掉的是后半句的返修做法和结果（照式子写宽高「后与源端一致」）；那个做法正文第 1 步本来就有。

**例 5 卡里验证的条目：甲类，带上卡号和怎么测的（T1）** — `68023ac5`

- 统一稿：「末指抬起时 Up 事件 type=1、touches.length=1（touches 仍含正在抬起的手指），写成 touches.length === 0 的判定永不成立：返修时在设备上打日志实测」
- 定稿：「ArkUI onTouch 的 Up 事件里 touches 仍含正在抬起的手指：最后一根手指抬起时 type 为 Up、touches.length 为 1，不会出现 0」｜卡里上机实测（case-a1849836a1bfff3c265c，设备日志）

**例 6 默认值加成立条件，值不变（T4）** — `08b9064f`

- 统一稿：「LinearLayout 与 RelativeLayout 的 mGravity 默认 Gravity.START | Gravity.TOP：没写 gravity 时子项贴起始边、贴顶」
- 定稿：「LinearLayout 与 RelativeLayout 的 mGravity 默认 Gravity.START | Gravity.TOP：布局、style 和代码都没设 gravity 时子项贴起始边、贴顶」

**例 7 去掉句尾的做法建议（T5）** — `bdc493f5`、`a8452bfe`

- 「Length 写 number 或不带单位的字符串时按 vp，'10px' 才按 px；所以 Image 的 .width(n).height(n) 直接写换算出的 dp 数」→「Length 写 number 或不带单位的字符串时按 vp，'10px' 才按 px」
- 「Stack 的 alignContent 默认 Alignment.Center：外层 Stack 定触摸盒尺寸时，内层图标不写对齐也居中」→「Stack 的 alignContent 默认 Alignment.Center：不写对齐时子组件在 Stack 内居中」
- 「……HitTestMode.None：自身不响应触摸测试，也不阻塞子节点、兄弟节点和祖先节点，适合不参与命中的占位层」→ 去掉「，适合不参与命中的占位层」

**例 8 去掉的建议正文没有，并进正文（T6）** — `47785524`

- 条目：「shadow(value: ShadowOptions | ShadowStyle)：ShadowOptions.radius 是模糊半径，单位 px；offsetX、offsetY 单位 px、默认 0；color 默认 Black。源端 dp 的 elevation 要先换成 px 再写」→ 去掉最后一句。
- 改句（做法第 2 步，写成明确做法）：「ArkUI Button 设 stateEffect:false，按压用 stateStyles 只换投影」→「……只换投影，shadow 的 radius、offset 按 px 写（dp 值乘屏幕密度）」，basis：「从 shadow 条删下的做法尾巴；鸿蒙 SDK 的 ets/component/common.d.ts，ShadowOptions（radius、offsetX、offsetY 单位 px）」。

## 三 删掉的

**例 9 卡里验证的条目：乙类，是一次返修的做法和结果，拿掉（T1）**

- `0ef2cd00`：「宽度、文字宽、槽宽、指示器与图标位置都在 px 域 floor/trunc、写入属性前 px2vp 后，Row 总宽等于容器 px 宽；在 vp 域 floor 时右侧留空、整体左偏」｜卡里修好并验证过 → 拿掉（正文做法第 2 步就是这个做法）。
- `68023ac5`：「两个按钮各挂 onTouch 时按全屏 touches.length 过滤：……改成控件内按 changedTouches[0].id 维护手指集合后两者各自按下、抬起」→ 拿掉。理由：这是两按钮各挂 onTouch 的返修结果；做法第 1 步已写明按 pointer id 集合的做法，平台事实（touches 含别处手指）另有 TouchEvent 那一条。

**例 10 拿掉乙类之后补前提进正文（T2）** — `7708f650`

- 拿掉：「整屏背景 Image 由 ImageFit.Cover 改为 ImageFit.Fill 后，背景顶部图文完整显示」。
- 改句（做法第 1 步，加条件）：「目标底色取 surface 的实际可见色（每帧清成透明即为黑）」→「目标底色取 surface 的实际可见色（未经 getHolder().setFormat 改成带透明度的格式、每帧清成透明时即为黑）」，basis：「卡里成立的前提：源 SurfaceView 子类只调 getHolder().addCallback，没有 setFormat；android.view.SurfaceView 默认请求格式 PixelFormat.RGB_565（不透明）」。

**例 11 候选整条经验全丢，写 note（V4、V11）** — `42df1ac4`

- 候选 46 行（request、hilog、相机、录音、滚动……），定稿 entries 为空，note：「流程类经验（写码前把 skill、规格和源文件读全、处理截断回执），做法里没有要用的鸿蒙或安卓平台事实，给空条目；46 条候选来自来源卡里别的问题……与读全输入这件事无关，全部丢掉」。

**例 12 未核实的旁注删掉，要上机的进 device_todo（U5）** — `c3bd9c8b`

- 初稿 4 条未核实：① decodeResource 的取整本机没源码；② desiredSize 解码用哪种插值没写；③ 默认 vp 画布上 drawImage 不传宽高按像素还是按 vp 没写；④ densityDPI 是否总等于 densityPixels × 160 没核。
- 统一稿：① ③ 进 device_todo（改写成「在什么设备上量什么」）；条目没加；dropped_notes = 2，即 ② ④ 作为对做法没有影响的旁注删掉。

## 四 正文改句

**例 13 改错（U1）** — `94715d0d` 原因：「语言、uiMode、fontScale、densityDpi、mcc/mnc 变化都会销毁并重建 Activity」→「语言、uiMode、fontScale、densityDpi 变化都会销毁并重建 Activity（mcc/mnc 自 Android 8.0 起默认不重建，只有写进 recreateOnConfigChanges 才重建）」，basis：「Android SDK 平台资源 data/res/values/attrs_manifest.xml，configChanges 的 mcc、mnc 注释」。

**例 14 加条件（U1、U7）** — `0e1c8468` 做法第 1 步：「targetSdk<26 且未声明 maxAspectRatio 或 meta-data android.max_aspect 时，系统按最大宽高比 1.86 截长边」→「targetSdk<26、未声明 maxAspectRatio 或 meta-data android.max_aspect、且 activity 不可调整大小（resizeableActivity 未设为 true；未声明时只有 targetSdk<24 才算不可调整）时，系统按最大宽高比 1.86 截长边」。同一条经验原因段的原句带「本机 android-36.1 源码」，新句写「Android 源码」。

**例 15 写成明确做法，绕开平台没规定的事（U6）** — `1a66114f` 做法第 1 步：「或等价的 4x5 矩阵（RGB 取着色色、alpha 取着色 alpha × 原 alpha）」→「不改写成 4x5 矩阵（矩阵着色要把着色色写进第 5 列偏移量，偏移量的刻度平台没有规定）」；另加一条条目「平台没有规定 4×5 颜色矩阵第 5 列偏移量的刻度（0–255 还是 0–1），声明和文档都没写」；device_todo「ArkUI ColorFilter 4×5 矩阵第 5 列偏移量的刻度……量出 R 通道」。统一时一度写成「要上机核一次」，按 U6 改成这样。

**例 16 恢复原句（U6）** — `c3bd9c8b` 做法第 2 步：统一时一度改成「第一次画出后核对像素宽」，最后恢复原句「drawImage 不传目标宽高，1:1 绘制。」：卡里没记画布的单位，也没有行为写明的等价写法；条目里仍有「dx、dy、dw、dh 默认单位 vp，可构造时传 PX」，要上机的进 device_todo。

**例 17 正文不改，条目写清（U4）** — `cce58a15`：经验说 resourceManager 的 locale「下划线分隔、子标签可能为空」，声明注释示例是连字符。定稿条目：「设备上 ResourceManager.getConfigurationSync().locale 为下划线分隔：en_Latn_US；应用偏好语言只有语言码时为 fa_Arab_（尾部空子标签）……声明注释里的示例 zh-Hans-CN 为连字符写法」｜卡里上机实测（case-4f8a6d24236bd7f92a26）；鸿蒙 SDK 的 ets/api/@ohos.resourceManager.d.ts，Configuration.locale 注释。

**例 18 逐个核对改成脚本做法（U9）** — `08b9064f` 做法第 2 步：「每写完一个撑满宽的 Column，逐个核对固定尺寸或内容宽子项的水平位置由谁决定。」→「写完用一条命令把本页的 Column( 和 Row( 连同紧跟的 alignItems、justifyContent 列出来（例如 grep -n -E 'Column\(|Row\(|alignItems|justifyContent' 文件），只看没有显式写对齐的撑满宽 Column：……」，basis：「逐个容器核对的范围随页面大小增长；没有显式写对齐的容器可以用一条命令列出来，只需要看这几个」。

## 五 新写法

**例 19 同一条换成新写法（N1、N4、N5）** — `73894333`（只示意格式怎么换，这里的事实没有按文档 master 重核）

- `sdk`：旧 `{"harmony": "HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）", "android": "不涉及"}` → 新 `{"verified_on": "2026-11-21", "docs_commit": "e42bd18a89ff75e48e3effdf3d58748376c2caec", "docs_date": "2026-11-21", "harmony": "HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）", "android": "不涉及"}`。
- 出处：旧「文档 ts-basic-components-image.md，draggable 参数说明」→ 新「https://gitcode.com/openharmony/docs/blob/master/zh-cn/application-dev/reference/apis-arkui/arkui-ts/ts-basic-components-image.md，draggable 参数说明」（`scripts/ohdocs_link.py --root <同步目录> --find ts-basic-components-image.md` 换的）。鸿蒙声明的出处写法不变。
- fact 不变：「ImageAttribute.draggable(value: boolean)：Image 自己的默认拖拽开关，自 API 11 起默认 true（API 9 默认 false）」——版本条件出自声明，本来就写在事实里（N5）。
- 交给模型的段头：「已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。……）：」，各行仍是「- 〔step〕fact」，不带出处和链接。
