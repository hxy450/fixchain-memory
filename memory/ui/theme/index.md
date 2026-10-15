# ui/theme

主题、语义色、排版样式、控件默认样式与 style 继承属性（圆角、高度、渐变、字号）的迁移：宿主、foundation 组件、依赖库与 Android 框架主题（Theme.Holo 等，值取本机 SDK 平台资源）隐式提供的外观，ArkUI 组件自带默认外观的显式覆盖，Material 库组件与框架主题组件（如 PreferenceActivity 偏好列表）的默认几何与内部留白，深浅主题状态的可观察与渲染期取色、应用内切换时命令式取色与系统栏的重解析，?attr 主题属性色按各主题导出颜色键、深色资源键的同步追加，多字重字体的注册，被引用 drawable 的取值，同时设圆角与描边时 border() 对圆角的覆盖，Compose Brush 渐变背景，视觉属性逐项取自源布局与适配器，颜色约束的写法，以及按色值与字号选择资源键，DayNight 框架默认色按深浅两态成对建 token；TextView/EditText 未写文字色时的默认 textAppearance 链，View 体系 Material 控件映射 ArkUI 内置组件，Compose 组件的隐式外观，android.preference 偏好页的平台默认外观

[上一级](../index.md)

## 本级经验

- [Compose 组件未显式给的外观（内容色、文本样式、Material3 组件几何与槽位留白、库主题色）按宿主与库默认解析后写成 ArkUI 显式值](lesson-cea5ceb16e4044504edb.lesson.md)
  - 时机：规格提取与界面实现阶段，为未写 tint/color 的 Compose Icon/Text 着色、翻译未传 textStyle 的 BasicTextField、翻译只显式传入部分参数的 Material3 组件（TopAppBar、Slider、Snackbar、LargeFloatingActionButton 等），或迁移 GlanceTheme 等依赖库主题色时
  - 情境：Compose 的 Icon/Text 未写 tint/color，颜色来自最近宿主 Surface/Scaffold/CompositionLocalProvider 的 LocalContentColor；foundation 的 BasicTextField 不传 textStyle；Material3 组件的 thumb 形状、留隙、容器高度、内距与标题、导航、动作槽留白来自库默认与 MaterialTheme，源码本身没有 padding 修饰符；颜色来自 GlanceTheme 一类依赖库主题，源码与规格里都没有具体色值；目标组件的内置样式与之不同。
- [TextView 未写文字色时按默认 textAppearance 链与主题代际解析，EditText 取 editTextColor](lesson-e9f02c6de64ad68b5b48.lesson.md)
  - 时机：规格提取与界面实现阶段，为源端没写 textColor 的 TextView/AppCompatTextView/EditText，或只写了 textAppearance（如 ?android:attr/textAppearanceMedium）的文本确定文字色与字号时；为顶部对齐、决定纵向排布的单行 TextView 定高时
  - 情境：源布局里的 TextView 没有 textColor、textAppearance、style，或只声明 textAppearance；目标 ArkUI Text 不写 fontColor 时取 ArkUI 默认近黑；工程里可能已有按“主文字色”写的先例、注释或提醒。也包括 TextView 默认 includeFontPadding=true，而 ArkUI Text 没有对应属性。
  - 例外：主题覆盖了 textViewStyle、textAppearanceSmall 或相关颜色属性时，按覆盖后的值解析，不直接套用下面的默认链
- [View 体系 Material 控件映射 ArkUI 内置组件时，先按主题代际列出源端库默认外观与度量，再逐项显式设置 ArkUI 属性](lesson-9694dd3b56dc6ce8164b.lesson.md)
  - 时机：界面实现与规格提取阶段，把 CheckBox、RadioButton、Switch/SwitchPreference、TabLayout、EditText/Spinner、工具栏 SearchView、MaterialToolbar（?attr/actionBarSize）、BottomNavigationView、FAB、OutlinedButton、NavigationView 菜单项或框架 ActionBar 溢出菜单映射为 ArkUI 组件，而布局未写具体样式值时
  - 情境：映射参考只给一对一或逐属性映射，而 ArkUI 组件自带的默认外观与源端 Material 默认不同（Checkbox 默认圆形、Radio 默认勾选样式、Toggle 胶囊开关、TextInput/Select 默认填充底、Tabs 默认标签样式、Menu 为系统定位的圆角卡片）；源端取值由 Theme.Material3.*、MaterialComponents、AppCompat 或框架主题的组件默认样式决定，库在 values-land、values-sw600dp 下可能另有取值；工程里可能有按 M2 默认值或兄弟页先例写的同类组件。
  - 例外：源端为控件写了 widgetLayout、thumb/track、itemIconTint 等具体覆写，或在 style 中写出具体值时，按显式值转换；style 只继承库样式（如 Widget.Material3.Button.OutlinedButton）时仍按本条解析库默认
- [View 控件未显式写的外观由主题、默认样式或依赖库提供时，按提供方链解析到值再写成目标显式样式；部分属性显式时其余仍取默认](lesson-47785524c7f132ea7efe.lesson.md)
  - 时机：规格提取阶段写 View 控件转换决策，或页面实现阶段写按钮、工具栏、列表、输入框等控件的修饰链，而布局与应用 style 没写全外观时；控件或祖先布局带 android:theme 覆盖（ThemeOverlay），或主题父链止于 android:Theme.Holo/Material/DeviceDefault、style 引用 @android:style/* 时
  - 情境：源布局中的控件没有声明（或只声明了部分）background / backgroundTint / textColor / 圆角 / 字重 / 投影 / 最小尺寸，外观来自应用主题、控件默认样式、祖先布局上的 android:theme 覆盖或依赖库；ArkUI 对应组件不设样式时使用平台默认外观。也包括 AppBarLayout/Toolbar 以 android:theme 指定 ThemeOverlay（如父样式为 ThemeOverlay.AppCompat.Light），而 Activity 主题是 DarkActionBar；Button/AppCompatButton 只写了 background、textColor、textSize，或自定义 View 继承 AppCompatButton 只换背景；框架主题提供的窗口背景、列表分隔线与按状态切换的位图背景（ImageWell、EditText、SeekBar）；库在 values-land、values-sw600dp 下另有取值而应用 res 没有覆盖。
  - 例外：源控件在应用自有的 layout 或 style 中写出了具体值时，按显式声明转换这些属性；显式声明只覆盖被声明的几项；style="@android:style/*" 或 ?android:attr 引用不算显式声明
- [android.preference 偏好页的列表行、分类头、行内控件与偏好对话框按平台资源和框架默认行为复刻](lesson-3f95e9d0ad81b3c431e9.lesson.md)
  - 时机：规格提取与界面实现阶段，迁移继承 PreferenceActivity/PreferenceFragment（android.preference，无自定义布局）的设置页，确定行几何、分类头、分隔线与行内控件，以及 EditTextPreference、ListPreference 等点击弹出的对话框时
  - 情境：页面由 addPreferencesFromResource 挂载，没有布局 XML；复选框、分类头、行高与内边距、列表左右内边距、分隔线规则、点击弹出的对话框都由平台 preference_holo/preference_material 等布局与资源隐式提供；代码中看不到 AlertDialog.Builder，规格却把 ListPreference 写成 Select、bindSheet 或“选项单”，或把行内控件写成 Toggle、带尾部箭头的通用列表行，或用估计内距与目标平台 sys 色。
  - 例外：AndroidX Preference（PreferenceFragmentCompat）或带自定义 layout/widgetLayout 的偏好：按库资源与应用布局取值，本条的平台几何不适用
- [“页面零硬编码色值”只禁止字面色值，不禁止用 $r 引用语义色](lesson-2e4279c4b82f06af64fd.lesson.md)
  - 时机：规格提取阶段书写颜色约束，或页面实现阶段解读规格里的颜色约束时
  - 情境：规格或功能说明写有“页面代码零硬编码色值”“深浅色由资源限定词目录负责”等全局约束，而具体控件仍需要与源端一致的颜色。
- [同时需要圆角与描边时把 radius 写进 .border()](lesson-8b7c4ece5e5bf7704a44.lesson.md)
  - 时机：界面实现阶段，为同一视图设置圆角与描边（按钮 cornerRadius 加 stroke、OutlinedBox、GradientDrawable setStroke）时
  - 情境：目标写成 .borderRadius(X) 后接不带 radius 的 .border({ width, color })；映射参考可能把圆角与描边分列成两个属性。
- [多字重字族按“族-字重”逐文件 registerFont，排版样式引用注册名，入口调用一次注册](lesson-046baeb5ffbb10a6abc5.lesson.md)
  - 时机：主题令牌阶段，把 Compose FontFamily(Font(R.font.x, weight), ...) 迁到 ArkUI，或确定全局字体注册由谁调用时
  - 情境：源字族为同一族声明多个字重文件，资源阶段已把字体文件放进 rawfile；目标要先 registerFont 才能用 fontFamily 引用；主题令牌、公共组件、页面与入口由不同任务分批生成。
- [布局引用的 @drawable（progressDrawable、背景 shape、标签背景、光标 shape）先打开文件取数值，再按消费它的属性落成目标写法](lesson-771d1ba1a032b769097a.lesson.md)
  - 时机：规格提取与界面实现阶段，为进度条、搜索框、分组标签等引用 drawable 的控件确定高度、圆角、颜色与描边时
  - 情境：源布局以 progressDrawable=@drawable/xxx、background=@drawable/bg_xxx 引用 drawable XML（如 shape），尺寸、圆角、轨道色、渐变和描边写在被引用文件里；目标工程可能已有名称相近、含义不同的颜色资源。也包括 EditText 用 textCursorDrawable 引用 shape 定义光标宽度与颜色，且只设在部分字段上。
- [应用内主题切换不只依赖 setColorMode：命令式取色、系统栏与画布要随主题重解析](lesson-f1069f514c0eb98702fb.lesson.md)
  - 时机：实现阶段，设计应用内深浅色切换，并为系统栏、Canvas、HTML 样式等非 $r 消费点取色时
  - 情境：源换主题靠 Activity 重建；目标用 ApplicationContext.setColorMode 切换，同时存在 getColorSync 取色、setWindowSystemBarProperties 内容色、Canvas 画笔色与内联 CSS。
  - 例外：应用只跟随系统深浅色、不提供应用内切换：主题状态与渲染期取色见 lesson-7b19b801e0f21481d1d6
- [引用 ?attr 主题属性的颜色按各主题与深浅两态解析后导出成对 base/dark 键；@color 写死的保持常量，不用目标平台 sys 色代替](lesson-1856958fc6d369f0e2bb.lesson.md)
  - 时机：资源前置、规格提取或界面实现阶段，为引用 ?attr 的图标 fillColor、工具栏主题色、自绘组件前景色或文字色新建或选择颜色 token 时；把 AppCompat DayNight 应用（含日间覆写主题色、values-night 重新定义同名 AppTheme 的情况）映射为 base/dark 颜色资源与页面配色时
  - 情境：源图标与控件颜色来自主题属性（应用自定义的图标色属性、colorControlNormal=colorOnSurface、colorOnSecondary 等），各主题取值不同；目标 SVG 只保留浅色值，color.json 可能缺对应键。也包括 AppTheme 只继承 Theme.AppCompat.DayNight、没有 values-night、没有 colorPrimary/colorAccent 覆写：窗口、对话框、ActionBar、状态栏、按钮、主次文字、提示、禁用、强调色与分隔线都来自框架默认并随深浅色变化。也包括日间 AppTheme 覆写了 colorPrimary/colorPrimaryDark/colorAccent，values-night 重新定义同名 AppTheme 却没写这些项：夜间回落 AppCompat 深色默认，布局中 ?attr/colorPrimary 处随之变色，@color/colorPrimary 写死处保持不变。规格可能把业务调色板镜像到 dark 当作深色适配，各页转换器各自补键、按某一模式写死 white，或改用目标平台 sys.color 语义色。
- [引用 style 或抽成共享 @Builder 的控件：先展开共享默认值，再逐实例叠加元素自身的覆写（字号、圆角、间距）；圆角不按半高推，也不照抄相邻控件](lesson-bc5b8558ab086168b462.lesson.md)
  - 时机：界面实现阶段（含返修期重写弹窗或按钮），为通过 style 继承形状、尺寸与渐变的控件确定修饰链时；把重复 XML 元素抽成 @Builder 时；为 TextView 的 maxLines/lines、TextAppearance 字号字重行高，或 LinearProgressIndicator 等 Material 控件的轨道色确定取值时
  - 情境：源 XML 控件以 style="@style/X" 继承圆角、高度、渐变等属性，元素本身只覆写部分项；同一或相邻布局里有圆角更大的卡片，或同 style 但显式覆写成胶囊的按钮。或按键等控件以 style 给默认 textSize、单个控件再覆写不同字号；多个同构元素（分组标题）各自带不同的 layout_marginTop。也包括 maxLines/lines、TextAppearance 与 trackColor 来自 style 引用或 Material 控件默认样式，布局 XML 本身没写。也包括 TextView 只声明 textAppearance（如 ?android:attr/textAppearanceMedium）而没写 textColor，映射参考只说“展开为样式”，写者只取了字号。
- [按源端实际色值与字号在资源里找同值键：主题语义色、排版样式与渐变调色板先解析到值，不按 accent、primary、title/body 等名称选键](lesson-4e9507a2a793c5583aa8.lesson.md)
  - 时机：界面实现阶段，为按钮、背景、文字与渐变色阶设置颜色资源引用，或为文本绑定字号资源令牌时；把 Compose Brush 渐变背景（Brush.horizontalGradient(调色板)）落为 ArkUI linearGradient 时
  - 情境：源端颜色以 shapeSolidColor、background、textColor 等硬编码色值或色值资源给出；目标工程已有多组语义名相近但色值不同的颜色资源（如 color_accent 与 brand_accent）。也包括 Compose 源端以主题语义色（如 colors.textPrimary）、排版样式（如 MaterialTheme.typography.titleMedium）或调色板列表（Brush.horizontalGradient(colors.xxx)，可能配 Surface(color = Transparent)）取值，而目标 color.json/float.json 只有部分令牌、缺同值键，流程要求缺令牌时报告 design_tokens_missing；用 text_size_large 一类名称暗示大小的资源承载源端数值；同一组件中语义不同的颜色准备共用一个已有 token；Java 以 Color.GREEN、Color.RED 等框架颜色常量着色，规格映射成名称相近、色值不同的应用色。
- [深浅主题状态放在可观察对象里并由入口同步，组件在渲染期读取主题色](lesson-7b19b801e0f21481d1d6.lesson.md)
  - 时机：主题层实现深浅色切换，以及组件、页面读取主题色（含对主题色做插值等数值运算）时
  - 情境：源端 Theme(darkTheme = isSystemInDarkTheme()) 经 CompositionLocal 下发两套颜色，组件在组合期读取；目标用模块级主题函数与 $r 颜色资源实现，由入口读取系统 colorMode。也包括源端对 MaterialTheme.colorScheme 的颜色做数值插值（如按折叠比例 lerp 顶栏容器色），而 $r 资源不能直接参与运算。
- [源端渲染方法按同一配置对象的字段分支（图片、纯色、渐变、空值恢复默认）时，逐分支迁移到目标渲染绑定](lesson-2dc88a09f6cfbbe3393c.lesson.md)
  - 时机：渲染实现阶段，源端同一方法里按条件分支生成 ColorDrawable（单色）、按方向生成 GradientDrawable（渐变）或加载图片地址，目标准备把这个配置对象映射到运行时渲染属性时
  - 情境：源端一个配置对象同时承载图片地址、颜色列表与方向（例：url、colors、orientation），渲染方法按“地址非空 → 图片、颜色数为 1 → 纯色、为 2 → 按方向渐变、对象为空 → 恢复默认”分支；目标外观配置模块已能保存与恢复这些字段。
- [追加主题颜色资源时同一次写深色限定目录的同名键，已存在的资源文件只追加不覆盖](lesson-1e972af4bc7e27b23d9c.lesson.md)
  - 时机：页面转换或资源阶段，为主题色追加颜色资源键时
  - 情境：源主题有 Light/Dark 两套调色板；目标颜色资源分 base 与 dark 限定目录，多个任务会分别追加，部分文件由模板预置。
- [页面视觉数值分散在布局、item 布局与适配器分支时逐项取值，缺项补读，不以近似值、通用卡片或自拟分隔线代替](lesson-e4e65a99e545871f96ae.lesson.md)
  - 时机：界面转换与实现阶段，确定标题栏背景、文字颜色与字号、按状态区分的样式（选中、当前项、特殊项）、item 尺寸、胶囊圆角、行高与分隔线时；把弹出菜单行、列表分组标题与批量操作底栏转成组件时
  - 情境：页面规格只给合成的结构（无颜色与尺寸），视觉数值分散在 Fragment 布局、include 布局、item 布局与适配器 convert 分支里；转换者可能只读到部分文件，或读到了却写成近似值。也包括差异清单与规格只按功能行为描述新入口，菜单行或操作按钮由 ImageView 加 TextView 组成、标题用 drawableLeft 图标与专用颜色资源，部分图标随选中状态切换。
