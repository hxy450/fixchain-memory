# ui/text

文本展示：源端对展示文本的加工（富文本、链接识别与点击）到 ArkUI Text/StyledString 的转换，静态说明页的逐字文案与图文结构，以及 Tab、页面标题、设置行等可见文案的逐字取值

[上一级](../index.md)

## 本级经验

- [Tab 标签、页面标题与设置行等可见文案沿资源引用链取源端 strings 资源的逐字值，不用枚举名、路由名或自拟英文](lesson-31ab9f59945e5f0259ea.lesson.md)
  - 时机：界面实现阶段，为 Tab 标签、页面/路由标题、设置入口行等可见文案取值并写入页面与路由表时；以及派发侦察或规格任务、确定导航与标题字段的形态时
  - 情境：源端可见文案经资源键间接引用（导航目的地的 label、配置路由的标题资源、顶栏 title），常与目的地枚举名或功能名不同（如 Map 目的地显示“Mesh Map”、Messages 目的地的页面标题为“Conversations”）；目标以硬编码字符串或自建资源表承载；上游 brief 或页面规格已给出、或可从 strings.xml 解析出逐字值。
- [移植 Compose 文本组件时先确认 Text 收到的是原始字符串还是加工后的 AnnotatedString；链接识别、样式与点击要落到目标端](lesson-57a52be767730880cbba.lesson.md)
  - 时机：界面实现阶段，把源端 Compose Text 译成 ArkUI Text 时
  - 情境：源组件先调用工具函数（如按正则识别 URL、附加 LinkAnnotation 的 buildAnnotatedStringWithUrls）生成 AnnotatedString 再交给 Text；目标页面规格和验收条目只写了空值隐藏、折叠展开等布局行为。
- [说明类静态页按源布局逐卡迁移：文案逐字取自源 XML，标题条背景与插图一并迁入](lesson-0197307e63e8d848ba02.lesson.md)
  - 时机：界面实现阶段，依据源布局 XML 生成规则、说明、注意事项一类静态图文页时
  - 情境：源静态页由多张卡片组成，标题条使用 drawable 背景，正文是写在布局 XML 里的长文案，卡内或页首尾有插图；规格只要求“展示说明并可返回”，不复述内容。
