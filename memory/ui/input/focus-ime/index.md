# ui/input/focus-ime

输入焦点与软键盘：首屏输入框按平台缺省获焦的时机（窗口获焦后再 requestFocus），对话框里 EditText 的焦点、软键盘与预填光标，会被子页覆盖再返回的页面里获焦来源的判别，只收键盘不清焦点的 IME 接口选择（hideTextInput 与需系统权限的接口）

[上一级](../index.md)

## 本级经验

- [会被子页覆盖再返回的页面里，TextInput 的获焦回调先判别是否由用户触摸引起再写业务状态](lesson-4c476a62732697c56c22.lesson.md)
  - 时机：界面实现阶段，把 TextInput 的焦点回调接到页面业务状态，且页面常驻 NavBar 或保活容器、会被 pushPath 覆盖时
  - 情境：页面用 focused 之类的业务字段决定显示分支（如建议列表与分类）；从子页系统返回后，框架可能把焦点交还该 TextInput。
- [只收键盘不清焦点用 hideTextInput：show/hideSoftKeyboard 需系统权限，stopInputSession 会让输入框失焦](lesson-edae4e2795ec169255bb.lesson.md)
  - 时机：界面与服务实现阶段，把 InputMethodManager 的显示、隐藏软键盘调用迁到 IMEKit 或 ArkUI 输入组件时
  - 情境：源端用 InputMethodManager.hideSoftInputFromWindow 只收键盘、焦点仍留在输入框，或用 showSoftInput 弹键盘；规格写“inputMethodController，具体方法实现期核实”；目标是三方应用，调用方可能依赖输入框的焦点态。
  - 例外：源端收键盘时同时 clearFocus：此时结束编辑并失焦正是源端语义
- [对话框里的 EditText 把焦点、软键盘与预填光标分三项迁移：只获焦不弹键盘时 TextInput/TextArea 设 enableKeyboardOnFocus(false)，setText 预填后光标置于开头](lesson-b8d75f1de6a5d144f6fc.lesson.md)
  - 时机：规格提取阶段为源端对话框内 EditText 写打开时的焦点、软键盘与预填光标契约时；弹层内容组件实现与宿主接线阶段落实这些初始状态时
  - 情境：源端 AlertDialog/DialogFragment 用 setView 承载 EditText，靠布局 &lt;requestFocus/&gt; 或首个可获焦视图获焦，onCreateDialog 里 setText 预填；源码与 manifest 都没有 showSoftInput、setSoftInputMode 或 windowSoftInputMode。目标以 openCustomDialog 承载 TextInput/TextArea 内容组件，用 defaultFocus 或宿主 requestFocus 获焦。
  - 例外：源码显式请求输入法（showSoftInput，setSoftInputMode 为 STATE_VISIBLE/ALWAYS_VISIBLE，或 DialogPreference/EditTextPreference 打开时请求输入法）：按源端打开即弹键盘
- [首屏输入框按源端平台缺省获焦时，在窗口获焦后再 requestFocus：冷启动窗口激活晚于首屏查询，提前请求不会拉起输入法](lesson-9d42548ee3c075de3330.lesson.md)
  - 时机：界面实现阶段，为首屏含输入框的页面落实冷启动初始焦点与软键盘时
  - 情境：源端靠平台缺省给第一个可获焦的 EditText 焦点并自动弹键盘（源码没有 requestFocus/showSoftInput），获焦条件随数据分支变化（如列表为空时）；目标为 NavDestination 页 + TextInput，ArkUI 不会自动给输入框焦点。
