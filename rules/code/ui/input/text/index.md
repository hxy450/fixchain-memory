# 输入框与软键盘

源端有 EditText、SearchView、Compose TextField、android:inputType / maxLength / textCursorDrawable、windowSoftInputMode，目标端有 TextInput、TextArea、Search、caretColor、inputFilter、获焦和键盘避让时

## 触发族

- [EditText 的光标（textCursorDrawable）](edittext-cursor/index.md)（4 条）：读过的布局里 EditText 写了或没写 android:textCursorDrawable，光标来自 shape drawable 或所在 Activity 的主题；交回的 TextInput 上 .caretColor / .caretStyle 是照抄别处的、凭记忆的，或写成了不存在的 caretWidth
- [EditText 的背景与 TextInput 默认带出的外观](edittext-background/index.md)（8 条）：读过的布局里 EditText 或 Spinner 没写 android:background、padding、高度（外观来自主题），或用 @null 去掉了默认装饰、没有密码显隐切换；交回的 TextInput / Select 带着 ArkUI 默认的填充底、圆角、内边距、高度、清除按钮或显隐图标，或写成凭记忆的静态下边框
- [定长格子密码框（EditText 子类叠掩码格）](grid-password-input/index.md)（3 条）：读过的源码里格子式密码输入控件是 EditText 子类，写死 dp 宽高、带 maxLength、focusableInTouchMode，输满即在 OnTextChangeListener 里比对；交回的透明 TextInput 没设尺寸、被 HitTestMode.None 的掩码层挡住点不到，或改成了确定按钮提交
- [EditText 的 maxLength 与程序写入（setText、TextWatcher）](edittext-length-settext/index.md)（3 条）：读过的源码里只有某个 EditText 声明了 android:maxLength，或程序用 setText 回填、载入后才 addTextChangedListener；交回的几个 TextInput 一并写了同一个 .maxLength、回填没按 maxLength 截断，或 onChange 把载入回显算成修改
- [EditText 的 inputType 和输入过滤](edittext-input-type-filter/index.md)（8 条）：读到 EditText / EditTextPreference 的 android:inputType（textCapCharacters、textNoSuggestions、number）、android:numeric、android:digits 或 setFilters / InputFilter.AllCaps；产物里 TextInput / TextArea 的 type、autoCapitalizationMode、enablePreviewText、inputFilter、聚焦和大写转换
- [SearchView 迁成 Search](search-view/index.md)（5 条）：源端的 SearchView（工具栏菜单里的 actionView、OnQueryTextListener.onQueryTextSubmit 里发起查询和改界面状态），对应目标 Search 组件的外观、onSubmit 和提交后才出现的界面状态
- [软键盘避让模式](keyboard-avoid-mode/index.md)（2 条）：源 Manifest 的 android:windowSoftInputMode（写了 adjustResize，或没写、布局里有 EditText 和可滚动列表）；产物里有没有 setKeyboardAvoidMode、设在 EntryAbility 还是页面的显示和隐藏回调里
- [输入框的获焦和弹键盘](input-focus/index.md)（6 条）：源端 EditText 在首屏或 Dialog 弹出时获焦弹键盘；产物里 TextInput 的 defaultFocus / requestFocus、条件挂载的输入浮层和分段输入的节点
- [Compose 的输入框和开关控件](compose-textfield-switch/index.md)（8 条）：读到 Compose 的 TextField / OutlinedTextField / BasicTextField(value, onValueChange) 或 Switch(checked, onCheckedChange)；产物里对应的 TextInput、Toggle 及其 onChange、$$ 绑定和样式
- [EditText 输入值的取用](edittext-input-value/index.md)（2 条）：读到源端各执行方法从本组 EditText 的 getText().toString() 原文取值去校验和传参，产物里是 TextInput 的 @State 表单字段、请求 interface 的字段和校验前的 trim / toLowerCase
- [TextInput 的获焦回调](textinput-focus/index.md)（1 条）：读到源端 BasicTextField 的 Modifier.onFocusChanged 写业务 focused 状态；产物里 TextInput.onFocus 无条件把 true 上抛进业务状态，没有 enableKeyboardOnFocus(false) 和 onTouch 的来源判别
- [InputMethodManager 收起软键盘](hide-soft-input/index.md)（2 条）：读到源端 InputMethodManager.hideSoftInputFromWindow / showSoftInput 只收或弹键盘、不改焦点；产物里 inputMethodController 的 hideSoftKeyboard / stopInputSession / hideTextInput 调用、包着它的 try/catch，以及收键盘后 .onBlur 改写的焦点态
- [EditText 的 imeOptions 和软键盘回车键](edittext-ime-options/index.md)（1 条）：读到一组单行 EditText（singleLine、inputType=textPassword 等）写了或没写 android:imeOptions；产物里各 TextInput 的 .enterKeyType(...)、回车后的 onSubmit 和焦点移动
- [EditText.setError 的字段错误提示](edittext-set-error/index.md)（1 条）：读到源码校验时对 EditText 调 setError(...)；产物里 TextInput 下面条件渲染的红字 Text、.showError(...)，或尾部错误图标加浮层气泡、改字即清的写法
- [多行 EditText 的最小行数和高度（minLines）](edittext-min-lines/index.md)（1 条）：读到 EditText 带 android:minLines、没写 android:gravity；产物里 TextArea 的 minHeight 怎么算、lineHeight 带不带单位、内容不足时文字的竖直对齐
- [setText 预填的输入框的光标位置](prefill-caret/index.md)（1 条）：读到源端（如 onCreateDialog 里）对 EditText 调 setText(...) 预填、光标在开头；产物里 TextInput({ text }) / TextArea({ text }) 有没有 controller 和首次 onFocus 时的 caretPosition(0)
