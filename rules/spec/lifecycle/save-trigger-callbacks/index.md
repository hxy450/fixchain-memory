# 源 Activity 的存档触发回调

agent 会看到什么：读到源 Activity 只在 onPause、onBackPressed、onSaveInstanceState、标题栏 Up 里调 save()，onDestroy 不存档；规格的转换决策写「onHide / aboutToDisappear 等价钩子」，没写哪些回调不存档

## 规矩

- rule-f64347466cdf｜源端存档触发点按时机逐个对到目标回调，onDestroy 不存档就不写 aboutToDisappear｜读到：源 Activity 只在 onPause、onBackPressed、onSaveInstanceState 和标题栏 Up 里调 save()，没有覆写 onDestroy，或 onDestroy 里不存档；写错：规格的转换决策把存档触发写成「onHide / onBackPressed / aboutToDisappear 等价钩子」，onSaveInstanceState 被对到组件销毁回调；也没写源端哪些回调不存档
