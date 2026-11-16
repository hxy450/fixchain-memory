# 透明主题的 Activity（windowIsTranslucent）

agent 会看到什么：读到源 Activity 的主题里 android:windowIsTranslucent 为 true、android:windowBackground 为 @android:color/transparent，并有 android:backgroundDimEnabled；产物里对应 NavDestination 的 .mode(...)、页背景是否透明，以及页内那层半透明遮罩

## 规矩

- rule-e65a8f69b211｜源 Activity 用透明主题时，NavDestination 设 DIALOG 模式和透明背景，遮罩只作页内一层｜读到：源 Activity 的主题里 `android:windowIsTranslucent` 为 true、`android:windowBackground` 为 `@android:color/transparent`，并有 `android:backgroundDimEnabled`；写错：目标 `NavDestination` 没设 `.mode(...)`（默认 STANDARD）、页背景不透明，只在页内铺一层半透明 `Stack` 遮罩，下层页面透不出来
