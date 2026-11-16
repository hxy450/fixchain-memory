# 软键盘避让模式

agent 会看到什么：源 Manifest 的 android:windowSoftInputMode（写了 adjustResize，或没写、布局里有 EditText 和可滚动列表）；产物里有没有 setKeyboardAvoidMode、设在 EntryAbility 还是页面的显示和隐藏回调里

## 规矩

- rule-8b5de43c90ba｜源页声明 adjustResize 时，页面显示时设 KeyboardAvoidMode.RESIZE、隐藏时还原｜读到：Manifest 里 android:windowSoftInputMode="adjustResize"，编辑页用 Modifier.imePadding()；写错：页面没调 setKeyboardAvoidMode，注释写「键盘避让由系统默认行为承担」或报告写「取系统默认 OFFSET 行为」
- rule-3664b1fcf73e｜源端实际是 adjustResize 时，在 loadContent 回调里显式设 RESIZE 避让｜读到：规格的软键盘条目只写「默认」；源 manifest 无 windowSoftInputMode，布局含 EditText 和 ListView / ScrollView（或继承 ListActivity）；写错：EntryAbility 的 windowStage.loadContent 回调里没有 setKeyboardAvoidMode，窗口沿用缺省 KeyboardAvoidMode.OFFSET 整页上推
