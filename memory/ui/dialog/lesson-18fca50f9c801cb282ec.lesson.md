# 源确认框用 setView 注入复选框等自定义内容时改用自定义弹窗承载，不写成 AlertDialog.show 的 builder 参数

ID：`lesson-18fca50f9c801cb282ec` · 版本：1

[本主题](index.md)

## 何时使用

界面实现阶段，把 Android AlertDialog/MaterialAlertDialogBuilder 转换为 ArkUI 弹窗、确定弹窗 API 与参数结构时

## 适用情境

源对话框在标题、正文和正负按钮之外还 setView 注入自定义布局（如“不再提示”复选框），确认回调读取其中控件的状态并写偏好；目标准备用 AlertDialog.show 弹出。

## 例外与边界

- 源对话框只有标题、正文与按钮，没有自定义视图，此时直接映射 AlertDialog.show

## 原因

AlertDialog.show 的参数只有标题、副标题、必填的 message、按钮等字段，没有承载自定义组件树的 builder；把自定义视图写进不存在的字段会让编译解析失败并引发大面积连锁错误。来源转换者写前已判断“自定义内容需 openCustomDialog”，落盘时又凭记忆假定存在带 builder 的参数形态；修复者删掉 builder 以通过编译，复选框及其偏好写入随之丢失。

## 做法

1. 先看源对话框是否调用 setView 或加载自定义布局：没有才映射 AlertDialog.show；有则用自定义弹窗，在同一个自定义构建里放正文、复选框与按钮，确认回调读取复选状态后再执行源端的偏好写入与后续动作。
2. V1 页面可用 @CustomDialog + CustomDialogController；@ComponentV2 页面用 UIContext.getPromptAction().openCustomDialog 或状态驱动浮层，不用 CustomDialogController 承载 V2 组件。
3. 只能先落简化弹窗时，把丢失的交互（控件、偏好写入）登记为占位与回补点，并在报告中列为与源端的行为差异；不以不存在的参数假装等价。

## 依赖经验

- [@ComponentV2 页面的弹窗不用 CustomDialogController 承载 V2 组件，改用状态驱动浮层、半模态或 openCustomDialog](lesson-3f3e1ff0a4d0e0299bda.lesson.md)

## 来源（按需复核）

- [case-d8867d30fe76e4d44ceb](../../../store/cases/case-d8867d30fe76e4d44ceb/3537efdf372896502b8a0b63e22b06ece4e7d54e2c06ca2c8c0ff730e6a5f932.json) · 结论：diagnosis, recommendation:1, recommendation:3
  卡片版本：`3537efdf372896502b8a0b63e22b06ece4e7d54e2c06ca2c8c0ff730e6a5f932`
