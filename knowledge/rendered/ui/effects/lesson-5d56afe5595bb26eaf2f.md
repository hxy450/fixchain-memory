# Compose Brush 渐变描边用“外层渐变 + 边宽内衬 + 内层实底”实现，不降级成渐变首色

## 何时使用

界面实现阶段，把 Compose border(width, Brush) 或项目自定义的渐变描边 Modifier 翻成 ArkUI 组件时

## 适用情境

源组件用 Brush.linearGradient 描边（自定义渐变描边扩展等），边宽来自扩展的默认参数，外面可能套 elevation > 0 的 Surface；ArkUI border 只接受单色。

## 原因

ArkUI border 不支持渐变，但描边环可以用外层 linearGradient、边宽 padding 和内层实底拼出；降级成渐变首色会丢掉渐变。双层结构的内层底色若漏挂，渐变会铺满整块组件；边宽和绘制顺序写在扩展定义里，没读定义就会凭猜测写错。

## 做法

1. 外层容器写 linearGradient、padding(边宽) 和圆角，内层写实底与相应圆角；边宽和绘制顺序先读 Modifier 扩展定义取默认参数，文本内距相应减去边宽以保持总尺寸。
2. 逐一确认未选中、选中、按压各状态下内层都遮住环内侧，组件内定义的颜色函数都有调用点。
3. 外层 Surface 按 elevation 叠加底色时，内层底色按同样的规则逐状态计算，不只核一种状态。

来源支持：2 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 1 步〕LinearGradientOptions 没写 angle 时为 180、没写 direction 时为 GradientDirection.Bottom（自上而下）、没写 repeating 时为 false
- 〔做法第 1 步〕angle 不是 undefined 时 direction 不生效；colors 每项的位置取值 [0, 1.0]，小于 0 按 0、大于 1.0 按 1.0，位置比前一项小时按等于前一项处理
