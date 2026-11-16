# 源端实际是 adjustResize 时，在 loadContent 回调里显式设 RESIZE 避让

审的是：代码
触发（任一种）：
- 读到：规格的软键盘条目只写「默认」；源 manifest 无 windowSoftInputMode，布局含 EditText 和 ListView / ScrollView（或继承 ListActivity）；写错的样子：EntryAbility 的 windowStage.loadContent 回调里没有 setKeyboardAvoidMode，窗口沿用缺省 KeyboardAvoidMode.OFFSET 整页上推
适用范围：页面含 TextInput、源 Activity 的软键盘模式实际解析为 adjustResize 时
做法：
- 规格只写了「默认」时回查源 manifest 和布局确认实际模式；ArkUI 缺省 OFFSET 只对应 adjustPan
- adjustResize 时在 windowStage.loadContent 的回调里取窗口的 UIContext，调 getUIContext().setKeyboardAvoidMode(KeyboardAvoidMode.RESIZE)
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- setKeyboardAvoidMode(value: KeyboardAvoidMode): void，Default mode: KeyboardAvoidMode.OFFSET：窗口级键盘避让模式（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，UIContext.setKeyboardAvoidMode）
- KeyboardAvoidMode.OFFSET = 0、RESIZE = 1、OFFSET_WITH_CARET = 2、RESIZE_WITH_CARET = 3、NONE = 4：窗口级避让模式的取值（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，KeyboardAvoidMode）
- import { KeyboardAvoidMode } from '@kit.ArkUI'（导出自 @ohos.arkui.UIContext）：不导入时用到的是 common.d.ts 里全局的同名枚举 KeyboardAvoidMode（只有 DEFAULT、NONE，给弹窗、半模态用），没有 RESIZE（出处：鸿蒙 SDK 的 ets/kits/@kit.ArkUI.d.ts，KeyboardAvoidMode；ets/component/common.d.ts，KeyboardAvoidMode）
- getUIContext(): UIContext：Window 上取 UIContext 的方法（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，Window.getUIContext）
- 在 loadContent 回调里加 getUIContext().setKeyboardAvoidMode(KeyboardAvoidMode.RESIZE) 后，键盘弹出时行为和源端一致：修好的写法（出处：卡里修好并验证过）
针对本应用要查的：
- 源 Activity 的软键盘模式实际是 resize 还是 pan：源工程 AndroidManifest.xml 里该 activity 的 android:windowSoftInputMode，没有时看它的布局 XML 和父类；声明了就照声明；没声明时有可滚动视图（ListView、ScrollView、RecyclerView 或继承 ListActivity）取 RESIZE，没有取 OFFSET
来源：1 张卡，1 个应用
- case-c96bdbf4d2e0fb58e797（Blockinger）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2、诊断；取值 5 ← 诊断
