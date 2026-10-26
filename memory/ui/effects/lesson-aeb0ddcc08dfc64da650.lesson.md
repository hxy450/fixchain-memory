# linearGradient 的 angle 按 CSS 语义（0 向上、90 左→右）；渐隐到透明的终点取底色同色 alpha 0，不写 transparent

ID：`lesson-aeb0ddcc08dfc64da650` · 版本：2

[本主题](index.md)

## 何时使用

界面实现与共享组件实现阶段，用 ArkUI linearGradient 写滚动边缘渐隐遮罩条或其他轴向渐变，确定渐变方向（angle/direction）与终点色时

## 适用情境

源端用 fadingEdges 一类修饰让横滑行或纵向滚动区的内容在边缘淡出，或有其他轴向渐变；目标改用叠在内容上、从容器底色渐变到透明的 linearGradient 遮罩条，按左右或上下边分别放置，底色常是运行期解析出的 '#AARRGGBB' 主题色。

## 原因

ArkUI linearGradient 的 angle 与 CSS 同义（0 指向上方、顺时针为正），按数学坐标或 Android GradientDrawable（0 = 向右）记忆取值，会把横向渐隐写成竖向、横纵整组互换；本机 .d.ts 对 angle 只写缺省值 180，不足以判断方向。'transparent' 与 Color.Transparent 是透明黑 #00000000，渐变按非预乘色插值，与有色底色之间的中段会变成半透明灰带（HarmonyOS 6.1.0 设备截图对照）。

## 做法

1. 轴向渐变优先用 direction: GradientDirection.Right/Left/Bottom/Top；写 angle 时取 90（左→右）、270（右→左）、180（上→下，缺省）、0（下→上），不按 0 = 向右换算。
2. 底色 → 透明的遮罩，终点色取起点色同 RGB、alpha 0（'#AARRGGBB' → '#00RRGGBB'）；起点色是 Resource 或主题令牌时先解析成具体色值再派生透明版，主题切换时一起重算。

## 可选检查

- 生成期不能上机时，逐条列出每个渐变的所在边、angle/direction、colors[0] 落在哪条边、终点是否同色透明，横向与纵向遮罩分别核对。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-9190f97a15e03668b874](../../../store/cases/case-9190f97a15e03668b874/db9056c5bb23244d6f71a8746bb23d341f491960adbf442d2838297fad076b1e.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`db9056c5bb23244d6f71a8746bb23d341f491960adbf442d2838297fad076b1e`
