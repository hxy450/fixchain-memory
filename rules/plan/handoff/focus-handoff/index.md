# 移交来的焦点获取项

agent 会看到什么：移交登记写「焦点获取细节归 Slice N」，接手方报告记为完成，而 .onKeyEvent 仍挂在原子组件上、没有获焦代码

## 规矩

- rule-4b2bbc9be125｜接手「焦点获取归本片」这类移交时，改挂页面根或落地获焦代码，只改返回值不算完成｜读到：转换报告或移交登记写「焦点获取细节归 Slice N」，规格写「onKeyDown → 页面 onKeyEvent」；写错：接手方报告把这项记为完成，但 .onKeyEvent 仍挂在原子组件上、没有获焦代码，只把回调改成返回 boolean 或加了 KeyType.Down 守卫
