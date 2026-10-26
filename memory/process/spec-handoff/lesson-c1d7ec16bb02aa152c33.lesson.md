# 规格提取把 AndroidManifest 声明（含未声明的平台缺省）解析成实际行为与鸿蒙目标值并指派实现：未声明 screenOrientation 时 EntryAbility 写 orientation: auto_rotation_restricted；未声明 windowSoftInputMode 时按是否含可滚动视图取 RESIZE/OFFSET，并写出首屏焦点与是否弹键盘；“默认”不能作目标值

ID：`lesson-c1d7ec16bb02aa152c33` · 版本：5

[本主题](index.md)

## 何时使用

规格提取阶段，为每个 Activity 整理全屏、方向、软键盘等窗口行为，并整理 application 级属性（备份等）时；把“横竖屏双布局”“默认弹出”这类结论写进决策账本或页面规格时

## 适用情境

窗口方向（如 screenOrientation=sensorLandscape）只声明在 AndroidManifest，Java 源码只见全屏标志一类调用；页面规格模板与元数据可能没有方向字段。也包括 application 显式 allowBackup=false，activity 未声明 screenOrientation、windowSoftInputMode 而依赖平台缺省；界面图谱把它们记为 unspecified/unknown，功能基线与计划都没有对应任务，目标备份配置保持模板值。 也包括各 activity 未声明 screenOrientation、源有 layout-land/values-land，规格只写“横竖屏双布局全支持”，module.json5 的 abilities 没有 orientation；以及未声明 windowSoftInputMode、布局含 EditText 和 ListView/ScrollView（或 Activity 继承 ListActivity），规格只写“无 windowSoftInputMode（默认弹出）”。

## 原因

只读 Java 源码会漏掉 manifest 属性；规格与页面元数据都没有方向字段时，实现者会以“规格未覆盖”跳过。记为 unspecified/unknown 的项没有目标值，下游没有写者，模板默认值（如允许备份）会保留到交付。鸿蒙 EntryAbility 不写 orientation 就不随传感器旋转，只迁两套布局时横屏分支永不出现；未声明 windowSoftInputMode 时安卓缺省 adjustUnspecified 由系统按窗口是否含可滚动视图取 adjustResize 或 adjustPan，而 ArkUI 缺省 OFFSET 整页上推；状态半 stateUnspecified 让首个可获焦视图为 EditText 时自动弹键盘，ArkUI 不会自动给输入框焦点。另一应用中注入的一行提醒只剩“无screenOrientation=跟随旋转”“无windowSoftInputMode（默认）”，写者照写安卓语义就算交差，目标值没有进入任何任务。

## 做法

1. 逐个 activity 列出 manifest 属性，把未声明项解析成实际行为再写鸿蒙目标值，“默认/按系统缺省”不能作结论：未声明 screenOrientation（随系统旋转）时，module.json5 的 EntryAbility 写 orientation: auto_rotation_restricted，与权限并列为 module.json5 必做项；sensorLandscape 等锁定值写成“进入页 setPreferredOrientation(对应方向)、离开恢复”的验收条目。
2. 未声明 windowSoftInputMode 且含 EditText 时拆成两条验收并各自指派：调整方式——窗口含 ListView/ListActivity/ScrollView 等可滚动视图为 adjustResize（目标窗口级 setKeyboardAvoidMode(KeyboardAvoidMode.RESIZE)），否则为 adjustPan（OFFSET）；状态——首屏焦点给布局顺序中第一个可获焦视图（AdapterView 只在有数据时可获焦），写清各数据分支谁获焦、是否自动弹键盘。
3. application 级属性同样逐项映射（如 allowBackup → allowToBackupRestore）并为每项指派实现任务，不留 unknown。

## 可选检查

- 解除旋转锁并转 90°，窗口宽高互换、横屏分支出现；点输入框弹出键盘时顶部内容不被推出屏幕、内容区收缩。

来源支持：7 张卡 · 已知 4 次迁移（部分未记录） · 已知 4 个应用（部分未记录）

## 来源（按需复核）

- [case-11ff372c001b24f1dce2](../../../store/cases/case-11ff372c001b24f1dce2/f40c870d5e700ffb6226a4e7a20d9f684a6cac4051a6d541d8c5312bdc75d985.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`f40c870d5e700ffb6226a4e7a20d9f684a6cac4051a6d541d8c5312bdc75d985`
- [case-1b03af761b99c891e236](../../../store/cases/case-1b03af761b99c891e236/d25c19688c8b9de99ca7f74859821e8e30e81052b97268686628491ed8614154.json) · 结论：diagnosis, recommendation:1, recommendation:3
  卡片版本：`d25c19688c8b9de99ca7f74859821e8e30e81052b97268686628491ed8614154`
- [case-5e35bb283520acf3bd35](../../../store/cases/case-5e35bb283520acf3bd35/954c420a6eb53234d9a40e9851863e13e6a2b9e3e2195abc6f71fcfe048dcf4f.json) · 结论：recommendation:1
  卡片版本：`954c420a6eb53234d9a40e9851863e13e6a2b9e3e2195abc6f71fcfe048dcf4f`
- [case-69a2766b2050118ebd5a](../../../store/cases/case-69a2766b2050118ebd5a/6d5ac1c6e6d2ab3eae9fdfa84fcbe2a5898f18f062dd05c39baed1dcb8862237.json) · 结论：diagnosis, recommendation:1
  卡片版本：`6d5ac1c6e6d2ab3eae9fdfa84fcbe2a5898f18f062dd05c39baed1dcb8862237`
- [case-c6c056189eaa36176e28](../../../store/cases/case-c6c056189eaa36176e28/2cb68533b47b0adbcc44f6714eab0ed4eee48b603073820527988ebacca82229.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`2cb68533b47b0adbcc44f6714eab0ed4eee48b603073820527988ebacca82229`
- [case-c96bdbf4d2e0fb58e797](../../../store/cases/case-c96bdbf4d2e0fb58e797/690e3e8044afac976d280680a439898d1d9c1767283cf4bcd2d13a82c3977cf3.json) · 结论：diagnosis, recommendation:1, recommendation:3
  卡片版本：`690e3e8044afac976d280680a439898d1d9c1767283cf4bcd2d13a82c3977cf3`
- [case-cc22f6cc1041c8cc1129](../../../store/cases/case-cc22f6cc1041c8cc1129/ec6e60182fe19865967b7c173312ac2be6c4dbf45c87407c6da85b673b5778f3.json) · 结论：recommendation:4
  卡片版本：`ec6e60182fe19865967b7c173312ac2be6c4dbf45c87407c6da85b673b5778f3`
