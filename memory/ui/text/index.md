# ui/text

文本展示与排版：源端对展示文本的加工（富文本、链接识别与点击）到 ArkUI Text/StyledString 的转换，Compose 行高到单行文本盒与多行行距的映射，多行末行省略的截断粒度，静态说明页的逐字文案与图文结构，Tab、页面标题、设置行等可见文案的逐字取值，以及字符串资源生成哪些语言限定目录

[上一级](../index.md)

## 本级经验

- [Tab 标签、页面标题与设置行等可见文案沿资源引用链取源端 strings 资源的逐字值，不用枚举名、路由名或自拟英文](lesson-31ab9f59945e5f0259ea.lesson.md)
  - 时机：界面实现阶段，为 Tab 标签、页面/路由标题、设置入口行等可见文案取值并写入页面与路由表时；以及派发侦察或规格任务、确定导航与标题字段的形态时
  - 情境：源端可见文案经资源键间接引用（导航目的地的 label、配置路由的标题资源、顶栏 title），常与目的地枚举名或功能名不同（如 Map 目的地显示“Mesh Map”、Messages 目的地的页面标题为“Conversations”）；目标以硬编码字符串或自建资源表承载；上游 brief 或页面规格已给出、或可从 strings.xml 解析出逐字值。
- [分开单行文本盒与多行行距，不把 Compose lineHeight 同名直映为 ArkUI .lineHeight](lesson-2a2924aaebbfbea80780.lesson.md)
  - 时机：规格提取、主题实现或页面转换阶段，把 Compose 排版令牌落成 ArkUI 文本属性或据文本高度推算容器尺寸时；视觉修复阶段改写主题层行高公式时
  - 情境：源 TextStyle 声明 fontSize/lineHeight、未设 lineHeightStyle；目标准备给所有 Text 无条件设置 .lineHeight()，或把 lineHeight 数值当单行文本的实际盒高来推算横向列表等容器的显式高度；映射参考可能给出 lineHeight → .lineHeight() 的 1:1 对应。
  - 例外：当前源端的 LineHeightStyle、字体内边距或已有明确契约要求固定行盒时，保留该契约，不默认改成自然高度。
- [只为源端实际存在的 values-&lt;语言&gt; 目录生成目标语言限定字符串；单语源不合成 zh_CN 等译文](lesson-b58df29f032cc6a8c9d6.lesson.md)
  - 时机：资源迁移阶段，决定目标工程生成哪些语言限定字符串目录（base、zh_CN 等）及各键取值时
  - 情境：Android 源只有默认 res/values/strings.xml（常为英文），没有 values-zh 等语言限定目录；规格要求与源应用逐屏对齐或写明“不擅自翻译”；资源转换 skill 带有“至少生成两套语言、默认英文则补 zh_CN”一类通用规则；设备可能使用中文系统语言。
  - 例外：规格或决策明确要求本轮新增本地化语言；此时按批准的译文来源生成，并在报告中注明源端没有该语言
- [多行 maxLines + Ellipsis 两端末行截断粒度不同：规格写明差异，确需字符级一致时才用测量截断兜底](lesson-836a5414b52f0e062f1f.lesson.md)
  - 时机：规格提取阶段为带 maxLines(N) + TextOverflow.Ellipsis（或 android:ellipsize）的多行正文写转换决策，以及界面实现阶段落实折叠态末行时
  - 情境：源端多行正文以 maxLines + Ellipsis 折叠；目标用 .maxLines() + .textOverflow({ overflow: TextOverflow.Ellipsis })，默认 wordBreak 为 BREAK_WORD；映射参考只记 ellipsize → textOverflow 的 API 对应；项目可能要求完整复刻源端可观察行为。
  - 例外：项目允许平台差异、不要求逐字复刻末行时，直接使用内置行为，不引入运行期测量
- [移植 Compose 文本组件时先确认 Text 收到的是原始字符串还是加工后的 AnnotatedString；链接识别、样式与点击要落到目标端](lesson-57a52be767730880cbba.lesson.md)
  - 时机：界面实现阶段，把源端 Compose Text 译成 ArkUI Text 时
  - 情境：源组件先调用工具函数（如按正则识别 URL、附加 LinkAnnotation 的 buildAnnotatedStringWithUrls）生成 AnnotatedString 再交给 Text；目标页面规格和验收条目只写了空值隐藏、折叠展开等布局行为。
- [说明类静态页按源布局逐卡迁移：文案逐字取自源 XML，标题条背景与插图一并迁入](lesson-0197307e63e8d848ba02.lesson.md)
  - 时机：界面实现阶段，依据源布局 XML 生成规则、说明、注意事项一类静态图文页时
  - 情境：源静态页由多张卡片组成，标题条使用 drawable 背景，正文是写在布局 XML 里的长文案，卡内或页首尾有插图；规格只要求“展示说明并可返回”，不复述内容。
