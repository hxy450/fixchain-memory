# TextInput 的获焦回调

agent 会看到什么：读到源端 BasicTextField 的 Modifier.onFocusChanged 写业务 focused 状态；产物里 TextInput.onFocus 无条件把 true 上抛进业务状态，没有 enableKeyboardOnFocus(false) 和 onTouch 的来源判别

## 规矩

- rule-377d006152ce｜常驻 NavBar 的页面里，TextInput.onFocus 先判别是否用户触发再写业务状态｜读到：源端 BasicTextField 的 Modifier.onFocusChanged 写业务 focused，状态用 remember 持有；写错：目标 TextInput 写 .onFocus(() => 回调(true)) 无条件上抛、写进业务 focused，没有 enableKeyboardOnFocus(false) 和 onTouch 的来源判别
