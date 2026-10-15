# 规格提取逐项盘点 AndroidManifest 的 activity 与 application 属性，未声明项先解析成平台行为再写鸿蒙目标值

ID：`lesson-c1d7ec16bb02aa152c33` · 版本：5

[本主题](index.md)

## 何时使用

规格提取阶段，为每个 Activity 整理方向、软键盘等窗口属性，并整理 application 级属性（备份等）时；把“默认”“按系统缺省”一类结论写进决策账本或页面规格时

## 适用情境

activity 未声明 screenOrientation、windowSoftInputMode 而依赖平台缺省，或 application 显式 allowBackup=false；界面图谱把它们记为 unspecified/unknown，功能基线与计划都没有对应任务，目标备份配置保持模板值；规格只写“无 windowSoftInputMode（默认弹出）”一类安卓语义。

## 原因

只读 Java 源码会漏掉 manifest 属性；记为 unspecified/unknown 或“默认”的项没有目标值，下游没有写者，模板默认值（如允许备份）会保留到交付。平台缺省本身是确定行为（未声明 screenOrientation 随系统旋转，未声明 windowSoftInputMode 按窗口内容取调整方式），鸿蒙缺省与之不同，只写安卓语义等于没有给出目标值。

## 做法

1. 逐个 activity 与 application 列出 manifest 属性，同时查主题中的对应属性（如 android:windowSoftInputMode）与代码里的运行时设置（setRequestedOrientation、getWindow().setSoftInputMode），代码设置优先（manifest 的 windowSoftInputMode 在 Activity.attach 时写入窗口，主题值只在未设置时由 PhoneWindow 采用，android-36.1）；未声明项先解析成平台实际行为，再写鸿蒙目标值，“默认/按系统缺省”不能作结论。
2. 方向按屏幕方向的经验映射为 EntryAbility 的 orientation 或页内 setPreferredOrientation，与权限并列列为 module.json5 必做项。
3. 含输入框的窗口把软键盘拆成两条验收并各自指派：调整方式（adjustResize/adjustPan 的判定与 KeyboardAvoidMode）与首屏焦点和是否自动弹键盘（按布局顺序、数据分支与 state 值）。
4. application 级属性逐项映射（如 allowBackup → 备份配置 backup_config 的 allowToBackupRestore）并为每项指派实现任务，不留 unknown。

## 依赖经验

- [源窗口按 resize 避让软键盘时设 KeyboardAvoidMode.RESIZE（含未声明的隐式 adjustResize），不用默认 OFFSET](../../ui/safearea/lesson-f86b02e97cc77e31d51a.lesson.md)
- [首屏输入框按源端获焦并自动弹键盘时，先核 windowSoftInputMode 与获焦条件，再在窗口获焦后 requestFocus](../../ui/input/lesson-9d42548ee3c075de3330.lesson.md)

来源支持：5 张卡 · 3 次迁移 · 3 个应用

## 来源（按需复核）

- [case-1b03af761b99c891e236](../../../store/cases/case-1b03af761b99c891e236/d25c19688c8b9de99ca7f74859821e8e30e81052b97268686628491ed8614154.json) · 结论：diagnosis, recommendation:1, recommendation:3
  卡片版本：`d25c19688c8b9de99ca7f74859821e8e30e81052b97268686628491ed8614154`
- [case-5e35bb283520acf3bd35](../../../store/cases/case-5e35bb283520acf3bd35/954c420a6eb53234d9a40e9851863e13e6a2b9e3e2195abc6f71fcfe048dcf4f.json) · 结论：recommendation:1
  卡片版本：`954c420a6eb53234d9a40e9851863e13e6a2b9e3e2195abc6f71fcfe048dcf4f`
- [case-c6c056189eaa36176e28](../../../store/cases/case-c6c056189eaa36176e28/2cb68533b47b0adbcc44f6714eab0ed4eee48b603073820527988ebacca82229.json) · 结论：recommendation:1
  卡片版本：`2cb68533b47b0adbcc44f6714eab0ed4eee48b603073820527988ebacca82229`
- [case-c96bdbf4d2e0fb58e797](../../../store/cases/case-c96bdbf4d2e0fb58e797/690e3e8044afac976d280680a439898d1d9c1767283cf4bcd2d13a82c3977cf3.json) · 结论：diagnosis, recommendation:1, recommendation:3
  卡片版本：`690e3e8044afac976d280680a439898d1d9c1767283cf4bcd2d13a82c3977cf3`
- [case-cc22f6cc1041c8cc1129](../../../store/cases/case-cc22f6cc1041c8cc1129/ec6e60182fe19865967b7c173312ac2be6c4dbf45c87407c6da85b673b5778f3.json) · 结论：recommendation:4, diagnosis
  卡片版本：`ec6e60182fe19865967b7c173312ac2be6c4dbf45c87407c6da85b673b5778f3`
