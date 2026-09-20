# 改主题层文本度量公式时把「已核」和「假设」分开，先在同轮 dump 里找多行回归基线

ID：`lesson-0e10b578fa6f2cb0a75e` · 版本：1

[本主题](index.md)

## 何时使用

视觉对齐修复阶段，把 Compose TextStyle 的 lineHeight 语义改写成 ArkUI Text 属性（lineHeight / lineSpacing）并确定折算公式、且不允许当场重编实测时

## 适用情境

源样式带 lineHeight；目标用同一主题令牌同时服务单行与多行段落；单行盒高已有 Android dump 与字体度量支撑，多行行距如何由 fontSize / 自然行盒 / lineSpacing 合成 SDK d.ts 无说明、当前 dump 无 lineSpacing 样本。

## 原因

round-0 fixer 把 .lineHeight 换成 lineSpacing(lineHeight − naturalHeight, onlyBetweenLines) 并在文件头写成既定事实，§6 假设「多行 = natural + spacing」却未回看 SnackDetail dump 里已正确的 5 行 140vp 基线；实测 ArkUI 多行行距 = fontSize + lineSpacing（16 + 9.3 ≈ 25.4vp），单行修好、多行变小，属修复中新生偏差。该合成规则只由 round-3 三页 dump（Karla/Montserrat 16fp）反推，无官方文档佐证。

## 做法

1. 单行自然高有 Android dump + ttf 度量支撑可以直接写；多行合成规则若 SDK 未写、dump 无样本，在代码注释和 §6 明确标为未验证假设并给出下轮必测数值（如 5 行块 ≈131vp、行距 28vp）。
2. 替换一条已有正确表现的渲染路径前，先在同轮 dump 里找出它的多行样本记为回归基线；改完至少用 measureTextSize 或下轮 dump 同时核单行盒与多行块高，两者只对一个不算修完。
3. 不允许重编实测时优先选不改变已正确行为的方案（只对单行关 lineHeight、或运行期 MeasureUtils 实测后再算 spacing），不把两个未知量都靠猜。

## 检查

- 修复 §6 里每条数值预测在下一轮 dump 有核销；单行 dump 高 = 自然高且多行块高 = N × lineHeight 同时成立。

## 来源（按需复核）

经验是有适用范围的历史建议。核查来源时同时看结论与 unknown；来源卡未随阅读包复制。

- [case-04c6d6166ebb2bcc3dfa](../../../store/cases/case-04c6d6166ebb2bcc3dfa/08cc614b7fd6dff41319ea673aceed9490eb8275b4fefb40e2711fb1fa952fdd.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`08cc614b7fd6dff41319ea673aceed9490eb8275b4fefb40e2711fb1fa952fdd`
