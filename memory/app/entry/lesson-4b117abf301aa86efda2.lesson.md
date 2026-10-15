# 源 Activity 未声明 configChanges 且直接 show() 非托管对话框时，目标页内浮层补配置变化关闭路径

ID：`lesson-4b117abf301aa86efda2` · 版本：1

[本主题](index.md)

## 何时使用

规格提取阶段为每个 Activity 把 configChanges/screenOrientation 缺省翻译成页面生命周期与弹窗状态契约时；实现阶段用页内状态驱动的浮层承载源端对话框时

## 适用情境

源 Activity 未声明 android:configChanges 且未锁定 screenOrientation（旋转、语言、深浅色等都会重建它），页面用 AlertDialog.Builder.show()/Dialog.show() 直接弹出非托管对话框，不经 DialogFragment、showDialog 或 DialogPreference；目标用页内状态驱动的浮层承载该对话框，HarmonyOS 页面在旋转等配置变化时不重建。页面只有静态列表与弹窗、没有动态文案时同样适用。

## 例外与边界

- 对话框经 DialogFragment、Activity.showDialog 或 DialogPreference 托管时，源端重建后会恢复，目标保持浮层显示
- 源 Activity 在 configChanges 中声明了 orientation、screenSize 等并自行处理时，按其处理代码迁移

## 原因

重建时旧实例先存档（托管对话框的状态随存档保存），再销毁并关闭窗口，直接 show() 的对话框随旧窗口消失且不会恢复；托管对话框在新实例读档后恢复。目标页面在旋转或配置变化时不重建，页内浮层状态一直为真，对话框残留。规格只把“无 configChanges、无 screenOrientation”记成溯源事实时，没有人写关闭路径。

## 做法

1. 规格对每个未声明 configChanges 的 Activity（不论页面是否有动态文案）列出重建后消失与恢复的可见状态：直接 show() 的对话框消失，托管对话框恢复；把消失项写进状态接口的关闭条件与验收（例：对话框打开时旋转，对话框关闭、列表保留）。
2. 实现时为这些浮层补配置变化关闭路径：页面根容器 onAreaChange 判断横竖翻转，或由 EntryAbility.onConfigurationUpdate 通知页面，关闭浮层并保留列表等其余状态；Back、遮罩与返回键的关闭路径照常保留。

## 可选检查

- 对话框打开时旋转，两端都只剩列表、对话框关闭。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-b99e7061a74e82b731f3](../../../store/cases/case-b99e7061a74e82b731f3/f12a65132c4acbc8fdba01b0f8f225d439bcb9807cf4d66d5048269d53bd1c24.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`f12a65132c4acbc8fdba01b0f8f225d439bcb9807cf4d66d5048269d53bd1c24`
