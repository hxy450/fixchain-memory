# Compose Brush 渐变描边用“外层渐变 + 边宽内衬 + 内层实底”实现，不降级成渐变首色

ID：`lesson-5d56afe5595bb26eaf2f` · 版本：1

[本主题](index.md)

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

## 来源（按需复核）

- [case-40c445e1fb0a99ce0a72](../../../store/cases/case-40c445e1fb0a99ce0a72/2243b17f2f740e65ee1727d642a6aca74ef48f8bc924a7f9ccdcf12c9198d74b.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:4
  卡片版本：`2243b17f2f740e65ee1727d642a6aca74ef48f8bc924a7f9ccdcf12c9198d74b`
- [case-583c797930b89c0d4e63](../../../store/cases/case-583c797930b89c0d4e63/f5953e9f12a3bcae8f4a8ae23194b2301733b2226bbed362e363b07da33b903c.json) · 结论：recommendation:2
  卡片版本：`f5953e9f12a3bcae8f4a8ae23194b2301733b2226bbed362e363b07da33b903c`
