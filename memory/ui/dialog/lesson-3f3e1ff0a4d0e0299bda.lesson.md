# @ComponentV2 页面不用 CustomDialogController 承载弹窗，改用 openCustomDialog、半模态或状态驱动浮层

ID：`lesson-3f3e1ff0a4d0e0299bda` · 版本：3

[本主题](index.md)

## 何时使用

界面实现阶段，为 @ComponentV2 页面选择弹窗承载方式、编写弹窗子组件时（含参照工程内已有弹窗写法时）

## 适用情境

项目要求页面与子组件都用 @ComponentV2、不混用 V1；需要把 Android Dialog/DialogFragment 一类居中或底部弹窗迁成 ArkUI；规格可能写着 CustomDialog、@CustomDialog 或 bindSheet。

## 原因

CustomDialogController 的 builder 约定是 @CustomDialog 组件；把 @ComponentV2 struct 当 builder 传入时，运行时在 builder 调用处报 TypeError: class constructor cannot called without 'new'，页面打开即崩溃或卡在加载态。编译能通过，自检若只查“有没有混用 V1/V2 装饰器”也发现不了；同工程已有这样写的先例时，照抄会让问题扩散。

## 做法

1. 在 V2 页面里从这些载体中选：页内 @Local 状态驱动的 Stack 条件浮层（遮罩＋卡片，卡片吞点击、遮罩点击关闭）、bindSheet/bindContentCover、UIContext.getPromptAction().openCustomDialog。
2. 写 CustomDialogController 前先核其 builder 约定；“全 V2、不混用”的规则与之冲突时换载体，不要把弹窗 struct 改写成 @ComponentV2 来绕开。
3. 自检时 grep CustomDialogController，逐个确认 builder 组件的装饰器，以及控制器是否在页面字段初始化时就执行构造。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-18113e210e1369d79e1d](../../../store/cases/case-18113e210e1369d79e1d/37c16bc6650280d7876fddb5a21db4abf1271051790070ee84ba091ba04450fb.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:4
  卡片版本：`37c16bc6650280d7876fddb5a21db4abf1271051790070ee84ba091ba04450fb`
