# 同时需要圆角与描边时把 radius 写进 .border()

## 何时使用

界面实现阶段，为同一视图设置圆角与描边（按钮 cornerRadius 加 stroke、OutlinedBox、GradientDrawable setStroke）时

## 适用情境

目标写成 .borderRadius(X) 后接不带 radius 的 .border({ width, color })；映射参考可能把圆角与描边分列成两个属性。

## 原因

后续不带 radius 的 .border() 会把先前的 borderRadius 重置为直角。

## 做法

1. 写成 .border({ width, color, radius: X })，或保证 .borderRadius() 位于 .border() 之后。

## 可选检查

- 沿用旧写法的文件较多时，检索“.borderRadius( 之后紧跟不含 radius 的 .border({”组合

来源支持：2 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1 步〕border 的边框宽度默认 0、圆角半径默认 0、颜色默认 Color.Black；border 里缺省 color、radius 时，要让 borderColor、borderRadius 生效必须把它们设在 border 之后
- 〔原因〕先 borderRadius(20) 再写不带 radius 的 border() 时，设备上圆角被重置为直角
