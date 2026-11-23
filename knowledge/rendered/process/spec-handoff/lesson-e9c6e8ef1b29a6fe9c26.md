# 沿用已生成页面、兄弟任务的写法或已有解析函数前，回到源码核对该片段的语义

## 何时使用

页面转换、公共组件抽取、切片接线或页面重建阶段，参照已生成页面中的同名控件、弹窗、列表、顶栏或导航栈写法时；数据层为新增接口方法复用已有的解析、封装函数时；复用工程已有的共享状态 key 时；按“与 Android 1:1 对齐”修改已有页面（含基线遗留骨架）时；在已有按钮、工具栏或面板上按 Android 契约改写时；把已转换页面的逻辑下沉到服务或 ViewModel 时

## 适用情境

后写的 worker 同时读到源码与先前 agent 已生成的目标代码片段（@Builder 控件、输入弹窗、弹窗承载方式、列表键函数、顶栏折叠、图标控件行、安全控件样式、全屏遮罩、onReady 取栈写法、共享状态 key、登录结果解析函数等），准备当作项目约定直接沿用。或对齐任务在一个与源端结构不同的既有页面上进行，写者已读到源布局 XML。 也包括后一批执行代理把同批尚未验收的兄弟页（如只回显接口 JSON 的页面）当作模板，照同一模式写出更多页面。也包括 1:1 返修重写已有片段时，沿用目标端已有的尺寸、颜色、限制属性（如三框统一的 maxLength、硬编码字色）或注释里的结论（“源码未设，保真”“已裁定”），以及以仓内同族页面为模板复刻输入行时照搬其图标尺寸与光标色。 也包括目标页面在本轮前已有一版可用实现（占位按钮各带回调、页内简化面板、既有字号与字数上限），本轮契约已写明 Android 的按钮 → 动作绑定、跳转目标与参数及数值，写者只换图标、文字或颜色。也包括先例里夹带登记为不确定、近似或“需真机校对”的取值（弹窗族底色与圆角、折叠头部近似、M2 工具栏度量），或行为类先例（弹窗回调接线时序、链式弹层参数、解析循环、定位写法）只经过类型检查。也包括服务或 VM 抽取时，把页面里已写的切片区间、空输入分支或同名 API 近似原样搬进服务，并在注释里写成“等价 Android”的新契约。

## 例外与边界

- 第 1、5 步说的“源中没有的属性”指源端实际没有这个值，不是源布局 XML 里没写：没写的属性先顺着控件 style、主题和框架默认解析出实际值；值来自主题或框架、又和目标端默认不同时，目标端要显式写出，不按“源布局没写”删掉。例如主题继承 Theme.Material 一族、没另设 textCursorDrawable 时，输入框光标按主题的 colorControlActivated（没覆盖时取 colorAccent）着色，而 TextInput 的 caretColor 不写时是 #007DFF；源图片视图不写具体尺寸时，位图按所在密度桶显示成固定 dp（dp = px × 160 ÷ 桶的 dpi），目标端 Image 要按算出的 dp 写宽高

## 原因

已有目标代码可能带有尚未暴露的偏差，或依赖原来的输入来源、状态更新、挂载方式与生命周期。把它直接当成项目约定，会让先例覆盖当前已经读到的源端语义，并把同一偏差复制到更多文件。来源中的这些先例尚未经相应运行验证，不能仅凭存在相似写法推断当前场景可用；对齐已有页面时，旧骨架也可能包含源端没有的结构。另一应用的返修会话三次出现同一机制：以同族页面为模板写弹窗输入行，沿用其 24×24 图标和蓝色光标而没解析源 drawable；改写密码页时把只在一个源控件上的 maxLength 写回三个框、把未声明的字色硬编码；把旧注释“组头不可点，保真”当作源端结论继续扩写。 已有回调与数值同样是待核对的先例：只换显示内容会把旧槽位的回调带到新按钮上，页内简化面板、旧字号与旧字数上限也会以“保留既有实现”为名留下。另一应用的漫画阅读页如此：“票”按钮沿用旧槽位回调跳到购买章节页，底部目录仍开页内面板，字号与字数上限未按契约修改。

## 做法

1. 沿用前逐个核对片段在源码里对应的行为：参数是否随状态变化、输入约束是否真的阻止显示、条目更新后键是否变化、折叠是否连续、取值来源（响应头还是响应体）是否相同、本页与先例页的挂载方式（压栈还是嵌入容器）是否相同；核对通过再落盘，已有代码不能代替对源码的核对。以同族页面为代码模板时只复用结构和逻辑，复制来的每个尺寸、颜色和修饰符都回到当前源布局逐项核对，源中没有的属性不带入。
2. 已有写法与本处源码不一致时按源码实现，并在报告写明差异，不把近似复制到新文件。
3. 先例本身没有经过运行验证（弹窗打开路径、真机截图）时，不以“先例能用”推断可运行；某处写法被修复后，搜索同一写法的其他页面一并核对。
4. 对齐既有页面时先按源 XML 列组件清单（背景、标题栏、卡片子项、主按钮文案、页签/ViewPager、空态），与现有组件树逐项比对；源端不存在的区块替换，不在旧骨架上只调尺寸。
5. 旧代码注释里的结论（“源码未设/保真/已裁定”）当作待核实的假设，用源码和框架默认行为重新验证后再保留；用 replace_all 或多控件模板批量改写前，确认一并写回的每个属性在每个对应源控件上确实存在。
6. 在已有按钮或面板上对齐时，先按源端监听代码列“按钮 → 点击目标”表，并把契约中的数值与跳转（字号、字数上限、目标页与参数）逐条映射到现有表达式，再逐个改写；只换图标、文字或颜色不算对齐。改完列出每个按钮的资源与 onClick 目标：两个按钮指向同一目标、或某个分支失去入口时回源码复核；单独改一个按钮的动作时，把它原来承担的动作迁到 Android 中对应的按钮。
7. 先例中登记为不确定、近似或“需真机校对”的值不当作已验证的族定值沿用；行为类先例（回调接线、弹层参数、定位写法、解析循环）先确认已运行验证，类型检查通过不代表行为正确。发现先例与源不符时改正先例或登记，不为“保持一致”沿用。
8. 把页面逻辑下沉到服务或 VM 时，以源码为准复核被搬运的每个分支与区间，不把页面里的近似写成服务契约或注释里的“等价”结论。

## 可选检查

- 对齐既有页面后，用契约关键值（目标页名、数值、状态参数）检索本次改动处，确认没有只停留在样式层。

来源支持：60 张卡 · 已知 18 次迁移（部分未记录） · 已知 17 个应用（部分未记录）

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的平台资源；android-36.1 的源码；com.google.android.material:material 1.12.0；androidx.appcompat:appcompat 1.7.1。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔适用情境 / 做法第 1 步〕CustomDialogController 只有作为 @CustomDialog 和 @Component struct 的成员变量、并在 @Component struct 内部定义时赋值才有效；CustomDialogControllerOptions.builder 声明为 any，编译期不约束传入的弹窗组件类型
- 〔适用情境 / 做法第 7 步〕NavDestination.onBackPressed 只在与 Navigation 绑定的导航控制器里有内容时生效；回调返回 true 表示重写返回键逻辑，返回 false 表示回退到上一个页面
- 〔适用情境 / 做法第 1 步〕页面组件外层仍保留 NavDestination、又作为主页 Swiper 的子页嵌入时，它 onReady 拿到的 context.pathStack 是嵌套 NavDestination 的栈，不是根 Navigation 的栈；用它覆盖注入的根栈时，点击跳转无反应，调用 pushPathByName 报 TypeError: pushPathByName is not callable
- 〔适用情境 / 做法第 7 步〕bindSheet 的选项没写时：SheetOptions.showClose 默认 true（显示关闭按钮）；dragBar 默认 true，但只有 detents 设了多档并生效时才显示；height 默认 SheetSize.LARGE；BindOptions.backgroundColor 默认 Color.White
- 〔适用情境 / 做法第 7 步〕同一个组件上链式绑定四个 bindSheet 时，其中三个面板打不开；每个 bindSheet 各自绑在独立的零尺寸组件上时都能打开
- 〔做法第 1 步〕NavPathStack.pushPathByName 的 param 声明为 unknown 或 Object，NavPathInfo.param 是 unknown，编译器不检查生产端和目标页用的是不是同一个类；ArkTS 不支持 structural typing，字段相同的两个类仍是不同类型；JSON.parse 返回 any，as 断言不会让结果成为该类的实例，instanceof 判定为 false
- 〔适用情境 / 做法第 1 步〕ForEach 替换数组项后，新项生成的 key 没变时，ForEach 不把数据更新同步给子组件，子组件仍绑定旧对象、感知不到新对象的属性变化；文档建议键值生成函数使用与 UI 显示相关的数据属性
- 〔适用情境 / 做法第 7 步〕SaveButton 从 onClick 回调到调用媒体库特权接口的间隔要在授权时间内：API version 19 及之前为 10 秒，API version 20 及之后为 1 分钟
- 〔适用情境 / 做法第 7 步〕SaveButton 授权成功的回调里先做冷缓存下载再写相册时，下载超出约 10 秒的授权窗口，写相册静默失败，相册里没有文件
- 〔适用情境 / 做法第 1 步〕Scroller.currentOffset() 返回的 OffsetResult.yOffset 单位是 vp；onScrollFrameBegin 回调的 offset（这一帧将要滚动的量）单位也是 vp，返回的 offsetRemain 是实际滚动量
- 〔原因 / 做法第 5 步〕ExpandableListView 的组头点击先交给 OnGroupClickListener，只有它返回 true 才拦截；没注册监听或监听返回 false 时，点已展开的组就折叠，点未展开的组就展开
- 〔原因 / 做法第 5 步〕android:maxLength 只给声明它的那个 TextView（EditText）加 LengthFilter；没声明时读到 -1，不加长度过滤器；android-36.1 源码里，可编辑且 singleLine 的输入框没声明 maxLength 时另加 5000 字符的限长（更早版本另核）
- 〔原因 / 做法第 5 步〕TextInput 的 maxLength 不设或设为无效值时取默认值 Infinity，不限字数；TextArea 的 maxLength 默认也没有上限
- 〔适用情境 / 做法第 1 步〕TextInput 的 caretColor 不写时为 '#007DFF'；API 12 起它同时决定文本选择手柄的颜色
- 〔适用情境 / 做法第 1、5 步〕主题继承 Theme.Material、主题链上（含依赖库主题）都没有另设 textCursorDrawable 时，输入框光标是 text_cursor_material：2dp 宽，按主题的 colorControlActivated 着色；Theme.Material 没覆盖时 colorControlActivated 取 ?attr/colorAccent；平台旧主题 Theme 的 textCursorDrawable 为 @null
- 〔适用情境 / 做法第 1 步〕图片视图没写具体尺寸时，BitmapDrawable 把位图从所在密度桶缩放到屏幕密度显示，等于固定的 dp 数：dp = px × 160 ÷ 桶的 dpi（mdpi 160、hdpi 240、xhdpi 320、xxhdpi 480、xxxhdpi 640）
- 〔适用情境 / 做法第 1 步〕ArkUI 组件不设 width 时取能完整容纳内容的宽度；Image 的 objectFit 只决定图片在组件框里怎么缩放，默认 ImageFit.Cover；Length 写 number 时单位是 vp
- 〔适用情境 / 做法第 7 步〕应用主题和工具栏样式都没有另设 actionBarSize 时，?attr/actionBarSize 的值随主题族不同：Theme.Material3.* 为 64dp（m3_appbar_size_compact → m3_comp_top_app_bar_small_container_height，material 1.12.0）；Theme.MaterialComponents.* 为 mtrl_toolbar_default_height 56dp（material 1.12.0）；Theme.AppCompat.* 为 abc_action_bar_default_height_material 56dp（appcompat 1.7.1）
- 〔原因 / 做法第 6 步〕Text 的 fontSize 传 number 时单位是 fp；不设时默认 16fp（穿戴设备上 15fp）
- 〔适用情境 / 做法第 1 步〕Stack 的 alignContent 默认 Alignment.Center，子组件默认居中摆放；通用属性 align 在 Stack 上与 alignContent 效果一致，在其他组件上对齐的是组件自己绘制区域里的内容；position 传 Edges 时按组件各边到父组件内容区相应边的距离定位
- 〔适用情境 / 做法第 1 步〕FrameLayout 的子视图没写 layout_gravity 时按 DEFAULT_CHILD_GRAVITY（Gravity.TOP | Gravity.START）摆放，即贴左上（RTL 下贴右上）
- 〔适用情境 / 做法第 1 步〕AppStorageV2.connect 未指定 key 时，第二个参数当默认构造器、用 type 的 name 作 key；关联 @Observed 对象时该类型的 name 属性未定义，要指定 key 或自定义 name；key 建议只由字母、数字、下划线组成，长度不超过 255，使用非法字符或空字符的行为未定义
- 〔适用情境 / 做法第 1 步〕AppStorageV2、PersistenceV2 的 key 含连字符或点号时编译通过，运行时报错：连字符 key 下 AceStateMgmt 输出 “Cannot use the key! The value of key can only consist of letters, digits and underscores”，点号 key 下 hilog 报 invalid AppStorageV2 key
- 〔适用情境 / 做法第 7 步〕API 23 上 XmlPullParser.parseXml 的上报顺序是：开始标签的 START_TAG token，接着是这个元素各属性的回调，然后才是下一个 token；在 START_TAG 到达时就按已累积的属性组装元素，会把上一元素的属性记到下一元素上
