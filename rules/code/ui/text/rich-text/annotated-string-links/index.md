# 带 LinkAnnotation 链接的 AnnotatedString 文本

agent 会看到什么：读到 Compose 文本或输入框经 buildAnnotatedString、LinkAnnotation、visualTransformation 给 URL 加链接；交回的是直接显示原始字符串的 Text 或纯文本 TextArea，链接不着色也不可点

## 规矩

- rule-028c4b7e0f63｜源端 Text 的文本带 LinkAnnotation 时，目标用 StyledString 加 UrlStyle｜读到：Compose 组件把原始字符串先交给 buildAnnotatedStringWithUrls 这类工具函数，得到带 LinkAnnotation 的 AnnotatedString，再 Text(text = …) 显示；写错：目标写成 Text(this.text) 这类直接显示原始字符串的 Text，链接不着色也不可点
- rule-bbf5a85be411｜Compose 正文带 LinkAnnotation 链接时，目标用 Span 分段、加链接样式并能点开｜读到：源 Compose 正文先转成带 `LinkAnnotation` 的 AnnotatedString（按 URL 链接化的辅助函数）再交给 Text；写错：目标是纯 `Text(<字符串>)`：没有 Span 分段，链接没有颜色和下划线，点了不跳转
- rule-9da71fc0157c｜源输入框用 visualTransformation 高亮链接时，目标用 RichEditor 加 span 样式｜读到：`OutlinedTextField(visualTransformation = { TransformedText(…AnnotatedString…, OffsetMapping.Identity) })`，按 URL 加链接色；写错：目标描述框是纯文本 `TextArea`，编辑态没有链接高亮，登记了 UNC 一类的不确定占位
- rule-76bf1e6c6014｜源码里有、验收项没写的可见行为照源码实现；做不了就登记占位、报告写明降级｜读到：源码对展示内容有可见加工（如 buildAnnotatedStringWithUrls 生成链接），而功能验收项只写了空值隐藏、折叠展开这类布局行为；写错：代码只落实验收项、把源码行为删掉，结构化报告的 `low_confidence_uncertain_regions` 为空，也没有登记占位
