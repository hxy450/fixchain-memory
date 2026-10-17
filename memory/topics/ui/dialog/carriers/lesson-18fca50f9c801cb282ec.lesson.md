# 源对话框带目标系统弹窗没有的槽位（setView 注入的复选框等自定义布局、Compose AlertDialog 的 icon）时改用自定义弹窗承载，不写成 AlertDialog.show 的参数，也不自行省略

ID：`lesson-18fca50f9c801cb282ec` · 版本：4 · 阶段：execute · 主题：[ui/dialog/carriers](index.md)

概要：带 setView 或图标的对话框改用自定义弹窗

信号：`setView`, `AlertDialog.show`, `showAlertDialog`, `MaterialAlertDialogBuilder`, `@CustomDialog`, `CustomDialogController`, `openCustomDialog`, `@ComponentV2`, `UIContext.getPromptAction()`

## 何时使用

界面实现阶段，把 Android AlertDialog/MaterialAlertDialogBuilder 或 Compose AlertDialog 转换为 ArkUI 弹窗、确定弹窗 API 与参数结构时

## 适用情境

源对话框在标题、正文和正负按钮之外还 setView 注入自定义布局（如“不再提示”复选框），确认回调读取其中控件的状态并写偏好；目标准备用 AlertDialog.show 弹出。也包括 Compose AlertDialog 传了 icon = { Icon(...) }，目标准备改用没有图标槽的 showAlertDialog/AlertDialog.show，并以“仅视觉降级”或“与兄弟页同模式”为由省略图标。

## 例外与边界

- 源对话框只有标题、正文与按钮，没有自定义视图或图标：可以映射 AlertDialog.show，但正/负键按角色核对目标槽位位置；项目要求一比一还原平台默认外观时改用自定义弹窗复刻

## 原因

AlertDialog.show 的参数只有标题、副标题、必填的 message、按钮等字段，没有承载自定义组件树的 builder，也没有图标槽；选它就等于删掉源端图标，把自定义视图写进不存在的字段还会让编译解析失败并引发大面积连锁错误。来源转换者写前已判断“自定义内容需 openCustomDialog”，落盘时又凭记忆假定存在带 builder 的参数形态；修复者删掉 builder 以通过编译，复选框及其偏好写入随之丢失。

## 做法

1. 先看源对话框是否调用 setView、加载自定义布局或传入 icon：都没有时才考虑 AlertDialog.show（按钮槽位与外观取舍见例外）；有则用自定义弹窗，在同一个自定义构建里放图标、标题、正文、复选框与按钮，确认回调读取复选状态后再执行源端的偏好写入与后续动作。
2. V1 页面可用 @CustomDialog + CustomDialogController；@ComponentV2 页面用 UIContext.getPromptAction().openCustomDialog 或状态驱动浮层，不用 CustomDialogController 承载 V2 组件。
3. 只能先落简化弹窗时，把丢失的交互或视觉元素（控件、偏好写入、图标）登记为占位与回补点，并在报告中列为与源端的差异；有决策台账时先查台账，未命中就作为决策缺口上报，不以“仅视觉降级”或兄弟页先例自行定案，也不以不存在的参数假装等价。

## 依赖经验

- [V2 页面弹窗用浮层或 openCustomDialog](lesson-3f3e1ff0a4d0e0299bda.lesson.md)

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [编译修复只改报错行，不删功能或换异义替代](../../../process/check-gaming/lesson-29744eb694376e8acaca.lesson.md)（共享 2 张卡）
- [remember 按首次或 key 变才求值](../../state/lifecycle/lesson-3b4a96141329db62a6af.lesson.md)（共享 1 张卡）
- [写 SDK 调用前按本地 .d.ts 核对成员名与可空性](../../../arkts/api-signatures/lesson-6e558834938be19c04e2.lesson.md)（共享 1 张卡）
- [平台默认 AlertDialog 先从平台资源写可见契约](../frame/lesson-9c4de55af3c1ecd8eaa4.lesson.md)（共享 1 张卡）
- [平台差异只收敛做不到的一步，其余出口照源保留](../../../app/capability/degradation/lesson-9c973e50aaea054facdc.lesson.md)（共享 1 张卡）

来源支持：3 张卡 · 3 次迁移 · 3 个应用

## 来源（按需复核）

- [case-3b8b620c1c7fa2848a34](../../../../../store/cases/case-3b8b620c1c7fa2848a34/2c8f9548575702e3dd4840957d2d99053daa0e3fe45f93f40765b5cabcb618bd.json) · 结论：diagnosis, rec-80ac7eeebf
  卡片版本：`2c8f9548575702e3dd4840957d2d99053daa0e3fe45f93f40765b5cabcb618bd`
- [case-bee1ccf417ac7e3b453c](../../../../../store/cases/case-bee1ccf417ac7e3b453c/068040f8788f96fdef9193826f1b953f434b4436bdfe72355d6b81975952282b.json) · 结论：rec-9610125451, rec-7142863703
  卡片版本：`068040f8788f96fdef9193826f1b953f434b4436bdfe72355d6b81975952282b`
- [case-d8867d30fe76e4d44ceb](../../../../../store/cases/case-d8867d30fe76e4d44ceb/3537efdf372896502b8a0b63e22b06ece4e7d54e2c06ca2c8c0ff730e6a5f932.json) · 结论：diagnosis, rec-29a338fd62, rec-e4bcc6ead7
  卡片版本：`3537efdf372896502b8a0b63e22b06ece4e7d54e2c06ca2c8c0ff730e6a5f932`
