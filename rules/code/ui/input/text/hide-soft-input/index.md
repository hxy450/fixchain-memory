# InputMethodManager 收起软键盘

agent 会看到什么：读到源端 InputMethodManager.hideSoftInputFromWindow / showSoftInput 只收或弹键盘、不改焦点；产物里 inputMethodController 的 hideSoftKeyboard / stopInputSession / hideTextInput 调用、包着它的 try/catch，以及收键盘后 .onBlur 改写的焦点态

## 规矩

- rule-8358921aee44｜只收键盘时用 hideTextInput，不用 hideSoftKeyboard 或 stopInputSession｜读到：源端 InputMethodManager.hideSoftInputFromWindow(...) 只收键盘、不改焦点；规格写 inputMethodController（@kit.IMEKit）的方法名「实现期复核后钉死」；写错：鸿蒙端用 inputMethodController 的 showSoftKeyboard / hideSoftKeyboard 弹收键盘，或用 stopInputSession 收键盘
- rule-028877e2a47d｜收键盘的调用方依赖焦点态时，把收键盘引起的失焦排除在焦点变化之外｜读到：源端 hideSoftInputFromWindow 只收键盘、焦点不变，提交后工具栏仍按聚焦状态显示菜单；写错：提交时收键盘后 .onBlur 分支照常把焦点态置 false，工具栏退回非聚焦的菜单
