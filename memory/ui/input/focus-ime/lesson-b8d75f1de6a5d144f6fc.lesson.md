# 对话框里的 EditText 把焦点、软键盘与预填光标分三项迁移：只获焦不弹键盘时 TextInput/TextArea 设 enableKeyboardOnFocus(false)，setText 预填后光标置于开头

ID：`lesson-b8d75f1de6a5d144f6fc` · 版本：3

[本主题](index.md)

## 何时使用

规格提取阶段为源端对话框内 EditText 写打开时的焦点、软键盘与预填光标契约时；弹层内容组件实现与宿主接线阶段落实这些初始状态时

## 适用情境

源端 AlertDialog/DialogFragment 用 setView 承载 EditText，靠布局 <requestFocus/> 或首个可获焦视图获焦，onCreateDialog 里 setText 预填；源码与 manifest 都没有 showSoftInput、setSoftInputMode 或 windowSoftInputMode。目标以 openCustomDialog 承载 TextInput/TextArea 内容组件，用 defaultFocus 或宿主 requestFocus 获焦。

## 例外与边界

- 源码显式请求输入法（showSoftInput，setSoftInputMode 为 STATE_VISIBLE/ALWAYS_VISIBLE，或 DialogPreference/EditTextPreference 打开时请求输入法）：按源端打开即弹键盘

## 原因

<requestFocus/> 只决定焦点：手机上的普通对话框窗口软输入模式为 STATE_UNSPECIFIED|ADJUST_PAN，只获焦、不弹键盘，点按输入框才弹（参照机 dumpsys input_method 实测 mShowRequested=false）。ArkUI TextInput/TextArea 的 enableKeyboardOnFocus 默认 true，defaultFocus 或 requestFocus 获焦就会绑定输入法：首次打开可能不弹，再次打开就弹。安卓 setText 预填后光标在开头、长文本从首行显示；ArkUI 以 text 预填时光标在末尾并滚到末尾，直接键入会接在旧文本之后。把“打开即聚焦”写成“打开即弹软键盘”或不写光标位置时，实现照目标默认走。

## 做法

1. 规格为每个对话框输入框分三项写：焦点（谁获焦）、软键盘（源码显式请求才弹；STATE_UNSPECIFIED 解析为 adjustResize 或大屏时另核）、预填光标（setText 后在开头、从首行显示）；源码与 manifest 都看不出时，在参照机打开对话框用 adb shell dumpsys input_method 看 mShowRequested/mInputShown，按结果再写条目。
2. 实现时只获焦不弹键盘的 TextInput/TextArea 设 .enableKeyboardOnFocus(false)；预填框挂 TextInputController/TextAreaController，在首次 onFocus 时 caretPosition(0)。宿主需要补获焦（如 openCustomDialog().then 里 requestFocus(组件 id)）时，按组件写给宿主的义务落实。

## 可选检查

- 连开对话框几次、再点按一次输入框，分别看键盘是否弹出与光标位置。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-1446bd8a3fc8a14b0a94](../../../../store/cases/case-1446bd8a3fc8a14b0a94/fb6e49bb5629713c24983914208eda2fefbcb3374a3527d8ea29e518d7f15e63.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`fb6e49bb5629713c24983914208eda2fefbcb3374a3527d8ea29e518d7f15e63`
