# 源 manifest 未声明 android:supportsRtl 时布局方向恒为 LTR：有顺序或对齐语义的容器逐个显式 Direction.Ltr

ID：`lesson-148a3e67bd557bafd722` · 版本：1

[本主题](index.md)

## 何时使用

规格提取与界面实现阶段，为带多语言资源的应用确定布局方向契约，新建按钮条、对话框面板等有顺序或起止对齐语义的容器时（含返修中用自绘面板替换系统弹窗）

## 适用情境

AndroidManifest 的 <application> 未声明 android:supportsRtl（安卓布局方向恒为 LTR）；应用含 fa 等 RTL 语言资源，或可能在 RTL 系统语言下运行；目标用 Row/Column 等容器实现按钮条、对话框或起始对齐的内容，未设 direction。

## 例外与边界

- 源端声明 android:supportsRtl="true"：按源布局的 start/end 语义让容器随语言方向翻转

## 原因

ArkUI 组件默认 Direction.Auto，跟随系统语言；来源实测子组件不继承父容器设置的方向，只给外层面板设 Ltr 时按钮条仍会镜像。未声明 supportsRtl 的源应用在 RTL 语言下保持 LTR，目标不显式固定，就会把负/正键顺序与起始对齐翻过来。

## 做法

1. 规格把“布局方向恒 LTR”写成目标契约；实现时在每个有顺序或对齐语义的容器（按钮条 Row、alignItems(Start) 的 Column、对话框面板）上显式 .direction(Direction.Ltr)，不只设在最外层。

## 可选检查

- 在阿拉伯语等 RTL 系统语言下截图，确认按钮顺序与起始对齐和安卓一致。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-e485c29b5b8cabfc9f01](../../../store/cases/case-e485c29b5b8cabfc9f01/a8e485f8e03e133b583406cbe9ebb22bb3f5d623076d62b99bab73fa82a762cb.json) · 结论：diagnosis, recommendation:2, recommendation:4
  卡片版本：`a8e485f8e03e133b583406cbe9ebb22bb3f5d623076d62b99bab73fa82a762cb`
