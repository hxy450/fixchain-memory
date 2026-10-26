# 颜色插值或混合按 ARGB 四通道拆分并输出同一格式：#AARRGGBB 串与 getColorSync 数值不按 #RRGGBB 偏移取子串

ID：`lesson-b742fb724345e4cfeb50` · 版本：1

[本主题](index.md)

## 何时使用

界面实现阶段，对主题色等颜色值做插值、混合或其他按通道的运算（折叠顶栏背景、状态色过渡、按压混色）时

## 适用情境

目标代码先把颜色取成 '#AARRGGBB' 字符串或 32 位 ARGB 数值（resourceManager.getColorSync 的结果、8 位 color.json 值），再在两个颜色之间按比例插值或混合；写者自写分量运算，工程里可能已有或稍后才有 ARGB 混色工具。

## 原因

8 位颜色串前两位是 alpha；按 #RRGGBB 的 slice(1,3)/(3,5)/(5,7) 取通道，会把 alpha 当成红色，再拼回 6 位串就丢掉 alpha，颜色整体错位。

## 做法

1. 先确认两个端点的实际表示（getColorSync 返回 32 位 ARGB 数值；8 位串是 #AARRGGBB），按 A/R/G/B 四个通道用位移拆分（>>> 24/16/8/0 再 & 0xFF），逐通道插值后输出与端点同一种 8 位表示。
2. 颜色的产出与解析共用一种格式约定：工程已有 ARGB 混色工具就直接复用；还没有时写成单个共享工具，并在注释写明输入输出格式，不在页面里各自手写拆分。

## 可选检查

- 对插值函数有疑问时，把 fraction=0 与 1 代入，结果应原样等于两个端点；位数变了或首两位变成 alpha 值即为通道错位。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-6577b14c75288c37fce7](../../../store/cases/case-6577b14c75288c37fce7/8f2ffa41460a00ac84fcaa4273c2932602ad1ae914e85b0010b5b4a7a4a07ca7.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`8f2ffa41460a00ac84fcaa4273c2932602ad1ae914e85b0010b5b4a7a4a07ca7`
