# EditText 的 imeOptions 和软键盘回车键

agent 会看到什么：读到一组单行 EditText（singleLine、inputType=textPassword 等）写了或没写 android:imeOptions；产物里各 TextInput 的 .enterKeyType(...)、回车后的 onSubmit 和焦点移动

## 规矩

- rule-e325fb5285f2｜单行 EditText 没写 imeOptions 时，TextInput 写 EnterKeyType.Next 链｜读到：源端一组单行 EditText（singleLine 或 inputType=textPassword 等），没写 android:imeOptions；写错：目标各 TextInput 都没写 .enterKeyType(...)，软键盘回车全是默认 Done
