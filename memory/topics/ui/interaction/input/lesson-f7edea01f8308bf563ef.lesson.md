# EditText.setError 迁成尾部错误图标加聚焦时弹出的气泡、改动即清，不改成 showError 下方文字或常显红字

ID：`lesson-f7edea01f8308bf563ef` · 版本：2 · 阶段：spec/execute · 主题：[ui/interaction/input](index.md)

概要：setError 迁尾部图标加聚焦气泡、改动即清

信号：`setError`, `TextInputLayout`, `showError`, `errorMessage`, `bindPopup`, `indicator_input_error`, `onFocus`, `onBlur`

## 何时使用

规格提取阶段为调用 setError 的输入框写转换决策时；界面实现阶段把 EditText.setError 校验提示落成 ArkUI 输入框时

## 适用情境

源码对 EditText（或 TextView）调用 setError(msg) 提示校验失败（如保存时标题为空、两次密码不一致），布局里没有 TextInputLayout 或自定义错误视图；目标准备用 TextInput 的 showError/errorMessage 在框下显示错误文字、在输入框下常显红字，或规格写成“实时校验”。

## 例外与边界

- 源端用 TextInputLayout.setError（框下常显错误文字）或自绘错误视图时，按其呈现迁移

## 原因

TextView.setError 把右侧复合图标换成错误图标，消息只在该框持有焦点时以弹出气泡显示、失焦隐藏，任何按键改动文本后图标与消息一并清除（本机 android-36.1 TextView.setError 注释、Editor.onFocusChanged）。框下文字或行内红字常显、改变布局高度且不随输入清除；“实时校验”还会在源端只在提交时校验的流程里提前报错。规格先把目标平台能力登记为对应物，后续页面再以首个实现为先例，同一偏差会扩散到多页。

## 做法

1. 在源端调用 setError 的同一时机为对应输入框置错误状态：框尾显示错误图标（从本机 SDK 平台资源复制 indicator_input_error），该框聚焦时用 bindPopup 在框下弹出消息气泡，失焦隐藏、再次聚焦再显示。
2. 该框文本改变即清除错误状态（图标与气泡），源端 setError(null) 处同样清除；不做逐字实时校验。
3. 规格转换决策写“尾部错误图标 + 聚焦时气泡 + 改动即清”，不写成 showError/errorMessage 或实时校验；同工程已有页面以行内红字作为 setError 等价物时，不当作先例沿用。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [TextInput 关默认装饰，按主题状态背景复刻](lesson-1150c0c721e6dc0dede4.lesson.md)（共享 1 张卡）
- [不补源端没有的元素；框架默认元素须保留](../../../process/unapproved-deviation/lesson-352b96f599237cd27403.lesson.md)（共享 1 张卡）
- [未设 WebSettings 时按安卓默认逐项显式设](../../web/lesson-65ebab594a9dabe77ac2.lesson.md)（共享 1 张卡）
- [沿用已生成页面或兄弟写法前回源码核对语义](../../../process/secondary-over-source/lesson-e9c6e8ef1b29a6fe9c26.lesson.md)（共享 1 张卡）

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-9174c62c22f8d979372e](../../../../../store/cases/case-9174c62c22f8d979372e/eec4229b6f305745c835a372c2d8c2fb44e5a7937fa2f43696c8ce7707fe1efa.json) · 结论：diagnosis, rec-8c896c8866
  卡片版本：`eec4229b6f305745c835a372c2d8c2fb44e5a7937fa2f43696c8ce7707fe1efa`
