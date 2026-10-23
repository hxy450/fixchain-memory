# 阶段：修复（repair）

本阶段可用的 97 条经验，按领域与主题分组；一条经验可属于多个阶段。

[返回根索引](../index.md)

## app — 应用级装配与横切机制：入口清单、启动链路、平台能力与系统状态、媒体文件、混合桥接、模块与资源产物

### [app/camera/capture](../topics/app/camera/capture/index.md) — 拍照触发与结果链：完成/失败回传与多帧交付、前屏补光、照片缓冲释放与资产回调

- [前屏补光保留控制器判定出口与回退等待](../topics/app/camera/capture/lesson-b20eaa8108cae9476ca3.lesson.md) · 信号：CONTROL_AE_PRECAPTURE_TRIGGER, CONTROL_AE_STATE, LENS_FACING_FRONT, FLASH_MODE_CLOSE
- [资产回调无请求 ID 时一拍一输出，超时退役不串帧](../topics/app/camera/capture/lesson-8a1d50b9fdcdee8a5752.lesson.md) · 信号：photoAssetAvailable, PhotoOutput, captureStartWithInfo, captureEnd

### [app/camera/orientation](../topics/app/camera/orientation/index.md) — 预览 surface 的缩放居中变换，以及拍照旋转与传感器朝向的目标接口

- [拍照旋转用设备角调 getPhotoRotation](../topics/app/camera/orientation/lesson-a211a70068ce00c94916.lesson.md) · 信号：JPEG_ORIENTATION, SENSOR_ORIENTATION, OrientationEventListener, PhotoCaptureSetting

### [app/camera/session](../topics/app/camera/session/index.md) — CameraKit 会话的输入输出组成、提交时机、拍照 profile、拆卸重建顺序与相机就绪时机

- [会话一次配齐输出再提交，拍照档不硬限 JPEG](../topics/app/camera/session/lesson-05cd365740c0003662a4.lesson.md) · 信号：createCaptureSession, ImageReader, beginConfig, addInput

### [app/capability/sdk-lookup](../topics/app/capability/sdk-lookup/index.md) — 判定无等价前先查 Kit、ohpm、SDK 声明与权限注解

- [应用内开关蓝牙先查 access 开关接口再定方案](../topics/app/capability/sdk-lookup/lesson-7a081dc36013a60358ac.lesson.md) · 信号：enableBluetoothAsync, disableBluetoothAsync, @ohos.bluetooth.access, BluetoothAdapter.enable

### [app/entry](../topics/app/entry/index.md) — 入口 Ability 与 module.json5 装配：初始化时序、全局守护、外部进入与结果回传、扩展能力与卡片登记

- [shortcuts 元数据挂 Ability 下，不挂模块级](../topics/app/entry/lesson-67118603fcc769a5edc9.lesson.md) · 信号：ohos.ability.shortcuts, module.json5, $profile:, shortcuts_config
- [前台服务改扩展能力先查基类导出，type 与基类成对](../topics/app/entry/lesson-16c24b9a44153d703f04.lesson.md) · 信号：extensionAbilities, ServiceExtensionAbility, AppServiceExtensionAbility, WorkSchedulerExtensionAbility

### [app/hybrid](../topics/app/hybrid/index.md) — Flutter 与原生桥接契约：通道方法集、事件通道、路由映射，以及交给冻结 Dart 的对象语义与行为等价核对

- [兼容层返回对象保留宽高语义，大图先在原生侧缩放](../topics/app/hybrid/lesson-e85bdb26fa6acc0cc9f7.lesson.md) · 信号：AssetEntity, ImageSource, getImageInfo, compressAndGetFile

### [app/media](../topics/app/media/index.md) — 媒体文件出入口与图片处理：picker 与安全控件、沙箱导出、播放 URI、解码预取、PixelMap 释放与快照限制

- [音频导入用 AudioViewPicker 并复制进沙箱](../topics/app/media/lesson-62ac5e65ac4aa51128bd.lesson.md) · 信号：AudioViewPicker, photoAccessHelper, MediaStore.Audio, READ_MEDIA_AUDIO

### [app/media-library](../topics/app/media-library/index.md) — 系统媒体库直接读写：受限权限下的相机资产保存、最近媒体入口、删除确认与外部查看分享

- [deleteAssets 先授权再删，取消与失败分开](../topics/app/media-library/lesson-dd3bd947a05103e1f5f0.lesson.md) · 信号：deleteAssets, MediaAssetChangeRequest.deleteAssets, WRITE_IMAGEVIDEO, ContentResolver.delete

### [app/modules](../topics/app/modules/index.md) — 多模块（壳 HAP + HAR）边界：构建常量来源、跨模块导入、资源闭包归属与可复用函数的模块放置

- [HAR 不引宿主 BuildProfile，模式由壳层注入](../topics/app/modules/lesson-6bd9ae0de39cecc06744.lesson.md) · 信号：BuildProfile, assembleHap, Index.ets, oh-package.json5

### [app/resources](../topics/app/resources/index.md) — 应用身份与资源产物从源端换算：脚手架模板值的替换、element/media 转换格式、图标尺寸与产物校验

- [应用显示名同时改 AppScope 与入口 label 值](../topics/app/resources/lesson-55f44e2efdc1a49ac387.lesson.md) · 信号：app_name, EntryAbility_label, string.json, app.json5
## arkts — ArkTS 语言与 ArkUI 声明层的编译约束：接口签名核对、严格类型限制、组件 DSL 规则与运行时语义差异

### [arkts/api-signatures](../topics/arkts/api-signatures/index.md) — 调用 SDK/ArkUI 接口或引用跨文件声明时，参数类型、重载、成员名与语义注释须按声明核对而非凭记忆推定

- [intl 货币格式化须显式传 currency 码](../topics/arkts/api-signatures/lesson-19cedec8ad1bc4b08b2c.lesson.md) · 信号：intl.NumberFormat, getCurrencyInstance, style: 'currency', @kit.LocalizationKit
- [tabBar 不接受 { title } 对象字面量](../topics/arkts/api-signatures/lesson-b402fa546504a1dd6db7.lesson.md) · 信号：TabContent, .tabBar(, TabBarOptions, BottomTabBarStyle
- [写 SDK 调用前按本地 .d.ts 核对成员名与可空性](../topics/arkts/api-signatures/lesson-6e558834938be19c04e2.lesson.md) · 信号：ets/component, ets/api, AppStorageV2.connect, getHostContext
- [单调计时映射 getUptime 并选 TimeType](../topics/arkts/api-signatures/lesson-ce456d60534d97524aa4.lesson.md) · 信号：System.nanoTime, SystemClock.elapsedRealtime, systemDateTime.getUptime, TimeType.ACTIVE
- [禁编译写大页后对照this成员常量导入与$r键声明](../topics/arkts/api-signatures/lesson-e04e26f1f98116275982.lesson.md) · 信号：$r('app., resources/base/element, @Local, @Param

### [arkts/strict-mode](../topics/arkts/strict-mode/index.md) — ArkTS 严格类型系统对对象字面量、接口实现、异常收窄与类声明顺序的限制，不编译时也会留到编译门

- [SDK 观察者声明为 class 时用类型标注的对象字面量](../topics/arkts/strict-mode/lesson-6e74f064efe2649fc295.lesson.md) · 信号：errorManager.on('error'), ErrorObserver, onUnhandledException, onException
- [对象字面量写具名类，Record 替换用字段类或 Map](../topics/arkts/strict-mode/lesson-1696967d1320c7735732.lesson.md) · 信号：Record&lt;string, Object&gt;, \[key: string\], Array&lt;{, constructor(public
- [重抛异常前先收窄为 Error，不直接 throw 变量](../topics/arkts/strict-mode/lesson-dbfae443e671c568e14e.lesson.md) · 信号：throw error, instanceof Error, catch (, new Error(String(

### [arkts/ui-syntax](../topics/arkts/ui-syntax/index.md) — 自定义组件成员声明与 build()/@Builder 的 DSL 规则：装饰器写法、插槽传参、渲染语句与容器专属属性

- [@BuilderParam 传值写箭头闭包不传方法引用](../topics/arkts/ui-syntax/lesson-7d643db6ab406ae64c77.lesson.md) · 信号：@BuilderParam, 10905102, @Builder, content: this.
- [stateStyles 只写 @Styles 或点号块](../topics/arkts/ui-syntax/lesson-39d1dee415d4a252fc5c.lesson.md) · 信号：stateStyles, @Styles, StateStyles, 10905203
## data — 数据层：网络地址与请求鉴权、序列化解析、模型映射、本地持久化及多阶段数据流程在迁移中的语义保持

### [data/model](../topics/data/model/index.md) — 持久化枚举、字段单位、关联键、展示字段与查询层派生状态在模型之间映射时的源端语义保持

- [完成态派生逐分支移植源函数，审计摘要只作线索](../topics/data/model/lesson-4ad956bab5fca6d7f418.lesson.md) · 信号：isCompleted, completedCount, completionMode, occurrenceDate

### [data/network-auth](../topics/data/network-auth/index.md) — 鉴权凭证、会话密钥与拦截器公共参数的获取来源、注入格式、失效判定及其写入侧生产者

- [请求通道按源端重载决定取 key 门，握手基址随请求](../topics/data/network-auth/lesson-62499aa25e87fa6ab5e1.lesson.md) · 信号：ensureKey, OkGo, baseUrl, sessionKey

### [data/network-request](../topics/data/network-request/index.md) — POST 请求体的字段来源与表单/JSON 编码选择，以及请求参数与响应加解密的移植与空值、失败回退

- [@FieldMap 用表单编码，@Body 才用 JSON](../topics/data/network-request/lesson-1cc76f37fe0aea9fef25.lesson.md) · 信号：@FieldMap, @FormUrlEncoded, @Field, @Body

### [data/storage](../topics/data/storage/index.md) — 本地持久化：relationalStore 建表与迁移、自增主键写入、预置数据与播种时机、fileIo 文件与目录操作

- [Room 迁移保留库名、schema 版本与显式升级分支](../topics/data/storage/lesson-a6f300f9295ba538f23b.lesson.md) · 信号：@Database(version, addMigrations, AutoMigration, fallbackToDestructiveMigration
## process — 迁移流程中输入、规格、检查结论与跨任务移交在交接环节失真的机制

### [process/check-gaming](../topics/process/check-gaming/index.md) — 用注释关键字、删功能、改产品语义或相似度阈值迎合检查与测试通过，而非落实源端语义

- [单测失败先用同一输入核对源端，不改产品语义迁就](../topics/process/check-gaming/lesson-75cb65ef5601aaa8f159.lesson.md) · 信号：BLOCKED, manual_review
- [孤儿检测报出的已登记页面不删，上报缺失触发](../topics/process/check-gaming/lesson-8390913de64b0adc00fc.lesson.md) · 信号：NO_IMPORTER, ui-manifest, pages/, dialogs/
- [安全区关键字检查逐页加真实 padding，不写注释蒙混](../topics/process/check-gaming/lesson-f6b95d7d6d0159cb0436.lesson.md) · 信号：NavDestination, Layer 3, avoidArea, statusBarHeight
- [编译修复只改报错行，不删功能或换异义替代](../topics/process/check-gaming/lesson-29744eb694376e8acaca.lesson.md) · 信号：@Entry, AlertDialog, onAreaChange, here-string

### [process/claimed-without-receipt](../topics/process/claimed-without-receipt/index.md) — 凭文本形式的调用、部分输出、过期构建或自动脚本结果宣告写入与完成，缺少真实回执核验

- [sed/perl 改含 $r 的片段用单引号并读回](../topics/process/claimed-without-receipt/lesson-6dae0bf2657b0e339742.lesson.md) · 信号：perl -pi, sed -i, $r(, app.float
- [编译按完整 ERROR 列表判定，失败只记 FAIL](../topics/process/claimed-without-receipt/lesson-7426a20525e52e34c2e7.lesson.md) · 信号：COMPILE RESULT, BUILD SUCCESSFUL, BUILD FAILED, hvigor
- [缺 hvigorw 时用工具自带构建，文本契约不算编译](../topics/process/claimed-without-receipt/lesson-25bc0b7518d335a947d6.lesson.md) · 信号：hvigorw, assembleHap, command-line-tools/bin/hvigorw, CompileArkTS

### [process/enumeration-gaps](../topics/process/enumeration-gaps/index.md) — 枚举迁移范围、入口能力、验收条目或归属时漏掉源端实际存在的项、分支与中间步骤

- [系统表面降级为应用内页时写明入口位置与形式](../topics/process/enumeration-gaps/lesson-238588d3cceaf707ccfe.lesson.md) · 信号：Widget, AppWidget, FormExtensionAbility, LongPressGesture

### [process/handoff-loss](../topics/process/handoff-loss/index.md) — 跨阶段推进、批次收口、重新规划或转述派工时，移交项、全局动作与规则原文在传递中丢失

- [跨文件补实现的功能登记带负责方与验证的移交项](../topics/process/handoff-loss/lesson-4f81eeea17b94190c2de.lesson.md) · 信号：HANDOFF, resolve_by, slice:N, TODO
- [转述规则保留替代写法；禁并发构建的改动汇总后立即全量构建](../topics/process/handoff-loss/lesson-73a7dd4f78cb747f7e7e.lesson.md) · 信号：Record, HashMap

### [process/inferred-not-traced](../topics/process/inferred-not-traced/index.md) — 凭名字、所在模块、import 或调用点推断语义，没有追到定义、委托终点与实际绑定

- [页面入口只按布局与页面类实际绑定推导，不补源端没有的控件](../topics/process/inferred-not-traced/lesson-76aa7901a0ae1af9d544.lesson.md) · 信号：initView, setOnClickListener, ViewModel, onClick

### [process/secondary-over-source](../topics/process/secondary-over-source/index.md) — 规格、合成快照、清单映射或已生成代码等二手产物取代源码成为实现依据而发生漂移

- [沿用已生成页面或兄弟写法前回源码核对语义](../topics/process/secondary-over-source/lesson-e9c6e8ef1b29a6fe9c26.lesson.md) · 信号：@Builder, onReady, maxLength, replace_all
- [规格与源码冲突按源实现，例外只认决策 ID](../topics/process/secondary-over-source/lesson-7a065e8fe384b8c462cc.lesson.md) · 信号：decision_ref, decision_gaps, source-notes, PD-

### [process/unloaded-input](../topics/process/unloaded-input/index.md) — 必读输入因截断、乱码、上下文压缩或过期读取并未真正进入上下文就开始写码

- [PowerShell 读文件带 UTF8 编码，乱码视为未读](../topics/process/unloaded-input/lesson-6a3a7f46c8fec282affa.lesson.md) · 信号：Get-Content, Select-String, -Encoding UTF8, $OutputEncoding
- [上下文压缩后按 spec_ref 与源码锚点重读再写计划代码](../topics/process/unloaded-input/lesson-f616adca9430826b1661.lesson.md) · 信号：spec_ref, feature-index, integration_points, Activity
- [按他文件返回语义改调用方前重读其当前版本](../topics/process/unloaded-input/lesson-35f4f9b3cf566d33e79c.lesson.md) · 信号：ViewModel

### [process/unverified-as-fact](../topics/process/unverified-as-fact/index.md) — 把生成期无法核验的推测、自拟值或假设写成硬性结论、期望值或已实现项

- [替换共享渲染公式时分开已核与假设，以正确场景作回归基线](../topics/process/unverified-as-fact/lesson-cf92f65492e41a03ed8a.lesson.md) · 信号：lineHeight, fontSize
- [点击无响应先设备复现定位，未上机结论标未验证](../topics/process/unverified-as-fact/lesson-afae8d13e00941efe808.lesson.md) · 信号：hitTestBehavior, uitest uiInput click, dumpLayout, hdc shell
## ui — 界面迁移：布局几何、主题图形、文本、状态反馈、导航、弹窗、交互输入与列表分页的机制级对照

### [ui/dialog/carriers](../topics/ui/dialog/carriers/index.md) — 按源弹层类型选载体：真弹窗不以页面叠层或路由页充当、V2 页面的弹窗 API、锚定下拉与自定义内容。

- [真弹窗迁成系统弹窗或半模态，不用可见性叠层充当](../topics/ui/dialog/carriers/lesson-368c4592e4c7075c1871.lesson.md) · 信号：XPopup, CenterPopupView, AttachPopupView, BottomPopupView

### [ui/dialog/content](../topics/ui/dialog/content/index.md) — 弹窗内容与行为的还原：按源布局逐控件重建、复用共享弹窗组件、打开触发点、展开后加载数据、下拉关闭的手势门禁。

- [ComponentContent 后赋的回调以闭包传入](../topics/ui/dialog/content/lesson-1c27b6c7cf05c05733d9.lesson.md) · 信号：ComponentContent, wrapBuilder, openCustomDialog, @Param
- [弹窗展开后才加载数据：先开弹层再内部异步加载带重试](../topics/ui/dialog/content/lesson-5f8833721d3c4a11c60a.lesson.md) · 信号：onExpanded, bindSheet

### [ui/dialog/mounting](../topics/ui/dialog/mounting/index.md) — 弹窗挂载层级与宿主节点：sheet 之上、覆层挂整窗根、锚点所在页、SheetMode 与 targetId

- [多个独立底部弹层不在同一节点链式 bindSheet](../topics/ui/dialog/mounting/lesson-b661a3a6a4c0a1e2a3c9.lesson.md) · 信号：bindSheet, @Local, BottomSheetDialog, SheetOptions

### [ui/graphics/drawing](../topics/ui/graphics/drawing/index.md) — Canvas 自绘的移植：坐标原点共用、自适应公式的参照常量、共享绘制分支的统一规则与被注释绑定的静态化。

- [共享绘制分支按源端通用规则统一修，不写单 key 特判](../topics/ui/graphics/drawing/lesson-17d6e4c04764983be25a.lesson.md) · 信号：drawBars, STROKE, FILL_AND_STROKE, strokeWidth
- [自绘红点按实际分支取尺寸，半径换直径](../topics/ui/graphics/drawing/lesson-99fe69fc59afa886750d.lesson.md) · 信号：BadgeView, setBadgeCount, drawCircle, Circle

### [ui/graphics/icons](../topics/ui/graphics/icons/index.md) — 图标资源的选取与显示：原图复制不以近名替代、固有 dp 与触摸盒分离、场景变体映射、动画矢量帧与 Lottie 接入。

- [图标用源端原图，缺失从 drawable 密度目录复制不替代](../topics/ui/graphics/icons/lesson-943544ce27bf04f9faf8.lesson.md) · 信号：does not have a base resource, drawable-xxhdpi, SymbolGlyph, $r('app.media
- [编码到资源的多变体映射按取值字段拆分不合一](../topics/ui/graphics/icons/lesson-c65e8e59008a5e31bcad.lesson.md) · 信号：iconEx, bgEx, icon2Ex, setBackgroundResource

### [ui/graphics/images](../topics/ui/graphics/images/index.md) — 背景图与图片组件的缩放、形状裁剪与分层落地：layer-list 逐层、整屏位图拉伸、自定义图片组件与兜底预览。

- [无来源兜底预览不加源端没有的边框选中态装饰](../topics/ui/graphics/images/lesson-c8909c3cb5f925913407.lesson.md) · 信号：borderWidth, FrameLayout, placeholder
- [自定义图片组件先读定义：圆形裁剪译 Cover 加圆角](../topics/ui/graphics/images/lesson-9dcd69d2824702310959.lesson.md) · 信号：CircleShape, ContentScale.Crop, ImageFit.Cover, borderRadius

### [ui/interaction/click-binding](../topics/ui/interaction/click-binding/index.md) — 点击绑定的归属与副作用：挂在源端真正持有点击的节点、按处理器分支迁副作用、回调契约兑现、被注释的监听视为死按钮。

- [onClick 挂在源端真正持有点击的节点，整栏或子控件](../topics/ui/interaction/click-binding/lesson-fd3add7128663eb9998f.lesson.md) · 信号：setOnClickListener, onClick, LinearLayout, DataBinding
- [监听回调体被注释时按无响应控件迁移，审计不放行](../topics/ui/interaction/click-binding/lesson-f3e614f295aa409485fd.lesson.md) · 信号：setOnClickListener, android:clickable, onClick, TODO

### [ui/interaction/hit-testing](../topics/ui/interaction/hit-testing/index.md) — 叠放层的命中测试与手势归属：全尺寸覆盖层透传、Block 只放遮罩、侧滑行按钮热区、滑删方向与触发瞬间的坐标取值。

- [不处理点击的全尺寸覆盖层显式设 Transparent 命中](../topics/ui/interaction/hit-testing/lesson-4a4f8d845a204ffa244b.lesson.md) · 信号：hitTestBehavior, HitTestMode.Transparent, HitTestMode.None, FrameLayout
- [侧滑行按钮被拦截时只调按钮热区，不把内容层设 None](../topics/ui/interaction/hit-testing/lesson-6677d286e690407d4af4.lesson.md) · 信号：HitTestMode.None, PanGesture, hitTestBehavior, Stack
- [吞触摸的叠放层显式 Block，空 onClick 不挡](../topics/ui/interaction/hit-testing/lesson-df573635678a799a5f80.lesson.md) · 信号：HitTestMode.Block, HitTestMode.BLOCK_HIERARCHY, HitTestMode.Transparent, HitTestMode.None
- [锚点坐标在点击回调即时取，onAreaChange 只兜底](../topics/ui/interaction/hit-testing/lesson-963bf871aa4e910a8fc8.lesson.md) · 信号：getLocationInWindow, onAreaChange, GestureEvent.fingerList, globalX

### [ui/interaction/input](../topics/ui/interaction/input/index.md) — EditText 到 TextInput 的属性转换：默认装饰关闭、长度上限、小数输入、光标取证与掩码格叠层获焦。

- [TextInput 关默认装饰，按主题状态背景复刻](../topics/ui/interaction/input/lesson-1150c0c721e6dc0dede4.lesson.md) · 信号：showPasswordIcon, InputType.Password, cancelButton, textPassword
- [未定制的光标外观以指定页真机取证，帧差分定位](../topics/ui/interaction/input/lesson-fb5a092e750a3101b862.lesson.md) · 信号：caretStyle, textCursorDrawable, caretWidth, TextInput

### [ui/interaction/selectors](../topics/ui/interaction/selectors/index.md) — 选择控件的选项、初值与选中标记：选项按源数据源、自定义属性初值、级联回填、条件勾选不换 Radio、Slider 步数。

- [自定义 View 的 XML 属性只在被读取时生效](../topics/ui/interaction/selectors/lesson-a6edef3bb44e01a82b72.lesson.md) · 信号：android:checked, styleable, obtainStyledAttributes, setChecked

### [ui/layout/constraints](../topics/ui/layout/constraints/index.md) — 锚点与对齐语义的转换：源端默认对齐与锚点落到 Column/Row/Stack/RelativeContainer。

- [Stack 子项 .align() 无效，对齐用满高容器](../topics/ui/layout/constraints/lesson-92aee54a305ea0bde363.lesson.md) · 信号：.align(, alignContent, Alignment.TopStart, layout_gravity

### [ui/layout/immersion](../topics/ui/layout/immersion/index.md) — 安全区沉浸：是否全屏、系统栏底色与避让带由哪一层承担

- [状态栏实色带挂外层 Column，把 Tabs 包进该层](../topics/ui/layout/immersion/lesson-fe10bd2491ca4ba82cb5.lesson.md) · 信号：Tabs, TabContent, Column, Swiper

### [ui/layout/insets](../topics/ui/layout/insets/index.md) — 系统栏与软键盘避让值的取值、单位与只消费一次

- [页面读避让值用主窗口，不用 getLastWindow](../topics/ui/layout/insets/lesson-8e0e9fe5373a2bbe47af.lesson.md) · 信号：getLastWindow, getMainWindowSync, getMainWindow, avoidAreaChange

### [ui/layout/intrinsic](../topics/ui/layout/intrinsic/index.md) — 由内容、位图比例或库内部规则决定的尺寸：wrap_content、固有高度与宽高比不用百分比或估值代替。

- [实测宽落在框架最小值时写 constraintSize](../topics/ui/layout/intrinsic/lesson-42364ad323112c3342ae.lesson.md) · 信号：constraintSize, minWidth, maxWidth, AppCompat
- [并排图片列按固有宽比例分列高度用 aspectRatio](../topics/ui/layout/intrinsic/lesson-0618cdf331560d389f0e.lesson.md) · 信号：aspectRatio, wrap_content, Blank().layoutWeight(1), layoutWeight

### [ui/layout/layers](../topics/ui/layout/layers/index.md) — 页面骨架与叠放层按运行时真实结构落定：运行时挂载、重叠子视图、gone 节点不按 XML 占位定几何。

- [RelativeLayout 无规则子项放同一 Stack](../topics/ui/layout/layers/lesson-7dcf2d92c689c96c190b.lesson.md) · 信号：RelativeLayout, layout_below, layout_above, layout_toEndOf
- [接线已转换页保留全屏底层加状态前景层骨架](../topics/ui/layout/layers/lesson-4de4283ec625be7e976c.lesson.md) · 信号：FEATURE_NO_TITLE, MapView, showRoute, tabData

### [ui/layout/scrolling](../topics/ui/layout/scrolling/index.md) — 滚动容器的包含范围、交叉轴尺寸、首尾留白与高度上限，以及 Scroll 内嵌套内容的测高与滚动归属。

- [嵌套滚动的 Web 高度跟文档，并锁 H5 自身滚动](../topics/ui/layout/scrolling/lesson-fd2dd522fdb03b3e5385.lesson.md) · 信号：wrap_content, nestedScroll, PARENT_FIRST, onPageEnd
- [并排卡等高用 onSizeChange 实测高度传递](../topics/ui/layout/scrolling/lesson-8334433bea644f2a89ae.lesson.md) · 信号：onSizeChange, SizeOptions, NestedScrollView, match_parent

### [ui/list/behaviors](../topics/ui/list/behaviors/index.md) — 列表容器行为：侧栏与分组列表的滚动联动、组头默认展开、Repeat 虚拟滚动的项高度核对、swipeAction 挂载。

- [分类页右侧用 Scroller 列表双向联动迁滚动保护](../topics/ui/list/behaviors/lesson-7723af3766fb843a2577.lesson.md) · 信号：scrollToIndex, onScrollIndex, Scroller, LazyListState
- [改用 Repeat 虚拟化前逐列表核对项高度来源](../topics/ui/list/behaviors/lesson-150e48577e599f64ee23.lesson.md) · 信号：virtualScroll, Repeat, LazyForEach, alignSelf(Stretch)
- [无组点击监听时组头仍默认切换展开状态](../topics/ui/list/behaviors/lesson-e01c6f821d631fad5383.lesson.md) · 信号：ExpandableListView, BaseExpandableListAdapter, setOnGroupClickListener, expandGroup

### [ui/list/data-sources](../topics/ui/list/data-sources/index.md) — 列表数据源的绑定与并发：各列表各自的数据与排序器、本地变换随列表迁移、分页门闩、代次保护与行内在途锁。

- [LazyForEach 换数据不换源对象，通知重载](../topics/ui/list/data-sources/lesson-40efd2d02a5ea9554a95.lesson.md) · 信号：LazyForEach, IDataSource, DataChangeListener, onDataReloaded

### [ui/list/items](../topics/ui/list/items/index.md) — 条目类型与渲染分支：多 viewType 卡片外观、绑定代码里的区块与模板、跨列占位、副行回退、配置驱动分派。

- [按全部 item 布局与 handleXxx 分支建页面区块](../topics/ui/list/items/lesson-e17b45a28a8d92ecbd01.lesson.md) · 信号：addItemType, handleXxx, onCreateViewHolder, SwipeRefreshLayout

### [ui/list/pager](../topics/ui/list/pager/index.md) — ViewPager 到 Swiper：页数与禁滑方式、初始页用 index 绑定、自绘 tab 双向联动与日历翻页容器

- [分页日历相邻页并发查询，Swiper 落定后一次提交](../topics/ui/list/pager/lesson-85b33ff729ab0514a20a.lesson.md) · 信号：Swiper, Canvas, onAnimationEnd, onGestureSwipe
- [自绘日历翻页用 Swiper 承载，每页一 Canvas](../topics/ui/list/pager/lesson-d4e63d27885d9e348723.lesson.md) · 信号：Swiper, Canvas, PanGesture, ViewPager2

### [ui/navigation/handoff](../topics/ui/navigation/handoff/index.md) — 跳转动作随行的交接：点击出口落实际跳转、跳前写入的共享状态、结果回传写回、同窗口 push 的方向切换与恢复。

- [副作用导航逐出口在 onClick 落实际跳转与参数](../topics/ui/navigation/handoff/lesson-32af50a1dfb0c1c254af.lesson.md) · 信号：findNavController().navigate, bundleOf, OpenTripDetail, onClick

### [ui/navigation/hosts](../topics/ui/navigation/hosts/index.md) — Navigation/@Entry 宿主与页面注册：栈来源、首屏压栈、路由跳板、默认标题栏、外部入口守卫与跨页生命周期。

- [main_pages 只登记路由页，子组件和弹窗不登记](../topics/ui/navigation/hosts/lesson-c4a6eaaf6a22c0b8823f.lesson.md) · 信号：main_pages.json, 10905402, @CustomDialog, router.pushUrl

### [ui/navigation/parameters](../topics/ui/navigation/parameters/index.md) — 路由参数契约：固定目的地名与 param、按接收端定义载荷、多入口共享载荷、缺失哨兵与有效性、语义冲突拆字段。

- [同一参数多语义时按源契约拆字段或入口解析](../topics/ui/navigation/parameters/lesson-e202ff0d01ace7dee225.lesson.md) · 信号：JSON.parse, pushPathByName, ViewModel, DTO
- [多入口目标页按全部 extras 定义共享路由载荷](../topics/ui/navigation/parameters/lesson-953309e05bc1cd36c0d1.lesson.md) · 信号：searchFromMap, locationType, searchText, setResult

### [ui/state/binding](../topics/ui/state/binding/index.md) — 状态到控件的绑定与刷新：随状态变的参数不作 @Builder 值参、事件给出的目标值直写、按状态显隐、乐观更新。

- [setVisibility 分支随状态迁移，GONE 不渲染](../topics/ui/state/binding/lesson-43a9050245b1afa165bf.lesson.md) · 信号：setVisibility, Visibility.Hidden, GONE, setText
- [宿主标题栏与 H5 导航栏按页面状态双向决定显隐](../topics/ui/state/binding/lesson-1a5fbc237ad071a62aaa.lesson.md) · 信号：runJavaScript, onOverrideUrlLoading, onTitleReceive, onPageEnd
- [状态派生值不传 @Builder，改 @Param 子组件](../topics/ui/state/binding/lesson-8d2979542fa2cd65150c.lesson.md) · 信号：@Builder, @Param, @ComponentV2, Repeat

### [ui/state/feedback](../topics/ui/state/feedback/index.md) — 操作结果反馈：异步结果各分支的副作用、失败隔离与降级语义、loading 收口、提示浮层的承载与队列。

- [异步结果回调按成功失败分支列全副作用逐项对齐](../topics/ui/state/feedback/lesson-ac7a2e17b8d88c3cee7b.lesson.md) · 信号：LiveData, showToast, AlertDialog.Builder, Settings.ACTION_APPLICATION_DETAILS_SETTINGS

### [ui/state/observation](../topics/ui/state/observation/index.md) — 共享可观察模型的订阅：@Trace 字段判定与直读、新数组赋值发变更、ForEach 键与原位更新、实例拆分。

- [拆 ViewModel 单例，跨页状态显式传递而非换 new](../topics/ui/state/observation/lesson-fc724027e2c995632733.lesson.md) · 信号：getInstance(), AppStorageV2, @Param, @Monitor
- [替换对象时 ForEach 键并入显示字段；稳定键则原位更新](../topics/ui/state/observation/lesson-2e636699fa65aefd63f0.lesson.md) · 信号：ForEach, Repeat, RepeatItem, @Param

### [ui/text/formatting](../topics/ui/text/formatting/index.md) — 显示值的加工在目标端复现：AnnotatedString 加工、setSpan 开区间、格式化精度与带兜底的访问器。

- [textAllCaps 按 locale 大写](../topics/ui/text/formatting/lesson-cce58a1538fedfda3695.lesson.md) · 信号：textAllCaps, AllCapsTransformationMethod, toLocaleUpperCase, textCase

### [ui/text/typography](../topics/ui/text/typography/index.md) — 文本度量的换算：lineHeight 与单行盒高、字号倍率 dp→vp，以及单行中间省略与多行末行截断粒度。

- [单行盒高与多行行距分开，lineHeight 不同名直映](../topics/ui/text/typography/lesson-2a2924aaebbfbea80780.lesson.md) · 信号：lineHeight, .lineHeight(), lineSpacing, LengthMetrics.fp
- [缺枚举的 FontWeight 写数值，不换近名](../topics/ui/text/typography/lesson-605038b091e03c26c005.lesson.md) · 信号：FontWeight.SemiBold, FontWeight.Light, FontWeight.ExtraBold, FontWeight.Thin

### [ui/theme/effects](../topics/ui/theme/effects/index.md) — 渲染效果换算：阴影 px 单位、模糊边缘、blendMode 离屏范围、渐变端点几何与角度、渐变描边与背景分支。

- [blendMode 着色把底色字形渐变放同一离屏组](../topics/ui/theme/effects/lesson-3024193e4816229c5370.lesson.md) · 信号：blendMode, BlendApplyType, drawWithContent, BlendMode.Plus
- [圆角加描边时 radius 写进 .border()](../topics/ui/theme/effects/lesson-8b7c4ece5e5bf7704a44.lesson.md) · 信号：.border(, .borderRadius(, cornerRadius, setStroke

### [ui/theme/sources](../topics/ui/theme/sources/index.md) — 控件外观数值的真实来源：应用主题、库默认 Tokens、style 继承、被引用 drawable 与截图取证。

- [style 引用先展开再逐实例叠加覆写，圆角不照抄相邻](../topics/ui/theme/sources/lesson-bc5b8558ab086168b462.lesson.md) · 信号：@style/, styles.xml, @Builder, borderRadius
- [视觉修复以源布局为准，截图差先折算 vp 再三方对照](../topics/ui/theme/sources/lesson-8119d8bf0b58e4daac24.lesson.md) · 信号：@Preview, docs/assets, setVisibility, getChannel
- [视觉属性逐项取自源布局、item 布局与适配器分支，不近似](../topics/ui/theme/sources/lesson-e4e65a99e545871f96ae.lesson.md) · 信号：drawableLeft, drawableStart, ImageView, TextView
