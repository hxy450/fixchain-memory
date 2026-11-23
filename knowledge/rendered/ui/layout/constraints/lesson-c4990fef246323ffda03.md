# 摘要行、价格行一类 Row 组：自定义组件不靠 Flex 基线对齐，内距逐行复制，靠右标签补文本对齐

## 何时使用

页面转换阶段，翻译源端为 Compose 的摘要行、价格行等由若干 Row 组成的列表块时

## 适用情境

源 Row 用 alignBy(LastBaseline) 对齐文本与自定义组件（如数量选择器）；各子 Row 各自 padding(horizontal)，分隔线在行外全宽；标签用 weight(1) + wrapContentWidth(End) 靠右。

## 例外与边界

- 第 1 步只管基线对齐的一端是自定义组件的情形；两端都是 Text 时，Flex 加 ItemAlign.Baseline 能按文本基线对齐，原有这样的写法保留，不改成居中近似。

## 原因

自定义组件没有可对齐的文本基线，来源改用 Flex 基线对齐后把它挤到了下一行；把各行 padding 上提到公共父容器会让分隔线跟着缩进；wrapContentWidth(End) 的靠右效果在权重布局里需要文本对齐补回。

## 做法

1. 单行文本与自定义控件对齐时，用 Row + alignItems(Center) + layoutWeight(1) 近似基线对齐（来源复核误差约 0.5dp），不直接用 Flex 的基线对齐。
2. 逐行复制 padding，不上提到外层；weight(1) + wrapContentWidth(End) 写成 layoutWeight 或 flexGrow 加 textAlign(End)。

## 可选检查

- 首次可构建时截图核对文本与控件的纵向位置。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 2 步〕Text 的 textAlign 没有设置时，段落水平对齐为 TextAlign.Start（Wearable 设备上为 TextAlign.Center）
- 〔做法第 2 步〕flexGrow 只在作为 Flex、Column、Row（及 DynamicLayout）的子组件时生效，按比例分父容器的剩余空间；父容器是 Column、Row 时要设主轴尺寸，未设时主轴自适应子组件，剩余空间分配可能达不到预期；设置它会触发二次布局
- 〔原因 / 做法第 1 步〕ItemAlign.Baseline 是 Flex 容器里沿交叉轴按文本基线对齐
