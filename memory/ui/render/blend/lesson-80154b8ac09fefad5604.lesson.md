# Compose 依赖画布已有内容的 blendMode 叠色，不能映射成 ArkUI 独立兄弟节点的离屏混合

ID：`lesson-80154b8ac09fefad5604` · 版本：1

[本主题](index.md)

## 何时使用

规格提取阶段，为 Compose drawWithContent/drawRect(brush, blendMode) 这类依赖画布上已画内容的绘制修饰符确定 ArkUI 渲染映射、并决定是否定为 HARD 决策时

## 适用情境

源码用 Modifier.drawWithContent { drawContent(); drawRect(Brush.linearGradient(colors), blendMode = Plus/Darken) } 给图标着色，效果依赖同一画布上已画好的底盘与字形（白底加法饱和仍白，只有深色字形像素变成渐变色）；目标侧渐变层、图标、底盘是 Stack 中并列的兄弟节点，准备用 .blendMode(mode, BlendApplyType.OFFSCREEN)。

## 例外与边界

- 源端 blendMode 的结果不依赖画布已有内容（如只对自身 alpha 起作用的 SRC_IN/DST_IN）

## 原因

ArkUI 单节点 .blendMode(…, OFFSCREEN) 的混合目标是该节点自身的透明离屏层，不含兄弟节点已画内容：PLUS 于透明底等于源本身，结果是一块淡色方块盖住白盘与圆环。F002 spec 作者读到了 Gradient.kt 的公式与源码注释「should use a layer + srcIn」，仍把独立兄弟节点的 PLUS/DARKEN 定为 HARD、把 SRC_IN 蒙版法降为「真机偏色则退回」，而生成期禁编译、无真机，回退不可能触发。

## 做法

1. 先判断混合结果是否依赖画布上已画好的兄弟内容（白底 + PLUS 饱和为白、深底 + DARKEN 取 min 都依赖底色）；是则把参与混合的节点（字形与渐变，必要时含底盘）放进同一个 .blendMode(SRC_OVER, OFFSCREEN) 离屏组，组内用只依赖源/目标 alpha 的 SRC_IN/DST_IN 取形。
2. SDK 文档只给「与其下方画布已有内容混合」这类未定义范围的措辞、skill 参考 grep 为空时，不定 HARD：标为待真机核验项并写明核验方法；若已想到不依赖画布状态的等价方案（SRC_IN 蒙版），把它设为主方案，依赖画布状态的方案设为回退。
3. 源码原作者的实现提示（如 `// This should use a layer + srcIn`）是目标结构的直接线索，映射决策要引用并给出采纳或不采纳的理由。

## 检查

- 实现落地后对一枚带渐变着色的图标截图：字形以外的像素应与底盘一致，不得出现覆盖圆环的半透明色块。
- spec 里每条 blendMode 映射都能回答「混合目标包含哪些已画内容」；答不出来的不得标 HARD。

## 来源（按需复核）

经验是有适用范围的历史建议。核查来源时同时看结论与 unknown；来源卡未随阅读包复制。

- [case-0e3ff99e6b2aa8afcfff](../../../../store/cases/case-0e3ff99e6b2aa8afcfff/08bee2db10230570995be1ac03f4f0a07ebf80600f0c6bf1ce80029468144a01.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`08bee2db10230570995be1ac03f4f0a07ebf80600f0c6bf1ce80029468144a01`
