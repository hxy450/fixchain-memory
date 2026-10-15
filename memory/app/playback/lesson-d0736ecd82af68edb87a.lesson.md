# AVPlayer 错误只经一条通道上报，Promise 调用接 catch 并按状态表调用

ID：`lesson-d0736ecd82af68edb87a` · 版本：3

[本主题](index.md)

## 何时使用

播放服务实现阶段，映射 ExoPlayer 的单次 onPlayerError，并调用 AVPlayer 的 prepare/play/pause/stop/reset 时

## 适用情境

AVPlayer 同时有 on('error') 与 stateChange('error') 两条错误通道，控制方法返回 Promise；参考模板可能同时处理两条通道、prepare() 也不接 catch。

## 原因

两条通道各自上报会弹两个错误对话框；同步 try/catch 接不住 Promise 拒绝，未处理的拒绝会被全局错误处理记成崩溃；在不允许的状态调用会再次报错。

## 做法

1. 只用 on('error')（带具体原因）发错误事件，stateChange('error') 只做状态处理；按装载代数去重：同一次装载（及其实例）只上报一次，新的装载出现的故障照常上报。
2. Promise 调用都接 .catch，已由 on('error') 上报的拒绝不在 catch 里重复上报；设 url/fdSrc 前确保处于 idle（否则先 reset），stop 只在 prepared/playing/paused/completed 下调用。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-0b0bf6cdf94608e17cbb](../../../store/cases/case-0b0bf6cdf94608e17cbb/dd2e8bf60efdf5837f24bc9a7ed3431911662580e1b814ee514fb8c78df9d3e0.json) · 结论：recommendation:2, recommendation:3, diagnosis
  卡片版本：`dd2e8bf60efdf5837f24bc9a7ed3431911662580e1b814ee514fb8c78df9d3e0`
