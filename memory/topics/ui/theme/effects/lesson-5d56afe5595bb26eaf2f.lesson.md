# Compose Brush 渐变描边用“外层渐变 + 边宽内衬 + 内层实底”实现，不降级成渐变首色

ID：`lesson-5d56afe5595bb26eaf2f` · 版本：4 · 阶段：execute · 主题：[ui/theme/effects](index.md)

概要：Brush 渐变描边用外层渐变加内衬实底实现

信号：`Modifier.border`, `Brush.linearGradient`, `Surface`, `linearGradient`, `borderRadius`

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

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [blendMode 着色把底色字形渐变放同一离屏组](lesson-3024193e4816229c5370.lesson.md)（共享 1 张卡）
- [渐变端点几何换算成 linearGradient 角度与色标](lesson-4ce3a1c186651285f362.lesson.md)（共享 1 张卡）
- [派工必读清单覆盖语义来源，提速要求下也保留](../../../process/handoff-loss/lesson-8598e0af342dd5c8ba28.lesson.md)（共享 1 张卡）
- [占位只登记输入缺值的情况，能实现的当场实现](../../../process/deferred-fulfillment/lesson-a2f6a4ae9a72be740de6.lesson.md)（共享 1 张卡）
- [Material 按钮区分布局占位、背景实绘与触控范围](../../layout/intrinsic/lesson-b73a1ac8908f74856a02.lesson.md)（共享 1 张卡）

来源支持：2 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-40c445e1fb0a99ce0a72](../../../../../store/cases/case-40c445e1fb0a99ce0a72/2243b17f2f740e65ee1727d642a6aca74ef48f8bc924a7f9ccdcf12c9198d74b.json) · 结论：diagnosis, rec-5c45b76497, rec-d37c2068b9, rec-c5ad41cfe1
  卡片版本：`2243b17f2f740e65ee1727d642a6aca74ef48f8bc924a7f9ccdcf12c9198d74b`
- [case-583c797930b89c0d4e63](../../../../../store/cases/case-583c797930b89c0d4e63/f5953e9f12a3bcae8f4a8ae23194b2301733b2226bbed362e363b07da33b903c.json) · 结论：rec-1a1a46df3c
  卡片版本：`f5953e9f12a3bcae8f4a8ae23194b2301733b2226bbed362e363b07da33b903c`
