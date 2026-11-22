# @ComponentV2 页面的弹窗不用 CustomDialogController 承载 V2 组件，改用状态驱动浮层、半模态或 openCustomDialog

## 何时使用

界面实现阶段，为 @ComponentV2 页面选择弹窗承载方式、编写弹窗子组件时（含参照工程内已有弹窗写法时）

## 适用情境

项目要求页面与子组件都用 @ComponentV2、不混用 V1；需要把 Android Dialog/DialogFragment 一类居中或底部弹窗迁成 ArkUI；规格可能写着 CustomDialog、@CustomDialog 或 bindSheet。 换载体只换承载方式，不换呈现形态：源端是居中对话框时选居中的条件浮层或 openCustomDialog，bindSheet / bindContentCover 只用于源端本就是底部面板或全屏覆盖的弹窗；源弹窗的按钮集合和取消路径照旧。页面是 V1 的 @Component 时不在本条范围，CustomDialogController 加 @CustomDialog 照常可用。

## 原因

CustomDialogController 的 builder 约定是 @CustomDialog 组件；把 @ComponentV2 struct 当 builder 传入时，结构体构造语法不会被转译，运行时报 TypeError: class constructor cannot called without 'new'，页面打开或首次状态更新即崩溃或冻结。编译能通过，自检若只查“有没有混用 V1/V2 装饰器”也发现不了。来源中第一位写者没有采用规格给出的可用载体，第二位写者看到这个先例后推断“builder 接受任意组件”并照抄。

## 做法

1. 在 V2 页面里从这些载体中选：页内 @Local 状态驱动的 Stack 条件浮层（遮罩＋卡片，卡片吞点击、遮罩点击关闭）、bindSheet/bindContentCover、UIContext.getPromptAction().openCustomDialog。
2. 写 CustomDialogController 前先核其 builder 约定；“全 V2、不混用”的规则与之冲突时换载体，不要把弹窗 struct 改写成 @ComponentV2 来绕开。
3. 自检时 grep CustomDialogController，逐个确认 builder 组件的装饰器，以及控制器是否在页面字段初始化时就执行构造。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 未用。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 2 步〕CustomDialogController 仅在作为 @CustomDialog 和 @Component struct 的成员变量、且在 @Component struct 内部定义时赋值才有效
- 〔原因 / 做法第 2 步〕自定义弹出框的内容组件要用 @CustomDialog 装饰，CustomDialogController 要在 @Component 内定义
- 〔原因〕CustomDialogControllerOptions.builder 在声明里是 any 类型，传入什么组件编译期都不检查
- 〔原因〕@ComponentV2 页面里 CustomDialogController 的 builder 写成 V2 结构体调用时编译通过，真机打开页面即 jscrash：TypeError: class constructor cannot called without 'new'，位置在 builder 调用处，页面卡在加载态
