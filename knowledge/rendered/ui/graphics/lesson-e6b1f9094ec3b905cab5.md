# AnimatedImageVector/animated-vector 按 atEnd 在起止帧之间实现形变过渡；同名静态 SVG 只是起始帧，两态静态帧或符号切换只在已批准降级时使用

## 何时使用

规格提取与界面实现阶段，为 AnimatedImageVector/animated-vector 图标确定实现方案、各状态显示的帧与状态切换时的过渡时；以及资源迁移阶段遇到 animated-vector 时

## 适用情境

源码用 AnimatedImageVector.animatedVectorResource 与 rememberAnimatedVectorPainter(icon, atEnd)，atEnd 由完成、运行等状态决定，animated-vector 的 objectAnimator 以 pathData 的 valueFrom/valueTo、duration 与 interpolator 描述两态形变；目标没有直接等价组件，资源目录里的同名媒体是资源迁移从起始帧导出的静态 SVG；规格可能允许资源动画或等价符号，或写“图标态切换即可满足”。

## 例外与边界

- 决策记录以编号批准省略形变过渡、差异验收与之一致时，按批准的两态静态帧或等价符号实现，仍按状态分别给出起止帧

## 原因

直接引用同名静态图，所有状态都显示起始帧，例如完成的步骤仍显示播放三角。来源中资源阶段按规则应把 animated-vector 记为不可映射，却导出起始帧且没在映射表标注；转换者读过 XML 的 valueTo，仍只写起始帧并挂成待补资源。两态静态帧或符号切换只修正了状态对应的帧，两态之间的形变过渡仍然丢失；规格以“无直接等价、图标态切换即可”定案时，下游会把未实现的形变当作已覆盖。

## 做法

1. 规格阶段读 painter 的 atEnd 由哪个状态决定，再打开对应 *_anim.xml，取 pathData 的 valueFrom/valueTo、duration 与 interpolator，把两态之间的形变写成保真要求并给出实现路线，不以“无直接等价、图标态切换即可”作转换决策。
2. 实现 atEnd 语义：false 画首帧、true 画末帧；状态变化时按源 duration 与插值器（fast_out_slow_in 对应 Curve.FastOutSlowIn，即 cubic-bezier(0.4, 0, 0.2, 1)）在两组 pathData 的同序数值之间插值，在 Canvas 等可按进度重绘路径的载体中按源 viewport 缩放绘制；反向切换从当前帧回放。AVD 的 pathData 形变本身要求起止路径命令结构一致，可逐数值插值。
3. 只有批准的降级才用两态静态帧、语义相符的系统 SymbolGlyph（名称以本地 SDK 的 sysResource 为准）或独立终点图形，并按状态分别给出两帧；同名媒体已存在时打开核对它画的是哪一帧。
4. 资源迁移阶段为保证引用可解析导出起始帧静态 SVG 时，在资源映射表同一行写明“仅起始帧，动画与终点帧已丢弃”。

来源支持：2 张卡 · 2 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-37.0 的平台资源；android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔适用情境 / 做法第 1 步〕objectAnimator 的 valueFrom、valueTo 是动画的起止值；valueType="pathType" 表示这两个值是路径字符串，用于 AnimatedVectorDrawable 的路径形变
- 〔原因 / 做法第 4 步〕AnimatedVectorDrawable 的 android:drawable 指向的是静态 vector drawable，形变动画由 target 引用的 animator 另外描述，静态 vector 本身不含终点帧
- 〔做法第 2 步〕安卓解析 pathData 动画时用 PathParser.canMorph 检查 valueFrom、valueTo 两条路径能否形变，不能时抛 InflateException（Can't morph from … to …）；能形变的两条路径由 PathDataEvaluator 按动画进度逐点插值
- 〔做法第 2 步〕安卓 @android:interpolator/fast_out_slow_in 是 pathInterpolator，控制点为 controlX1=0.4、controlY1=0、controlX2=0.2、controlY2=1
- 〔做法第 2 步〕ArkUI 的 Curve.FastOutSlowIn 就是 cubic-bezier(0.4, 0.0, 0.2, 1.0)；curves.cubicBezierCurve 的 x1、x2 取值 [0, 1]，返回的 ICurve.interpolate(fraction) 输入取值 [0, 1] 的归一化时间，返回插值后的进度
- 〔做法第 2 步〕Canvas 的 Path2D(d) 按符合 SVG 路径描述规范的字符串建路径，插值得到的 pathData 字符串可以直接构造（API 12 起另有带 LengthMetricsUnit 的重载）
