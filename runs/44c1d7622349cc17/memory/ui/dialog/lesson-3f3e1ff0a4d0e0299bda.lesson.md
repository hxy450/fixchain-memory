# @ComponentV2 页面的弹窗不用 CustomDialogController 承载 V2 组件，改用状态驱动浮层、半模态或 openCustomDialog

ID：`lesson-3f3e1ff0a4d0e0299bda` · 版本：1

[本主题](index.md)

## 何时使用

界面实现阶段，为 @ComponentV2 页面选择弹窗承载方式、编写弹窗子组件时（含参照工程内已有弹窗写法时）

## 适用情境

项目要求页面与子组件都用 @ComponentV2、不混用 V1；需要把 Android Dialog/DialogFragment 一类居中或底部弹窗迁成 ArkUI；规格可能写着 CustomDialog、@CustomDialog 或 bindSheet。

## 原因

CustomDialogController 的 builder 约定是 @CustomDialog 组件；把 @ComponentV2 struct 当 builder 传入时，结构体构造语法不会被转译，运行时报 TypeError: class constructor cannot called without 'new'，页面打开或首次状态更新即崩溃或冻结。编译能通过，自检若只查“有没有混用 V1/V2 装饰器”也发现不了。来源中第一位写者没有采用规格给出的可用载体，第二位写者看到这个先例后推断“builder 接受任意组件”并照抄。

## 做法

1. 在 V2 页面里从这些载体中选：页内 @Local 状态驱动的 Stack 条件浮层（遮罩＋卡片，卡片吞点击、遮罩点击关闭）、bindSheet/bindContentCover、UIContext.getPromptAction().openCustomDialog。
2. 写 CustomDialogController 前先核其 builder 约定；“全 V2、不混用”的规则与之冲突时换载体，不要把弹窗 struct 改写成 @ComponentV2 来绕开。
3. 自检时 grep CustomDialogController，逐个确认 builder 组件的装饰器，以及控制器是否在页面字段初始化时就执行构造。

## 来源（按需复核）

经验是有适用范围的历史建议。核查来源时同时看结论与 unknown；来源卡未随阅读包复制。

- case-18113e210e1369d79e1d · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:4
  卡片版本：`74f215ee70468d99d599856323715d9f955e3102e23b4e774dadfccd1dce2a6f`
