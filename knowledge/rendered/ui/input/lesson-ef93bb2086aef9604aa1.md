# 源端同一控件既可编辑又分段着色（EditText + Spannable、Compose TextField 的 visualTransformation）时用 RichEditor 承载，不拆成只读着色与单色编辑两态，也不降级成纯文本；整体重建与焦点恢复照源实现

## 何时使用

规格提取与界面实现阶段，为源端常驻可编辑、带分段着色的输入框（EditText + Spannable 与输入过滤，或带 visualTransformation 的 Compose TextField，如十六进制数据编辑器、编辑态 URL 高亮的描述框）选择 ArkUI 编辑组件并迁移刷新语义时

## 适用情境

源端每个数据单元是常驻可编辑的 EditText：文本以 setText(text, SPANNABLE) 分段着色、挂 InputFilter.AllCaps、宽度 wrap_content，着色刷新靠删除重建整个编辑器并按序号恢复焦点；规格可能写“TextArea + 分段 Span 着色”这类不可实现的组合；材料与映射参考里没有提到 RichEditor。也包括 Compose TextField/OutlinedTextField 以 visualTransformation（如按正则给 URL 着色的 buildAnnotatedStringWithUrls）在编辑态显示样式，规格写成“输入框内富文本高亮能力受限，编辑态降级为纯文本”。

## 原因

TextArea 不承载 Span，组件选择与着色要求自相矛盾；改成“着色只读 Text ↔ 点击切换单色 TextArea”的双态，会丢掉常驻着色、插入色、按内容测宽与整体重建等行为，注释却称等价。来源中规格作者与转换器都读全了源码，转换器也意识到 TextArea 不支持 Span，仍选了双态，后续切片沿用。

## 做法

1. 映射到能同时编辑与承载样式片段的组件：RichEditor 配控制器按段 addTextSpan，内容变化后按源端规则重设各段样式（如 URL 段着色）；写入前核对所选组件是否支持子 Span 或样式，不写“TextArea + Span”，也不在核对 RichEditor 之前把编辑态着色判为平台受限。
2. 实现阶段发现规格组件满足不了源行为时，先查同平台的可编辑富文本组件，不自行拆成双态；确需降级时在规格与占位登记中列出丢失的行为，不在注释中声称等价。
3. 迁移“删除并重建整个编辑器再恢复焦点”的逻辑时保留重建语义（错误单元随数据消失、按子项序号恢复焦点），不以原地刷新代替。

来源支持：2 张卡 · 2 次迁移 · 2 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔适用情境 / 原因〕TextArea 没有子组件，不能承载 Span
- 〔做法第 1 步〕RichEditor 是支持图文混排和文本交互式编辑的组件，可编辑的同时给各段文本设样式
- 〔适用情境 / 做法第 1 步〕RichEditor 给文本段设样式后，编辑态里 URL 段能常驻显示链接色
- 〔做法第 3 步〕ForEach 的键值变化时，框架把该元素视为已被替换，基于新键值创建新组件；没定义 keyGenerator 时默认键值由 index 和 JSON.stringify(item) 拼成
