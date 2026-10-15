# 按钮行里有 match_parent 高的竖分隔 View 时，先给按钮行定高再让分隔线撑满，不让未定高行里的 Stretch 子项决定卡片高度

ID：`lesson-2a07020daf9a7d8a60a3` · 版本：3

[本主题](index.md)

## 何时使用

界面实现阶段，转换弹窗或卡片里的按钮行（按钮之间有 layout_height=match_parent 的竖分隔 View），确定行高与卡片高度约束时

## 适用情境

源布局卡片为 wrap_content 高，按钮行由 wrap_content 按钮加 padding 构成，按钮之间的竖分隔 View 为 match_parent 高；目标准备给分隔线 alignSelf(ItemAlign.Stretch)，而按钮行本身不设高度，卡片放在覆盖整窗的遮罩容器里。也包括按钮由 AlertDialog.Builder 的 setPositive/Negative/NeutralButton 生成、源布局里没有按钮行，按钮条外观来自主题的平台对话框样式。

## 例外与边界

- 行位于 Scroll 等纵向无界容器内、子项要随最高兄弟等高时不按本条（本条针对上层有确定高度的弹窗卡片），按 lesson-cb1a12afca61db08ed9a 处理

## 原因

按钮行不定高时，Stretch 的分隔线会取到更外层的确定尺寸，把按钮行和卡片撑到父容器全高；源端 match_parent 的分隔线只随按钮行的内容高度。

## 做法

1. 先给分隔线所在的 Row 确定高度：应用布局里的按钮取源按钮实测高度，或由按钮 padding 与字号行框计算；再让分隔线 Stretch 或取 100%。
2. 按钮条由平台 AlertDialog 生成时，行高与分隔线按源主题的平台对话框样式求和：SDK platforms/android-<api>/data/res/layout/alert_dialog_<主题>.xml 中 buttonPanel 的按钮 minHeight（@dimen/alert_dialog_button_bar_height）、dividerHorizontal 与 buttonBarStyle 内边距，不默认按 48vp 写；平台对话框的完整外观契约见 lesson-9c4de55af3c1ecd8eaa4。

## 可选检查

- 写完用真机 dump 核对卡片高度接近源端实测，而不是父容器高度。

来源支持：2 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-bf55dc1aedfb0f2a965e](../../../store/cases/case-bf55dc1aedfb0f2a965e/bcb7663fe953c49cc6b18f293ae448fe649838e3a6f0e8e0e2d31020c4836d2d.json) · 结论：diagnosis, recommendation:2, recommendation:3
  卡片版本：`bcb7663fe953c49cc6b18f293ae448fe649838e3a6f0e8e0e2d31020c4836d2d`
- [case-ed0c3a60e7342aa867b4](../../../store/cases/case-ed0c3a60e7342aa867b4/72a121533a777b3f391b3c19ced6417310c07f19590b2c0971726410e40c7715.json) · 结论：recommendation:5
  卡片版本：`72a121533a777b3f391b3c19ced6417310c07f19590b2c0971726410e40c7715`
