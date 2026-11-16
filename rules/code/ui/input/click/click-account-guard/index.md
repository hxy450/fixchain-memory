# 写操作点击前的账号就绪守卫

agent 会看到什么：读到 Compose 里投票、收藏、删除、发送等写操作的 onClick lambda 包在源端的账号就绪守卫函数里，或按钮组件收 account 参数、点击前先校验；产物里自写判定只 showToast 后 return，或回调直接调 ViewModel 写方法不加守卫

## 规矩

- rule-604c92456d82｜源端写操作包在账号就绪守卫里时，目标调用已移植的同名守卫，不用本地 Toast 判定代替｜读到：Compose 里写操作（投票、收藏、删除、屏蔽、发送）的 onClick lambda 包在源端的账号就绪守卫函数里，或按钮组件收 account 参数、点击前默认先校验；写错：目标自写判定，未就绪时只 showToast 后 return；或接线回调时直接调 ViewModel 写方法不加守卫；投票先改本地分数再上抛
