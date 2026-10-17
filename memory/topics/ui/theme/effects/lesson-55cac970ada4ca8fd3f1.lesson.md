# 源端图像模糊、乘法压暗与折叠态着色按参数等价实现

ID：`lesson-55cac970ada4ca8fd3f1` · 版本：2 · 阶段：execute · 主题：[ui/theme/effects](index.md)

概要：模糊、乘法压暗与折叠着色按源参数等价实现

信号：`LightingColorFilter`, `.blur(`

## 何时使用

界面实现阶段，迁移折叠头部等使用图片模糊、LightingColorFilter 压暗和按折叠状态切换工具栏图标颜色的页面时

## 适用情境

源背景图经模糊变换与 LightingColorFilter(mul, 0) 处理，工具栏图标由专门的着色管理类按折叠阈值切换颜色。

## 原因

以“无对等图片模糊链”为由只用半透明遮罩近似、用固定次要色代替状态着色，视觉明显偏离且不易被后续发现。

## 做法

1. 模糊用 blur；LightingColorFilter(mul, 0) 用 opacity = 1 − mul/255 的纯黑覆盖层表达乘法压暗。
2. 写前读取规格锚点中的状态着色实现类，移植折叠阈值与展开、折叠两态颜色。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [文字阴影用 textShadow，不用组件 shadow](lesson-2f1af636a29b131071b3.lesson.md)（共享 2 张卡）
- [Stack 子项 .align() 无效，对齐用满高容器](../../layout/constraints/lesson-92aee54a305ea0bde363.lesson.md)（共享 2 张卡）
- [内容定尺寸的父级里不写 100%，描边画在自身](../../layout/intrinsic/lesson-a58ebfe7a4c55b041b14.lesson.md)（共享 2 张卡）
- [纵向容器默认起始对齐与贴顶在目标显式写出](../../layout/constraints/lesson-08b9064f678f1635e647.lesson.md)（共享 1 张卡）
- [占位只登记输入缺值的情况，能实现的当场实现](../../../process/deferred-fulfillment/lesson-a2f6a4ae9a72be740de6.lesson.md)（共享 1 张卡）

来源支持：2 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-4f627840679361f165a3](../../../../../store/cases/case-4f627840679361f165a3/8b0f7cc40d821777a77dc3bf68c6739f335039023414e9bcb04404d5b4ac02e8.json) · 结论：rec-e0cac4f0cd
  卡片版本：`8b0f7cc40d821777a77dc3bf68c6739f335039023414e9bcb04404d5b4ac02e8`
- [case-9058ac868b6feb3a04e0](../../../../../store/cases/case-9058ac868b6feb3a04e0/d8e013afe2706da7f1b19c1a0d603c05f971b4ebc0c4542f6fb5e8a956b3ebc4.json) · 结论：rec-053d7777f5
  卡片版本：`d8e013afe2706da7f1b19c1a0d603c05f971b4ebc0c4542f6fb5e8a956b3ebc4`
