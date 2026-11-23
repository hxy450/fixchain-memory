# 对话框里的 EditText 把焦点、软键盘与预填光标分三项迁移：只获焦不弹键盘时 TextInput/TextArea 设 enableKeyboardOnFocus(false)，setText 预填后光标置于开头

## 何时使用

规格提取阶段为源端对话框内 EditText 写打开时的焦点、软键盘与预填光标契约时；弹层内容组件实现与宿主接线阶段落实这些初始状态时

## 适用情境

源端 AlertDialog/DialogFragment 用 setView 承载 EditText，靠布局 <requestFocus/> 或首个可获焦视图获焦，onCreateDialog 里 setText 预填；源码与 manifest 都没有 showSoftInput、setSoftInputMode 或 windowSoftInputMode。目标以 openCustomDialog 承载 TextInput/TextArea 内容组件，用 defaultFocus 或宿主 requestFocus 获焦。

## 例外与边界

- 源码显式请求输入法（showSoftInput，setSoftInputMode 为 STATE_VISIBLE/ALWAYS_VISIBLE，或 DialogPreference/EditTextPreference 打开时请求输入法）：按源端打开即弹键盘
- 光标在开头只是 setText 后没有另设选区时的默认：源码在 setText 之后自己调了 setSelection（如放到末尾或全选）或换了 movementMethod 的，按源码的选区实现，不一律 caretPosition(0)

## 原因

<requestFocus/> 只决定焦点：手机上的普通对话框窗口软输入模式为 STATE_UNSPECIFIED|ADJUST_PAN，只获焦、不弹键盘，点按输入框才弹（参照机 dumpsys input_method 实测 mShowRequested=false）。ArkUI TextInput/TextArea 的 enableKeyboardOnFocus 默认 true（文档写明 TextInput 在 TV 设备上默认 false），defaultFocus 或 requestFocus 获焦就会绑定输入法：首次打开可能不弹，再次打开就弹。安卓 setText 预填后光标在开头、长文本从首行显示；ArkUI 以 text 预填时光标在末尾并滚到末尾，直接键入会接在旧文本之后。把“打开即聚焦”写成“打开即弹软键盘”或不写光标位置时，实现照目标默认走。

## 做法

1. 规格为每个对话框输入框分三项写：焦点（谁获焦）、软键盘（源码显式请求才弹；STATE_UNSPECIFIED 解析为 adjustResize 或大屏时另核）、预填光标（setText 后在开头、从首行显示）；源码与 manifest 都看不出时，在参照机打开对话框用 adb shell dumpsys input_method 看 mShowRequested/mInputShown，按结果再写条目。
2. 实现时只获焦不弹键盘的 TextInput/TextArea 设 .enableKeyboardOnFocus(false)；预填框挂 TextInputController/TextAreaController，在首次 onFocus 时 caretPosition(0)。宿主需要补获焦（如 openCustomDialog().then 里 requestFocus(组件 id)）时，按组件写给宿主的义务落实。

## 可选检查

- 连开对话框几次、再点按一次输入框，分别看键盘是否弹出与光标位置。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 2 步〕enableKeyboardOnFocus 决定 TextInput 通过单击以外的方式（如 defaultFocus、requestFocus）获焦时是否主动拉起软键盘；未设置时 TV 设备为 false、其他设备为 true
- 〔原因〕对话框里的 TextInput/TextArea 没设 enableKeyboardOnFocus(false) 时，经 defaultFocus 或 requestFocus 获焦，首次打开可能不弹键盘、再次打开就弹
- 〔做法第 2 步〕TextInputController.caretPosition 以第一个字符前为 0；取值小于 0 时按 0，大于文本长度时光标放在文本末尾
- 〔原因 / 做法第 1 步〕安卓 EditText 在应用没有另设 movementMethod 时，移动方式是 ArrowKeyMovementMethod，其 initialize 调 Selection.setSelection(text, 0)，setText 后光标在开头
- 〔原因〕ArkUI TextInput/TextArea 以 text 预填时，光标停在末尾、长文本滚到末尾显示，直接键入接在旧文本之后
- 〔原因 / 做法第 1 步〕安卓 softInputMode 的 SOFT_INPUT_STATE_UNSPECIFIED（0）表示没有指定软键盘状态，由系统决定窗口获焦时显示或隐藏软键盘
- 〔原因〕安卓手机（Pixel 5）上只靠布局 <requestFocus/> 获焦的普通对话框，窗口 softInputMode 为 STATE_UNSPECIFIED|ADJUST_PAN|IS_FORWARD_NAVIGATION，dumpsys input_method 显示 mShowRequested=false，打开时不弹键盘，点按输入框才弹
