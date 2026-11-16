# @ComponentV2 页面不用 CustomDialogController 套 V2 struct 做弹窗

审的是：代码
触发（任一种）：
- 读到：项目锁定 V2，页面写 `@ComponentV2`；规格转换决策给的是「CustomDialog（UIContext 形）或 bindSheet」或「@CustomDialog」；写错的样子：页面字段初始化 `new CustomDialogController({ builder: ... })`，builder 是 `@ComponentV2` struct；打开页面报 TypeError: class constructor cannot called without 'new'
- 读到：工程里已有 `CustomDialogController` 配普通 struct 的先例；写错的样子：照先例写 `CustomDialogController`，自检只看「没混用 V1/V2」
适用范围：为 @ComponentV2 页面选弹窗载体、写弹窗子组件时
做法：
- 用 @Local 显隐状态在根 Stack 末尾 if 条件渲染遮罩加卡片：卡片吞点击、点遮罩取消，底部弹窗对齐到底部
- 或用 bindSheet / bindContentCover，或 getUIContext().getPromptAction().openCustomDialog(componentContent)
- CustomDialogController 的 builder 必须是 @CustomDialog 组件；与「全 V2 不混用」冲突就换上面的载体，不改成 @ComponentV2 规避；先例与规格、文档不一致时以后者为准
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- CustomDialogController 仅在作为 @CustomDialog 和 @Component struct 成员变量、且在 @Component struct 内部定义时赋值才有效：@ComponentV2 页面里的 CustomDialogController 字段不在有效用法内（出处：ts-methods-custom-dialog-box.md，CustomDialogController 导入对象）
- 使用 @CustomDialog 装饰器装饰自定义弹出框；CustomDialogController 需在 @Component 内定义：builder 组件要用 @CustomDialog（出处：arkts-common-components-custom-dialog.md，创建自定义弹出框）
- CustomDialogControllerOptions.builder: any：声明不约束 builder 的类型，传错组件编译期发现不了，打开时才崩（出处：鸿蒙 SDK 的 ets/component/custom_dialog_controller.d.ts，CustomDialogControllerOptions.builder）
- openCustomDialog<T extends Object>(dialogContent: ComponentContent<T>, options?: promptAction.BaseDialogOptions): Promise<void>：UIContext 形的自定义弹窗，经 getPromptAction() 取得的 PromptAction 调用（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，PromptAction.openCustomDialog、UIContext.getPromptAction）
- bindSheet(isShow: boolean, builder: CustomBuilder, options?: SheetOptions): T：半模态弹出，V2 页面可直接用（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.bindSheet）
- bindContentCover(isShow: boolean, builder: CustomBuilder, options?: ContentCoverOptions): T：同族接口：全模态弹出（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.bindContentCover）
- 去掉 CustomDialogController、改为 @Local 显隐状态驱动的根 Stack 条件遮罩后，页面不再崩溃，弹窗正常：验证过的写法（出处：卡里修好并验证过）
未核实：bindSheet / bindContentCover / openCustomDialog 三种载体卡里没有上机验证，验证过的是根 Stack 条件遮罩；卡里的崩溃在目标 API 24 上看到，本机核对用的是 API 23 的声明
来源：1 张卡，1 个应用
- case-18113e210e1369d79e1d（免费来电多多）：做法第 1 步 ← 诊断、建议 1；做法第 2 步 ← 建议 1；做法第 3 步 ← 建议 2、建议 3；取值 7 ← 诊断
