# 用 @Monitor 监听数组路径代替 collect 时，生产方按源端以新数组重新赋值发出变更

ID：`lesson-0cc7ae4eec0a59086202` · 版本：1

[本主题](index.md)

## 何时使用

状态模型与 ViewModel 实现阶段，把 StateFlow/Flow 的列表或消息队列迁成 @Trace 数组，并由消费方用 @Monitor 监听数组属性路径时

## 适用情境

源端以 StateFlow.update { list + item } 一类写法每次发射新列表；目标生产方准备原位 push（出队却重新赋值），消费方以 @Monitor('model.items') 一类路径模拟 collect。

## 原因

来源中原位 push 没有触发监听数组路径的 @Monitor，提示永远不出现，重新赋值的出队路径却正常；生产方写法与消费方观察方式不配套时 UI 静默失效。这一点依据修复者诊断与设备复测，未另查文档，不当作所有 API 版本的定律。

## 做法

1. 源端以新列表发射事件时，目标也重新赋值新数组（this.items = [...this.items, x]），入队和出队用同一种变更信号；不因 @Trace 数组原位 push 能刷新渲染就改成 push。
2. 消费方用 @Monitor 监听数组路径前先读生产方写法；生产方原位修改时，要求其改为重新赋值，或实测确认能触发。

## 可选检查

- 有疑问时触发一次入队，确认消费方回调确实执行、提示出现。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-5184da257133ebcc7073](../../../store/cases/case-5184da257133ebcc7073/fed0f7aa28d6ee296719c0490ea8a5ff6c8212ba348c192ba1d653410ad7b9a9.json) · 结论：diagnosis, recommendation:3, recommendation:4
  卡片版本：`fed0f7aa28d6ee296719c0490ea8a5ff6c8212ba348c192ba1d653410ad7b9a9`
