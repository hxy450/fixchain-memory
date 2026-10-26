# 两层共享转场（sharedBounds 包 sharedElement）每端只在外层挂一个 geometryTransition，不嵌套两对

ID：`lesson-3cd65cd70fb4a5ccc3d5` · 版本：2

[本主题](index.md)

## 何时使用

界面实现阶段，把 Compose 共享元素转场落为 ArkUI geometryTransition、确定每端挂几个配对键和挂在哪个节点时；规格提取阶段写共享转场契约时

## 适用情境

源端在 SharedTransitionLayout 内用 sharedBounds(键 A) 包住带 sharedElement(键 B) 的内容，两层键不同，列表卡与同页详情浮层两端各有这两层；目标用同页条件浮层加 geometryTransition 做展开与收起。

## 原因

逐层翻译会在同一子树里嵌套两对 geometryTransition；设备上（HarmonyOS 6.1.0 模拟器实测）嵌套配对使内层配对节点的子树丢失，浮层卡与收起后的列表卡都成了没有子节点的空卡，形变停在源几何上而错位。规格只列源端两层键或写成“两对”，后写的一端再照先写的一端镜像，两端会同时出错。

## 做法

1. 每端只挂一个 geometryTransition 承担形变，挂在外层容器上（对应 sharedBounds 的键），内层内容随容器一起过渡，不再给内层挂第二个配对键。
2. 规格写明每端一对、用哪个键、挂在哪个节点，并注明内层不再挂第二个；后写的一端与已写一端配对时，同时核对对方有没有嵌套第二个 geometryTransition，有就报告而不照样镜像。

## 可选检查

- 两端写完后在设备上打开、关闭一次，用控件树确认浮层卡和收起后的列表卡都还有子节点。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-b64a7b51e4483f31922d](../../../store/cases/case-b64a7b51e4483f31922d/2aa260d9288a6eff0bb812ceb75dcd8604eed8c05ed5024abb7e503939128ec1.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`2aa260d9288a6eff0bb812ceb75dcd8604eed8c05ed5024abb7e503939128ec1`
