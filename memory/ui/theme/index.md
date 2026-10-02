# ui/theme

主题、语义色、排版样式、控件默认样式与 style 继承属性（圆角、高度、渐变、字号）的迁移：宿主、foundation 组件与依赖库隐式提供的外观，Material3 库组件的默认几何与内部留白，深浅主题状态的可观察与渲染期取色、深色资源键的同步追加，多字重字体的注册，被引用 drawable 的取值，Compose Brush 渐变背景，视觉属性逐项取自源布局与适配器，颜色约束的写法，以及按色值与字号选择资源键

[上一级](../index.md)

## 本级经验

- [Compose 以 Brush 渐变着色的背景迁为 linearGradient：把调色板名解析成具体色序，透明 Surface 背景设透明，不压成单一品牌色](lesson-46805f8bf5da7b0c914b.lesson.md)
  - 时机：界面实现与共享组件实现阶段，把 Compose 按钮、卡片的 Brush.horizontalGradient(colors.xxx) 背景，或页面里已有的渐变字面色值落为 ArkUI linearGradient 与颜色资源时
  - 情境：源组件用主题中的渐变列表（如 JetsnackTheme.colors.interactivePrimary、gradient2_2）经 Brush 着色，常配 Surface(color = Transparent)；目标要求颜色走 color.json 资源引用，而 color.json 只收录了调色板的部分色阶。
- [“页面零硬编码色值”只禁止字面色值，不禁止用 $r 引用语义色](lesson-2e4279c4b82f06af64fd.lesson.md)
  - 时机：规格提取阶段书写颜色约束，或页面实现阶段解读规格里的颜色约束时
  - 情境：规格或功能说明写有“页面代码零硬编码色值”“深浅色由资源限定词目录负责”等全局约束，而具体控件仍需要与源端一致的颜色。
- [多字重字族按“族-字重”逐文件 registerFont，排版样式引用注册名，入口调用一次注册](lesson-046baeb5ffbb10a6abc5.lesson.md)
  - 时机：主题令牌阶段，把 Compose FontFamily(Font(R.font.x, weight), ...) 迁到 ArkUI，或确定全局字体注册由谁调用时
  - 情境：源字族为同一族声明多个字重文件，资源阶段已把字体文件放进 rawfile；目标要先 registerFont 才能用 fontFamily 引用；主题令牌、公共组件、页面与入口由不同任务分批生成。
- [委托 Material3 库的组件，默认外观、几何与内部留白从对应版本的库 Tokens 与源码取值，内部留白按库规则分侧落实](lesson-5a82d62ff7e087616968.lesson.md)
  - 时机：规格提取与界面实现阶段，翻译只显式传入部分参数、其余外观交给 Material3 库默认的组件（Slider、Snackbar、TopAppBar 等），或源码没写 padding、留白由库组件内部布局提供时
  - 情境：源组件只传少数颜色或尺寸，thumb 形状、留隙、刻度、容器高度、内距等来自库默认与 MaterialTheme；TopAppBar 等容器的标题槽、导航与动作槽留白由库内部布局决定，源码本身没有 padding 修饰符；目标组件的内置样式与之不同。
- [布局引用的 @drawable（progressDrawable、背景 shape、标签背景）先打开取数值：高度、圆角、轨道色、渐变与描边写进规格与实现](lesson-771d1ba1a032b769097a.lesson.md)
  - 时机：规格提取与界面实现阶段，为进度条、搜索框、分组标签等引用 drawable 的控件确定高度、圆角、颜色与描边时
  - 情境：源布局以 progressDrawable=@drawable/xxx、background=@drawable/bg_xxx 引用 layer-list/shape 资源，尺寸、圆角、轨道色、渐变和描边写在被引用文件里；目标工程可能已有名称相近、含义不同的颜色资源。
- [引用 style 或抽成共享 @Builder 的控件：先展开共享默认值，再逐实例叠加元素自身的覆写（字号、圆角、间距）；圆角不按半高推，也不照抄相邻控件](lesson-bc5b8558ab086168b462.lesson.md)
  - 时机：界面实现阶段（含返修期重写弹窗或按钮），为通过 style 继承形状、尺寸与渐变的控件确定修饰链时；把重复 XML 元素抽成 @Builder 时
  - 情境：源 XML 控件以 style="@style/X" 继承圆角、高度、渐变等属性，元素本身只覆写部分项；同一或相邻布局里有圆角更大的卡片，或同 style 但显式覆写成胶囊的按钮。或按键等控件以 style 给默认 textSize、单个控件再覆写不同字号；多个同构元素（分组标题）各自带不同的 layout_marginTop。
- [把 Android 主题、Compose 宿主或依赖库隐式提供的外观写成目标控件的显式样式，取值来自实际提供方](lesson-47785524c7f132ea7efe.lesson.md)
  - 时机：规格提取阶段写控件转换决策，或页面实现阶段写出按钮等控件的修饰链时；为未写 tint/color 的 Compose Icon、Text 着色，翻译未传 textStyle 的 BasicTextField，或迁移 GlanceTheme 等依赖库主题色时
  - 情境：源布局中的 Button 等控件没有声明 background / backgroundTint / textColor / 圆角，外观来自应用主题（如 Theme.MaterialComponents 的 colorPrimary、colorOnPrimary）；目标工程已迁移同名语义色资源，而 ArkUI 对应组件不设样式时使用平台默认外观。也包括 Compose 的 Icon/Text 未写 tint/color、颜色来自宿主 Surface 的 LocalContentColor，而相邻页面或组件里有显式写 iconPrimary、brand 的图标可供照搬。也包括 foundation 的 BasicTextField 不传 textStyle（默认 TextStyle.Default，不读 Material 排版），以及颜色来自 GlanceTheme 一类依赖库主题、源码与规格里都没有具体色值。
  - 例外：源控件已在布局或 style 中显式声明样式，此时按显式声明转换；决策记录明确要求目标端采用平台默认外观
- [按源端实际色值与字号在资源里反查同值键：主题语义色、排版样式先解析到值，不按 accent、primary、title/body 等名称或别页令牌选键](lesson-4e9507a2a793c5583aa8.lesson.md)
  - 时机：界面实现阶段，为按钮、背景、文字与渐变色阶设置颜色资源引用，或为文本绑定字号资源令牌时
  - 情境：源端颜色以 shapeSolidColor、background、textColor 等硬编码色值或色值资源给出；目标工程已有多组语义名相近但色值不同的颜色资源（如脚手架留下的 color_accent 与迁移出的 brand_accent）。也包括 Compose 源端以主题语义色（如 colors.textPrimary）或排版样式（如 MaterialTheme.typography.titleMedium）取值，而目标 color.json/float.json 只有部分令牌：有名称相近或其他页面前缀的键（text_secondary、feed_font_title），缺同值键，流程要求缺令牌时报告 design_tokens_missing。
- [深浅主题状态放在可观察对象里并由入口同步，组件在渲染期读取主题色](lesson-7b19b801e0f21481d1d6.lesson.md)
  - 时机：主题层实现深浅色切换，以及组件、页面读取主题色时
  - 情境：源端 Theme(darkTheme = isSystemInDarkTheme()) 经 CompositionLocal 下发两套颜色，组件在组合期读取；目标用模块级主题函数与 $r 颜色资源实现，由入口读取系统 colorMode。
- [视觉属性逐项取自源布局、item 布局与适配器分支，缺项就补读，不以近似值、通用卡片或自拟分隔线代替](lesson-e4e65a99e545871f96ae.lesson.md)
  - 时机：界面转换与视觉返修阶段，确定标题栏背景、文字颜色与字号、周末与选中样式、item 尺寸、胶囊圆角、行高与分隔线时
  - 情境：页面规格只给合成的结构（无颜色与尺寸），视觉数值分散在 Fragment 布局、include 布局、item 布局与适配器 convert 分支里；转换者可能只读到部分文件，或读到了却按经验取整。
- [追加主题颜色资源时同一次写深色限定目录的同名键，已存在的资源文件只追加不覆盖](lesson-1e972af4bc7e27b23d9c.lesson.md)
  - 时机：页面转换或资源阶段，为主题色追加颜色资源键时
  - 情境：源主题有 Light/Dark 两套调色板；目标颜色资源分 base 与 dark 限定目录，多个任务会分别追加，部分文件由模板预置。
