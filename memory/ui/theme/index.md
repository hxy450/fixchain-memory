# ui/theme

主题、语义色、排版样式、控件默认样式与 style 继承属性（圆角、高度、渐变、字号）的迁移：宿主、foundation 组件、依赖库与 Android 框架主题（Theme.Holo 等，值取本机 SDK 平台资源）隐式提供的外观，ArkUI 组件自带默认外观的显式覆盖，Material 库组件与框架主题组件（如 PreferenceActivity 偏好列表）的默认几何与内部留白，深浅主题状态的可观察与渲染期取色、应用内切换时命令式取色与系统栏的重解析，?attr 主题属性色按各主题导出颜色键、深色资源键的同步追加，多字重字体的注册，被引用 drawable 的取值，同时设圆角与描边时 border() 对圆角的覆盖，Compose Brush 渐变背景，视觉属性逐项取自源布局与适配器，颜色约束的写法，以及按色值与字号选择资源键，DayNight 框架默认色按深浅两态成对建 token

[上一级](../index.md)

## 本级经验

- [Compose 以 Brush 渐变着色的背景迁为 linearGradient：把调色板名解析成具体色序，透明 Surface 背景设透明，不压成单一品牌色](lesson-46805f8bf5da7b0c914b.lesson.md)
  - 时机：界面实现与共享组件实现阶段，把 Compose 按钮、卡片的 Brush.horizontalGradient(colors.xxx) 背景，或页面里已有的渐变字面色值落为 ArkUI linearGradient 与颜色资源时
  - 情境：源组件用主题中的渐变列表（如 JetsnackTheme.colors.interactivePrimary、gradient2_2）经 Brush 着色，常配 Surface(color = Transparent)；目标要求颜色走 color.json 资源引用，而 color.json 只收录了调色板的部分色阶。
- [“页面零硬编码色值”只禁止字面色值，不禁止用 $r 引用语义色](lesson-2e4279c4b82f06af64fd.lesson.md)
  - 时机：规格提取阶段书写颜色约束，或页面实现阶段解读规格里的颜色约束时
  - 情境：规格或功能说明写有“页面代码零硬编码色值”“深浅色由资源限定词目录负责”等全局约束，而具体控件仍需要与源端一致的颜色。
- [主题提供的颜色按各主题与深浅两态取值导出成对 base/dark 键：先把引用分成 ?attr 主题属性与 @color 写死两类，values-night 同名 style 未写的主题属性回落框架深色默认；取 Android 框架实际值，不以目标平台 sys token 代替](lesson-1856958fc6d369f0e2bb.lesson.md)
  - 时机：资源前置、规格提取或界面实现阶段，为引用 ?attr 的图标 fillColor、工具栏主题色、自绘组件前景色或文字色新建或选择颜色 token 时；把 AppCompat DayNight 应用（含日间覆写主题色、values-night 重新定义同名 AppTheme 的情况）映射为 base/dark 颜色资源与页面配色时
  - 情境：源图标与控件颜色来自主题属性（应用自定义的图标色属性、colorControlNormal=colorOnSurface、colorOnSecondary 等），各主题取值不同；目标 SVG 只保留浅色值，color.json 可能缺对应键。也包括 AppTheme 只继承 Theme.AppCompat.DayNight、没有 values-night、没有 colorPrimary/colorAccent 覆写：窗口、对话框、ActionBar、状态栏、按钮、主次文字、提示、禁用、强调色与分隔线都来自框架默认并随深浅色变化。也包括日间 AppTheme 覆写了 colorPrimary/colorPrimaryDark/colorAccent，values-night 重新定义同名 AppTheme 却没写这些项：夜间回落 AppCompat 深色默认（#212121/#000000/#80CBC4），布局中 ?attr/colorPrimary 处随之变色，@color/colorPrimary 写死处保持不变。规格可能把业务调色板镜像到 dark 当作深色适配，各页转换器各自补键、按某一模式写死 white，或改用目标平台 sys.color 语义色。
- [同时需要圆角与描边时把 radius 写进 .border()](lesson-8b7c4ece5e5bf7704a44.lesson.md)
  - 时机：界面实现阶段，为同一视图设置圆角与描边（按钮 cornerRadius 加 stroke、OutlinedBox、GradientDrawable setStroke）时
  - 情境：目标写成 .borderRadius(X) 后接不带 radius 的 .border({ width, color })；映射参考可能把圆角与描边分列成两个属性。
- [多字重字族按“族-字重”逐文件 registerFont，排版样式引用注册名，入口调用一次注册](lesson-046baeb5ffbb10a6abc5.lesson.md)
  - 时机：主题令牌阶段，把 Compose FontFamily(Font(R.font.x, weight), ...) 迁到 ArkUI，或确定全局字体注册由谁调用时
  - 情境：源字族为同一族声明多个字重文件，资源阶段已把字体文件放进 rawfile；目标要先 registerFont 才能用 fontFamily 引用；主题令牌、公共组件、页面与入口由不同任务分批生成。
- [委托 Material/AppCompat 库或平台框架（Theme.Holo、android.preference、框架 AlertDialog）提供外观的组件，先在本机 SDK 平台资源或依赖库 res（含 values-land、values-sw600dp 等限定目录）查默认外观与几何，查过仍无才标待核；内部留白按库规则分侧落实](lesson-5a82d62ff7e087616968.lesson.md)
  - 时机：规格提取与界面实现阶段，翻译只显式传入部分参数、其余外观交给 Material3 库默认的组件（Slider、Snackbar、TopAppBar 等），或源码没写 padding、留白由库组件内部布局提供时；为 View 体系的工具栏、底部导航、FAB、按钮、TabLayout、偏好分组标题确定高度、字号字重、圆角与配色，而布局 XML 未写具体值时；把 android.preference 的 PreferenceActivity/PreferenceFragment 偏好列表与 ListPreference、框架 AlertDialog 转成目标行与对话框，确定行几何、分类头、分隔线、对话框几何与行内控件类型时；判断这些默认值是否随横竖屏或窗口宽度变化时
  - 情境：源组件只传少数颜色或尺寸，thumb 形状、留隙、刻度、容器高度、内距等来自库默认与 MaterialTheme；TopAppBar 等容器的标题槽、导航与动作槽留白由库内部布局决定，源码本身没有 padding 修饰符；目标组件的内置样式与之不同。也包括 View 体系源用 ?attr/actionBarSize、MaterialToolbar、BottomNavigationView、TabLayout、未写 style 的 FAB 或 OutlinedButton，取值由 Theme.Material3.*、MaterialComponents 或 AppCompat 父主题与组件默认样式决定，且库在 values-land、values-sw600dp 下另有取值（如 AppCompat 横屏 actionBarSize 48dp、Toolbar 标题 14dp；TabLayout 横屏 tabGravity=center），应用自身 res 没有对应覆盖。也包括 PreferenceFragment（preference_material）行、ListView 分隔线、框架 AlertDialog 与 ListPreference 单选对话框，几何在本机 SDK 平台资源里。也包括 View 体系 Activity 继承 android.preference.PreferenceActivity、主题为 Theme.Holo，页面没有布局 XML，复选框、分类头、行高与内边距、列表左右内边距、分隔线规则由平台 preference_holo 等布局与资源隐式提供。
- [布局引用的 @drawable（progressDrawable、背景 shape、标签背景、光标 shape）先打开取数值：高度、圆角、轨道色、渐变、描边与光标宽色写进规格与实现](lesson-771d1ba1a032b769097a.lesson.md)
  - 时机：规格提取与界面实现阶段，为进度条、搜索框、分组标签等引用 drawable 的控件确定高度、圆角、颜色与描边时
  - 情境：源布局以 progressDrawable=@drawable/xxx、background=@drawable/bg_xxx 引用 layer-list/shape 资源，尺寸、圆角、轨道色、渐变和描边写在被引用文件里；目标工程可能已有名称相近、含义不同的颜色资源。也包括 EditText 用 textCursorDrawable 引用 shape 定义光标宽度与颜色，且只设在部分字段上。
- [应用内主题切换不只依赖 setColorMode：命令式取色、系统栏与画布要随主题重解析](lesson-f1069f514c0eb98702fb.lesson.md)
  - 时机：实现阶段，设计应用内深浅色切换，并为系统栏、Canvas、HTML 样式等非 $r 消费点取色时
  - 情境：源换主题靠 Activity 重建；目标用 ApplicationContext.setColorMode 切换，同时存在 getColorSync 取色、setWindowSystemBarProperties 内容色、Canvas 画笔色与内联 CSS。
- [引用 style 或抽成共享 @Builder 的控件：先展开共享默认值，再逐实例叠加元素自身的覆写（字号、圆角、间距）；圆角不按半高推，也不照抄相邻控件](lesson-bc5b8558ab086168b462.lesson.md)
  - 时机：界面实现阶段（含返修期重写弹窗或按钮），为通过 style 继承形状、尺寸与渐变的控件确定修饰链时；把重复 XML 元素抽成 @Builder 时；为 TextView 的 maxLines/lines、TextAppearance 字号字重行高，或 LinearProgressIndicator 等 Material 控件的轨道色确定取值时
  - 情境：源 XML 控件以 style="@style/X" 继承圆角、高度、渐变等属性，元素本身只覆写部分项；同一或相邻布局里有圆角更大的卡片，或同 style 但显式覆写成胶囊的按钮。或按键等控件以 style 给默认 textSize、单个控件再覆写不同字号；多个同构元素（分组标题）各自带不同的 layout_marginTop。也包括 maxLines/lines、TextAppearance 与 trackColor 来自 style 引用或 Material 控件默认样式，布局 XML 本身没写。也包括 TextView 只声明 textAppearance（如 ?android:attr/textAppearanceMedium）而没写 textColor，映射参考只说“展开为样式”，写者只取了字号。
- [把主题、控件默认样式或依赖库隐式提供的外观写成目标显式样式：按“控件 style → 祖先布局 android:theme 覆盖 → Activity 主题 → 应用主题”定位提供方并解析到值（框架主题查本机 SDK 平台资源），部分属性显式时其余仍取控件默认；未写颜色的 TextView 取次文字色 textColorSecondary，EditText 才取主文字色](lesson-47785524c7f132ea7efe.lesson.md)
  - 时机：规格提取阶段写控件转换决策，或页面实现阶段写出按钮、文本、工具栏等控件的修饰链时；为带 android:theme 覆盖（ThemeOverlay）的 AppBarLayout/Toolbar 定色时；为只显式写了部分属性的 Button、未写颜色的 TextView、SwitchPreference 开关、NavigationView 菜单项确定默认外观时；为未写 tint/color 的 Compose Icon、Text 着色，翻译未传 textStyle 的 BasicTextField，或迁移 GlanceTheme 等依赖库主题色时；把 CheckBox、RadioButton、MaterialButton、TabLayout、EditText/Spinner、工具栏 SearchView 等 Material 控件映射为 ArkUI 组件时；为框架主题提供的窗口背景、文字色、列表分隔线、文字行框（单行与多行），以及平台 drawable 状态背景（ImageWell 按钮、EditText、SeekBar 的位图或 9-patch，Material CheckBox/RadioButton 的向量）确定目标取值时
  - 情境：源布局中的控件没有声明（或只声明了部分）background / backgroundTint / textColor / 圆角 / 字重 / 投影，外观来自应用主题、控件默认样式或祖先布局上的 android:theme 覆盖；ArkUI 对应组件不设样式时使用平台默认外观。也包括 AppBarLayout/Toolbar 以 android:theme 指定 ThemeOverlay（如 AppBarOverlay 的父样式为 ThemeOverlay.AppCompat.Light），而 Activity 主题是 DarkActionBar。也包括 Button/AppCompatButton 只写了 background、textColor、textSize，没有 style、textAllCaps、stateListAnimator、elevation，或自定义 View 继承 AppCompatButton 只换背景。也包括 TextView 未声明 textColor/textAppearance/style（缺省 textAppearanceSmall：次文字色、14sp、includeFontPadding）与 EditText 未声明 textColor（缺省主文字色）。也包括 PreferenceFragment 的 SwitchPreference 开关、未写 item 样式的 NavigationView 菜单项。也包括 Compose 的 Icon/Text 未写 tint/color、颜色来自宿主 Surface 的 LocalContentColor；foundation 的 BasicTextField 不传 textStyle；颜色来自 GlanceTheme 一类依赖库主题、源码与规格里都没有具体色值。也包括映射参考只给一对一或逐属性映射，而 ArkUI 组件自带的默认外观与源端 Material 默认不同：Checkbox 默认圆形、Radio 默认勾选样式、Toggle 胶囊开关、TextInput/Search/Select 默认填充底、Tabs 默认标签样式。也包括应用主题父链止于 android:Theme.Holo/Material/DeviceDefault 的老工程，外观由框架主题或 style="@android:style/*" 引用提供，本机装有 Android SDK 平台资源。
  - 例外：源控件在应用自有的 layout 或 style 中写出了具体值时，按显式声明转换这些属性；显式声明只覆盖被声明的几项，其余属性仍按控件默认样式补齐；style="@android:style/*" 或 ?android:attr 引用不算显式声明；决策记录明确要求目标端采用平台默认外观
- [按源端实际色值与字号在资源里反查同值键：主题语义色、排版样式先解析到值，不按 accent、primary、title/body 等名称或别页令牌选键](lesson-4e9507a2a793c5583aa8.lesson.md)
  - 时机：界面实现阶段，为按钮、背景、文字与渐变色阶设置颜色资源引用，或为文本绑定字号资源令牌时
  - 情境：源端颜色以 shapeSolidColor、background、textColor 等硬编码色值或色值资源给出；目标工程已有多组语义名相近但色值不同的颜色资源（如脚手架留下的 color_accent 与迁移出的 brand_accent）。也包括 Compose 源端以主题语义色（如 colors.textPrimary）或排版样式（如 MaterialTheme.typography.titleMedium）取值，而目标 color.json/float.json 只有部分令牌：有名称相近或其他页面前缀的键（text_secondary、feed_font_title），缺同值键，流程要求缺令牌时报告 design_tokens_missing。也包括用 text_size_large、text_size_small 一类名称暗示大小的命名资源承载源端数值（如 16sp 标题、12sp 信息条），或同一组件中语义不同的颜色（进度轨道与选中行底色）准备共用一个已有 token。也包括 Java 以 Color.GREEN、Color.RED 等框架颜色常量着色，规格映射成名称相近、色值不同的应用色（如 light_green #FF66FF66）。
- [深浅主题状态放在可观察对象里并由入口同步，组件在渲染期读取主题色](lesson-7b19b801e0f21481d1d6.lesson.md)
  - 时机：主题层实现深浅色切换，以及组件、页面读取主题色（含对主题色做插值等数值运算）时
  - 情境：源端 Theme(darkTheme = isSystemInDarkTheme()) 经 CompositionLocal 下发两套颜色，组件在组合期读取；目标用模块级主题函数与 $r 颜色资源实现，由入口读取系统 colorMode。也包括源端对 MaterialTheme.colorScheme 的颜色做数值插值（如按折叠比例 lerp 顶栏容器色），而 $r 资源不能直接参与运算。
- [源端一个背景选择对象同时表达图片、单色与渐变时，逐分支迁移到目标渲染绑定：url 非空用图片，否则按颜色数与方向生成纯色或渐变](lesson-2dc88a09f6cfbbe3393c.lesson.md)
  - 时机：渲染实现阶段，把编辑器的背景选择对象绑定到预览或组件的背景渲染节点时
  - 情境：源端一个选择对象同时承载 url、colors、orientation，渲染方法按 url 非空→图片、colors 长度 1→纯色、长度 2→按方向渐变分支；目标在模型层把选择对象映射到运行时渲染属性，外观配置模块已能保存与恢复 colors 和 orientation。
- [视觉属性逐项取自源布局、item 布局与适配器分支，缺项就补读，不以近似值、通用卡片或自拟分隔线代替；菜单行与操作栏的图标、按状态切换的图与颜色同列清单](lesson-e4e65a99e545871f96ae.lesson.md)
  - 时机：界面转换与视觉返修阶段，确定标题栏背景、文字颜色与字号、周末与选中样式、item 尺寸、胶囊圆角、行高与分隔线时；把弹出菜单行、列表分组标题与批量操作底栏转成组件时
  - 情境：页面规格只给合成的结构（无颜色与尺寸），视觉数值分散在 Fragment 布局、include 布局、item 布局与适配器 convert 分支里；转换者可能只读到部分文件，或读到了却按经验取整。 也包括增量迁移的差异清单与规格只按功能行为描述新入口，菜单行或操作按钮由 ImageView 加 TextView 组成、标题用 drawableLeft 图标与专用颜色资源，部分图标随选中状态切换。
- [追加主题颜色资源时同一次写深色限定目录的同名键，已存在的资源文件只追加不覆盖](lesson-1e972af4bc7e27b23d9c.lesson.md)
  - 时机：页面转换或资源阶段，为主题色追加颜色资源键时
  - 情境：源主题有 Light/Dark 两套调色板；目标颜色资源分 base 与 dark 限定目录，多个任务会分别追加，部分文件由模板预置。
