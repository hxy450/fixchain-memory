# ui/text

文本展示：源端对展示文本的加工（富文本、链接识别与点击）到 ArkUI Text/StyledString 的转换

[上一级](../index.md)

## 本级经验

- [移植 Compose 文本组件时先确认 Text 收到的是原始字符串还是加工后的 AnnotatedString；链接识别、样式与点击要落到目标端](lesson-57a52be767730880cbba.lesson.md)
  - 时机：界面实现阶段，把源端 Compose Text 译成 ArkUI Text 时
  - 情境：源组件先调用工具函数（如按正则识别 URL、附加 LinkAnnotation 的 buildAnnotatedStringWithUrls）生成 AnnotatedString 再交给 Text；目标页面规格和验收条目只写了空值隐藏、折叠展开等布局行为。
