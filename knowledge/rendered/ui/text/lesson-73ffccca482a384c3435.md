# 可能为空的 wrap_content TextView 仍占一行高：ArkUI 空串 Text 高为 0，空态用零宽空格或行高兜底并保留节点

## 何时使用

界面实现阶段，源端对应的是 wrap_content 的 TextView、空态时为 VISIBLE 或 INVISIBLE（不是 GONE），为这类文本可能为空的 Text 节点（列表卡片标题、正文预览、附件文字条）确定渲染条件与行高时

## 适用情境

源布局里 wrap_content 的 TextView 可能拿到空串（无标题、空正文、名称缺失），XML 或 Adapter 把它置为 VISIBLE 或 INVISIBLE 而不是 GONE；相邻元素（日期行、正文起始行、文字条底色）依赖它的一行字体高度定位；目标用 ArkUI Text 渲染。

## 例外与边界

- 源端在文本为空时把该 TextView 设为 GONE：按不渲染处理

## 原因

Android 空文本 TextView 仍按字体度量占一行高，INVISIBLE 也保留这块空间；ArkUI Text 内容为空时高度为 0，Visibility.Hidden 只保留组件自身那份（为零的）尺寸。按 if (text !== '') 条件渲染，或只换成 Hidden，都会让相邻元素上移、文字条塌陷。

## 做法

1. 按源端显隐语义选写法：VISIBLE 与 INVISIBLE 都保留节点（INVISIBLE 用 .visibility(Visibility.Hidden)），只有 GONE 才条件不渲染；共享组件的显隐以 Adapter bind/getView 中的 setVisibility 分支为准，不以 XML 初值或文本是否为空判断。
2. 空串可能到达的 Text，显示值为空时换成零宽空格 '\u200B' 或单个空格，或按源字体行高给 lineHeight、constraintSize({ minHeight })，保证空态仍占一行；再核对依赖它定位的相邻元素。

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1 步〕安卓 View.INVISIBLE 不可见但仍占布局空间，View.GONE 不可见且不占布局空间
- 〔原因 / 做法第 1 步〕ArkUI Visibility.Hidden 隐藏但参与布局占位，Visibility.None 隐藏且不参与布局、不占位
- 〔原因〕设备上：安卓 wrap_content 的 TextView 文本为空时仍按一行字体高度占高；ArkUI 内容为空字符串的 Text 高度为 0，设成 Visibility.Hidden 的空 Text 高度也是 0
- 〔做法第 2 步〕Text 的 lineHeight 传 number 时单位是 fp；设置值不大于 0 时不限制行高，由系统按字号自适应
