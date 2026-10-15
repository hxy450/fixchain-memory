# 从组件外的共享函数打开自定义弹窗时，用 wrapBuilder + ComponentContent 交给 openCustomDialog(content)：不在 options.builder 闭包里直接调用全局 @Builder

ID：`lesson-a3ac761b0d52a6bccb9f` · 版本：1

[本主题](index.md)

## 何时使用

界面实现阶段，把路由页改成多个入口复用的自定义弹窗，确定弹窗内容的构建与挂载方式时

## 适用情境

ArkTS V2（@ComponentV2）工程中，把 BottomSheetDialog/DialogFragment 一类弹窗迁成 UIContext.getPromptAction().openCustomDialog，并打算从组件外的导出函数（只持有 UIContext）为多个页面统一打开同一个自定义组件。

## 原因

SDK 声明要求 openCustomDialog 的 builder 写成 () => { this.xxx() } 调用组件内的 @Builder，全局 @Builder 须在组件内的 builder 中调用；模块级函数里的闭包直接调用全局 @Builder 并创建 V2 组件时缺少这层构建上下文，点击入口即崩溃，而编译与文本契约都能通过。项目参考只用组件内示例展示了这个前提，没有写成显式规则。

## 做法

1. 共享函数打开弹窗时：wrapBuilder(全局 Builder) 加 new ComponentContent(uiContext, wrapped, 参数)，用 openCustomDialog(content, options) 打开、closeCustomDialog(content) 关闭，并在 onDidDisappear 与打开失败分支调用 content.dispose()。
2. 保留 options.builder 写法时，把 @Builder 放在发起弹窗的 @ComponentV2 内，按 builder: () => { this.xxx() } 调用，由各入口组件自己打开；抽成共享 helper 时不能省掉这层 this 绑定。

## 可选检查

- 改动弹窗打开方式后，在设备上点击入口并比较点击前后的进程 PID；编译与文本契约通过不能说明构建上下文正确。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-256a1816e74ef8a6f70d](../../../store/cases/case-256a1816e74ef8a6f70d/63aa9c47d39447b16f155cf0b16dc001c803278a922f7f0fa60b57ccb46128ad.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`63aa9c47d39447b16f155cf0b16dc001c803278a922f7f0fa60b57ccb46128ad`
