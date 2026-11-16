# 声明没写先后的平台回调

agent 会看到什么：@ohos.xml 等声明里没写先后、也没保证返回值的回调（attributeWithTagCallbackFunction 与 START_TAG、getNamespace()）；源码笔记里对这类不确定项的说法

## 规矩

- rule-c1c116ec3878｜源码笔记遇到声明没写先后的平台回调时，写成待验证项，不写「两种顺序行为一致」｜读到：@ohos.xml 声明没写 attributeWithTagCallbackFunction 与 START_TAG token 的先后，也没保证 getNamespace() 给出元素 URI；写错：源码理解笔记把不确定项写成「START_TAG 时快照并清空——两种顺序下行为一致」，或写成「每个元素自报 uri，可直接取 getNamespace()」
- rule-7d91d8af242c｜两端异步终态没核实时，笔记和注释不写「同语义」，记进 decision_gaps｜读到：源端 await 平台插件调用后才给成功/失败提示，目标 API 的 Promise 和完成事件分开（如 show() 与 on('shareCompleted')）；写错：源码理解笔记（source-notes）或代码注释写「与源同语义」「与源同序」，但取消时 resolve 还是 reject 没有出处；信封的 decision_gaps 为 []，不确定项里也没有这个疑点
