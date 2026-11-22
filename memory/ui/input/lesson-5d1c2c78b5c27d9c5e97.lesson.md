# EditText.setError 迁为尾部错误图标加仅聚焦时显示的气泡、输入即清，不用 errorMessage 常显红字或行内文字

ID：`lesson-5d1c2c78b5c27d9c5e97` · 版本：1

[本主题](index.md)

## 何时使用

规格提取与界面实现阶段，为源端 EditText.setError（含 AppCompatEditText）写转换决策并落实校验失败提示时

## 适用情境

源端校验失败时对输入框调用 setError(文案)，没有自定义错误视图；目标为 ArkUI TextInput，候选是 TextInput.errorMessage、输入框下方的行内红字或自绘气泡；规格可能写成“实时校验”或“HarmonyOS 自带错误提示”。

## 例外与边界

- 源端用 Material TextInputLayout.setError（框下常显错误文字）而不是 EditText.setError：按该控件的呈现实现

## 原因

TextView.setError 的呈现是尾部 compound drawable 位置的错误图标，加上只在该框获得焦点时弹出的错误气泡（Editor 的 ErrorPopup）；按键改变文本时图标与消息一起清除（本机 SDK android-36.1 源码 TextView.setError 的注释与实现）。errorMessage 或行内红字常显在框下、改变布局高度且不随焦点出现，校验时机也被改成实时校验。

## 做法

1. 规格转换决策写成“尾部错误图标 + 仅聚焦时显示的错误气泡 + 输入即清除”，并保留源端调用 setError 的时机（如点保存或确认时才校验）；不写成 errorMessage 或实时校验。
2. 实现时在输入框尾部叠错误图标（取平台 indicator_input_error 资源，本机 SDK platforms/android-<api>/data/res），用锚定该框的 bindPopup 或自绘气泡显示文案，可见条件为“有错误且该框聚焦”；该框 onChange 时清除其错误状态。多个框同时出错时各自保留图标，气泡只随聚焦的框显示。

来源支持：2 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-9174c62c22f8d979372e](../../../store/cases/case-9174c62c22f8d979372e/eec4229b6f305745c835a372c2d8c2fb44e5a7937fa2f43696c8ce7707fe1efa.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`eec4229b6f305745c835a372c2d8c2fb44e5a7937fa2f43696c8ce7707fe1efa`
- [case-e91d2b9a9a156d1023ec](../../../store/cases/case-e91d2b9a9a156d1023ec/3558471f038583b62bb0d5d4b2516ab8ea7ee5c983b222032cb253201c25aec8.json) · 结论：recommendation:3
  卡片版本：`3558471f038583b62bb0d5d4b2516ab8ea7ee5c983b222032cb253201c25aec8`
