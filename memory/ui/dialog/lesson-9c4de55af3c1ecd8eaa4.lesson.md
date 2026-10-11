# 只靠平台默认外观的 AlertDialog 迁移前写出可见契约：按钮按角色核对目标槽位位置，要求一比一还原时用自定义弹窗复刻平台样式，不写“系统弹窗 1:1”

ID：`lesson-9c4de55af3c1ecd8eaa4` · 版本：1

[本主题](index.md)

## 何时使用

规格提取阶段为源端系统对话框写转换决策时，以及界面实现阶段按该决策落地 ArkUI 系统弹窗或自定义弹窗时

## 适用情境

源码用 AlertDialog.Builder 内联构造确认框，只设 title、message、setPositiveButton、setNegativeButton，无自定义布局或样式，外观由应用主题继承的平台默认警告框决定；目标准备用 ArkUI AlertDialog.show(primaryButton/secondaryButton) 等系统弹窗替代，项目要求与源端逐屏一致。

## 例外与边界

- 项目明确接受目标系统弹窗的固有外观、只要求文案与按键行为一致；此时仍按角色核对按钮槽位

## 原因

“正/负”是按钮角色，不是参数次序。ArkUI AlertDialog 把 primaryButton 放在左侧，自带居中标题、大圆角卡片、首字母大写的彩色按钮与全窗居中；来源中的安卓平台默认警告框是标题左对齐、按钮靠右且负键在左正键在右、全大写、小圆角，遮罩浓度与进出场取自平台主题。只写“系统组件 1:1/行为等价”时规格没有视觉契约，转换者照映射参考直接替换，版式与按钮顺序整体偏离。

## 做法

1. 按源端实际使用的对话框类与应用主题确定渲染样式（例如框架 android.app.AlertDialog 在 AppCompat Light 主题下取平台 Theme.Material.Light.Dialog.Alert），把按钮排位、按钮文字大小写、标题对齐、面板宽度与圆角、遮罩浓度、显示位置、进出场、点外部与返回键是否关闭写进规格，并注明取值来源的平台资源及版本。
2. 映射按钮时先查目标弹窗把每个参数槽位放在哪一侧，再按角色和视觉位置决定正/负键放进哪个槽位。
3. 目标系统弹窗的固有版式与源端对不上而任务要求一比一时，规格直接决定用自定义弹窗（openCustomDialog 加自绘面板）复刻；实现阶段若规格只写了“系统弹窗 1:1”，先与源端截图或平台样式逐项比对，有差异就回报规格或改用自定义实现。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-bee1ccf417ac7e3b453c](../../../store/cases/case-bee1ccf417ac7e3b453c/068040f8788f96fdef9193826f1b953f434b4436bdfe72355d6b81975952282b.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`068040f8788f96fdef9193826f1b953f434b4436bdfe72355d6b81975952282b`
