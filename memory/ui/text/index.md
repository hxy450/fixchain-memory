# ui/text

文本展示与排版：源端对展示文本的加工（富文本、链接识别与点击）到 ArkUI Text/StyledString 的转换，Compose 行高到单行文本盒与多行行距的映射，多行末行省略的截断粒度，静态说明页的逐字文案与图文结构，Tab、页面标题、设置行等可见文案的逐字取值，以及字符串资源生成哪些语言限定目录，单行中间/开头省略的测量截断，setSpan 区间拆成 Span 时的着色范围，以及数值显示精度（复用基类格式化 getter 与品类精度不一致时的子类覆写），以及源端代码格式化文案的参数化字符串资源

[上一级](../index.md)

## 本级经验

- [SpannableString.setSpan(start, end) 拆成 ArkUI Span 时按 end 为开区间逐字核对着色范围](lesson-eb59a95e5eb219c238b0.lesson.md)
  - 时机：界面实现阶段，把源端 setSpan 着色、加粗的文字拆成 ArkUI Text + Span 时
  - 情境：源端用 SpannableString.setSpan(span, start, end, flags) 按字符索引给一段文字着色，常见“固定前缀 + 动态值 + 后缀”的拼接，终点按前缀长度加动态值长度再加偏移计算。
- [Tab 标签、页面标题与设置行等可见文案沿资源引用链取源端 strings 资源的逐字值，不用枚举名、路由名或自拟英文](lesson-31ab9f59945e5f0259ea.lesson.md)
  - 时机：界面实现阶段，为 Tab 标签、页面/路由标题、设置入口行等可见文案取值并写入页面与路由表时；以及派发侦察或规格任务、确定导航与标题字段的形态时
  - 情境：源端可见文案经资源键间接引用（导航目的地的 label、配置路由的标题资源、顶栏 title），常与目的地枚举名或功能名不同（如 Map 目的地显示“Mesh Map”、Messages 目的地的页面标题为“Conversations”）；目标以硬编码字符串或自建资源表承载；上游 brief 或页面规格已给出、或可从 strings.xml 解析出逐字值。
- [分开单行文本盒与多行行距，不把 Compose lineHeight 同名直映为 ArkUI .lineHeight](lesson-2a2924aaebbfbea80780.lesson.md)
  - 时机：规格提取、主题实现或页面转换阶段，把 Compose 排版令牌落成 ArkUI 文本属性或据文本高度推算容器尺寸时；视觉修复阶段改写主题层行高公式时
  - 情境：源 TextStyle 声明 fontSize/lineHeight、未设 lineHeightStyle；目标准备给所有 Text 无条件设置 .lineHeight()，或把 lineHeight 数值当单行文本的实际盒高来推算横向列表等容器的显式高度；映射参考可能给出 lineHeight → .lineHeight() 的 1:1 对应。
  - 例外：当前源端的 LineHeightStyle、字体内边距或已有明确契约要求固定行盒时，保留该契约，不默认改成自然高度。
- [动态布局文本的字号、行距按源端 dp × 文字倍率落成 vp，只有 bounds、padding、背景等几何乘设计画布比例](lesson-4c494b9f89c7e9db2b55.lesson.md)
  - 时机：动态或灵活组件的渲染实现阶段，把源端动态布局文本的字号、行距换算成 ArkUI 预览、测量或原生绘制尺寸时
  - 情境：源端动态文本以 fontSize.dpF × dynamicTextScale × fontSizeScale 设字号、以 lineSpacing.dpF 设行距，只有节点宽高、位置、padding、背景按根尺寸与设计宽度之比缩放；目标预览用 renderWidth / document.width 一类画布比例统一换算几何。
- [单行 ellipsize=middle/start 在目标 TextOverflow 没有同名成员时实现测量式中间截断，不降级为尾部省略](lesson-a184209501ba02cb62e7.lesson.md)
  - 时机：界面实现阶段，转换单行文本的省略位置（ellipsize），而目标 TextOverflow 枚举没有对应成员时
  - 情境：源 TextView 用 android:ellipsize="middle"（或 start）配合 lines=1/maxLines=1 显示文件名等尾部有意义的文本，可能还有关键字 Span 高亮；ArkUI Text 的 TextOverflow 只有尾部 Ellipsis 等模式，映射参考只给 end → Ellipsis 示例。
  - 例外：项目已批准以尾部省略作为平台差异
- [只为源端实际存在的 values-&lt;语言&gt; 目录生成目标语言限定字符串；单语源不合成 zh_CN 等译文](lesson-b58df29f032cc6a8c9d6.lesson.md)
  - 时机：资源迁移阶段，决定目标工程生成哪些语言限定字符串目录（base、zh_CN 等）及各键取值时
  - 情境：Android 源只有默认 res/values/strings.xml（常为英文），没有 values-zh 等语言限定目录；规格要求与源应用逐屏对齐或写明“不擅自翻译”；资源转换 skill 带有“至少生成两套语言、默认英文则补 zh_CN”一类通用规则；设备可能使用中文系统语言。
  - 例外：规格或决策明确要求本轮新增本地化语言；此时按批准的译文来源生成，并在报告中注明源端没有该语言
- [复用基类的显示格式化 getter 前核对精度：品类精度不同（如 ETF 三位小数）时在子类覆写全部相关 getter，同一字段的各分支用同一精度](lesson-042445ba332611e04a80.lesson.md)
  - 时机：界面实现阶段，把源端十字光标、高亮联动等显示接入目标页面，决定复用基类 ViewModel 的格式化 getter 还是在子类覆写时；修改同一显示字段的任一分支（静态值、无数据兜底、高亮值）时
  - 情境：多个品类详情页共用一个基类 ViewModel，基类显示 getter 用通用精度格式化（如 formatPrice 保留两位）；某一品类的静态字段与源端联动代码使用不同精度（如 getPrice(..., 3)），子类尚未覆写对应 getter。
- [多行 maxLines + Ellipsis 两端末行截断粒度不同：规格写明差异，确需字符级一致时才用测量截断兜底](lesson-836a5414b52f0e062f1f.lesson.md)
  - 时机：规格提取阶段为带 maxLines(N) + TextOverflow.Ellipsis（或 android:ellipsize）的多行正文写转换决策，以及界面实现阶段落实折叠态末行时
  - 情境：源端多行正文以 maxLines + Ellipsis 折叠；目标用 .maxLines() + .textOverflow({ overflow: TextOverflow.Ellipsis })，默认 wordBreak 为 BREAK_WORD；映射参考只记 ellipsize → textOverflow 的 API 对应；项目可能要求完整复刻源端可观察行为。
  - 例外：项目允许平台差异、不要求逐字复刻末行时，直接使用内置行为，不引入运行期测量
- [源端在代码里格式化的含固定措辞文案（SimpleDateFormat、String.format、拼接）也建参数化字符串资源并用 $r 传参，不写模板字符串](lesson-d442eb6e9aab4d77db18.lesson.md)
  - 时机：界面转换阶段，为源端在代码里动态生成的可见文案（日历年月标题、带单位的数量等）选择文本来源并登记字符串资源时
  - 情境：Android 源在 Kotlin/Java 里用 SimpleDateFormat、String.format 或拼接生成带中文单位或固定措辞的显示文本（如 yyyy年M月），不在 strings.xml 中；目标工程约定可见文案走 $r('app.string.*')，模块 string.json 已有 %s 参数化条目。
  - 例外：文本只由纯数字或数据值构成（如日期格子的 day.toString()）
- [移植 Compose 文本组件时先确认 Text 收到的是原始字符串还是加工后的 AnnotatedString；链接识别、样式与点击要落到目标端](lesson-57a52be767730880cbba.lesson.md)
  - 时机：界面实现阶段，把源端 Compose Text 译成 ArkUI Text 时
  - 情境：源组件先调用工具函数（如按正则识别 URL、附加 LinkAnnotation 的 buildAnnotatedStringWithUrls）生成 AnnotatedString 再交给 Text；目标页面规格和验收条目只写了空值隐藏、折叠展开等布局行为。
- [说明类静态页按源布局逐卡迁移：文案逐字取自源 XML，标题条背景与插图一并迁入](lesson-0197307e63e8d848ba02.lesson.md)
  - 时机：界面实现阶段，依据源布局 XML 生成规则、说明、注意事项一类静态图文页时
  - 情境：源静态页由多张卡片组成，标题条使用 drawable 背景，正文是写在布局 XML 里的长文案，卡内或页首尾有插图；规格只要求“展示说明并可返回”，不复述内容。
