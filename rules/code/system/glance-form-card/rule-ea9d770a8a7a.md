# Glance 按实际宽高选布局时，由 FormExtensionAbility 取卡片尺寸下发给卡片页

审的是：代码
触发（任一种）：
- 读到：GlanceAppWidget 设 SizeMode.Exact，按 LocalSize.current 的宽高分支布局；规格写按实际尺寸渲染；写错的样子：EntryFormAbility 只按 `ohos.extra.param.key.form_dimension` 的档位映射形态，没有 getFormRect 调用和 onSizeChanged；卡片页没有 @LocalStorageProp 宽高
适用范围：Glance 小部件迁成 ArkTS 服务卡片、源端按连续宽高选布局时；getFormRect、onSizeChanged 出自声明 @since 20
做法：
- onAddForm 里从 want.parameters[formInfo.FormParam.IDENTITY_KEY] 取 formId，调 formProvider.getFormRect(formId).then(rect => formProvider.updateForm(formId, formBindingData.createFormBindingData({ cardWidth: rect.width, cardHeight: rect.height })))
- 实现 onSizeChanged(formId, newDimension, newRect)，把 newRect.width / height 同样 updateForm 下发；单位是 vp，直接和源端 LocalSize 的 dp 断点比
- 卡片页 @LocalStorageProp('cardWidth') cardWidth: number = 0（高同理），按源端断点派生形态
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onSizeChanged(formId: string, newDimension: formInfo.FormDimension, newRect: formInfo.Rect): void：卡片尺寸变化时回调，newRect 是卡片的新矩形，单位 vp（出处：鸿蒙 SDK 的 ets/api/@ohos.app.form.FormExtensionAbility.d.ts，FormExtensionAbility.onSizeChanged）
- function getFormRect(formId: string): Promise<formInfo.Rect>：查询卡片相对屏幕左上角的位置和卡片尺寸（出处：鸿蒙 SDK 的 ets/api/@ohos.app.form.formProvider.d.ts，formProvider.getFormRect；js-apis-app-form-formProvider.md，formProvider.getFormRect）
- interface Rect { left: number; top: number; width: number; height: number }：getFormRect 和 onSizeChanged 给出的矩形，宽高取 width、height（出处：鸿蒙 SDK 的 ets/api/@ohos.app.form.formInfo.d.ts，formInfo.Rect）
- function updateForm(formId: string, formBindingData: formBindingData.FormBindingData): Promise<void>：把数据推给卡片，卡片页的 @LocalStorageProp 按键名收到（出处：鸿蒙 SDK 的 ets/api/@ohos.app.form.formProvider.d.ts，formProvider.updateForm）
- function createFormBindingData(obj?: Object | string): FormBindingData：把 { cardWidth, cardHeight } 包成 updateForm 要的数据（出处：鸿蒙 SDK 的 ets/api/@ohos.app.form.formBindingData.d.ts，formBindingData.createFormBindingData）
- IDENTITY_KEY = "ohos.extra.param.key.form_identity"：onAddForm 的 want.parameters 里取 formId 用的键（出处：鸿蒙 SDK 的 ets/api/@ohos.app.form.formInfo.d.ts，formInfo.FormParam.IDENTITY_KEY）
- declare const LocalStorageProp: (value: string) => PropertyDecorator（注释带 @form）：卡片页可用的装饰器，按键名接收 updateForm 推来的值（出处：鸿蒙 SDK 的 ets/component/common.d.ts，LocalStorageProp）
针对本应用要查的：
- 源端选布局用的宽高断点：源工程里 GlanceAppWidget 的 provideGlance / 内容 Composable 中对 LocalSize.current.width、height 的比较；比较用的 dp 数值原样作为卡片页对 cardWidth / cardHeight 的 vp 阈值
来源：1 张卡，1 个应用
- case-77c6596fcdf362f9e832（Jetsnack）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1、诊断；做法第 3 步 ← 建议 1
