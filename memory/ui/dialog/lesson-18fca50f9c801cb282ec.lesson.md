# 源对话框有 setView 自定义布局或 icon 槽时改用自定义弹窗承载，不写进 AlertDialog.show 参数也不省略

ID：`lesson-18fca50f9c801cb282ec` · 版本：5

[本主题](index.md)

## 何时使用

界面实现阶段，把 Android AlertDialog/MaterialAlertDialogBuilder 或 Compose AlertDialog 转换为 ArkUI 弹窗、确定弹窗 API 与参数结构时

## 适用情境

源对话框在标题、正文和正负按钮之外还 setView 注入自定义布局（如“不再提示”复选框），确认回调读取其中控件的状态并写偏好；目标准备用 AlertDialog.show 弹出。也包括 Compose AlertDialog 传了 icon = { Icon(...) }，目标准备改用没有图标槽的 showAlertDialog/AlertDialog.show，并以“仅视觉降级”或“与兄弟页同模式”为由省略图标。

## 例外与边界

- 源对话框只有标题、正文与按钮，没有自定义视图或图标：可以映射 AlertDialog.show，但正/负键按角色核对目标槽位位置；项目要求一比一还原平台默认外观时改用自定义弹窗复刻

## 原因

AlertDialog.show 的参数（component/alert_dialog.d.ts 的 AlertDialogParam）只有标题、副标题、必填的 message、按钮与外观等字段，没有承载自定义组件树的 builder，也没有图标槽；选它就等于删掉源端图标。把自定义视图写进不存在的字段会让编译解析失败并引发连锁错误，为通过编译删掉 builder 时，复选框及其偏好写入随之丢失。

## 做法

1. 先看源对话框是否调用 setView、加载自定义布局或传入 icon：都没有时才考虑 AlertDialog.show（按钮槽位与外观取舍见例外）；有则用自定义弹窗，在同一个自定义构建里放图标、标题、正文、复选框与按钮，确认回调读取复选状态后再执行源端的偏好写入与后续动作。
2. V1 页面可用 @CustomDialog + CustomDialogController；@ComponentV2 页面的载体选择见 lesson-3f3e1ff0a4d0e0299bda。
3. 确实只能先落简化弹窗时，把丢失的交互或视觉元素（控件、偏好写入、图标）按占位规则登记并写明回补方案，在报告中列为与源端的差异；有决策台账时先查台账，未命中就作为决策缺口上报，不以“仅视觉降级”或兄弟页先例自行定案，也不以不存在的参数假装等价。其余情况一律按第 1 步用自定义弹窗实现。

## 依赖经验

- [@ComponentV2 页面不用 CustomDialogController 承载弹窗，改用 openCustomDialog、半模态或状态驱动浮层](lesson-3f3e1ff0a4d0e0299bda.lesson.md)

来源支持：3 张卡 · 3 次迁移 · 3 个应用

## 来源（按需复核）

- [case-3b8b620c1c7fa2848a34](../../../store/cases/case-3b8b620c1c7fa2848a34/2c8f9548575702e3dd4840957d2d99053daa0e3fe45f93f40765b5cabcb618bd.json) · 结论：diagnosis, recommendation:3
  卡片版本：`2c8f9548575702e3dd4840957d2d99053daa0e3fe45f93f40765b5cabcb618bd`
- [case-bee1ccf417ac7e3b453c](../../../store/cases/case-bee1ccf417ac7e3b453c/068040f8788f96fdef9193826f1b953f434b4436bdfe72355d6b81975952282b.json) · 结论：recommendation:2, recommendation:3
  卡片版本：`068040f8788f96fdef9193826f1b953f434b4436bdfe72355d6b81975952282b`
- [case-d8867d30fe76e4d44ceb](../../../store/cases/case-d8867d30fe76e4d44ceb/3537efdf372896502b8a0b63e22b06ece4e7d54e2c06ca2c8c0ff730e6a5f932.json) · 结论：diagnosis, recommendation:1, recommendation:3
  卡片版本：`3537efdf372896502b8a0b63e22b06ece4e7d54e2c06ca2c8c0ff730e6a5f932`
