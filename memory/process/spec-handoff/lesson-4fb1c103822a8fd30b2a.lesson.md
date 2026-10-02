# Application 初始化链注册的广播接收器与系统监听要读本体写进规格：锚点、触发条件、承接方法与目标 API

ID：`lesson-4fb1c103822a8fd30b2a` · 版本：1

[本主题](index.md)

## 何时使用

规格提取阶段，把源端 Application 初始化链里注册的 BroadcastReceiver、系统回调与监听写入 feature 规格时；覆盖检查准备把被引用的文件归为平台胶水时；实现阶段逐项迁移初始化链时

## 适用情境

Android 源在 Application 初始化链注册接收器（如监听 CONNECTIVITY_ACTION 的网络切换），接收器本体按前后状态判断后调用业务检测或上报，并传入专用触发来源常量；上游契约已点名该接收器，但它不在 feature 锚点内；目标需用 @ohos.net.connection 等监听等价实现。

## 原因

隐式触发入口不在页面与 ViewModel 的调用链里：规格只写显式触发入口、常量取值域只写“各场景传对应值”时，实现者拿不到触发条件，常量留在代码里却没有调用方；覆盖检查只按引用计数把接收器归为胶水，也发现不了其中的业务调用。

## 做法

1. 对初始化链里的 register*Receiver 与监听注册，读接收器本体；含业务调用就作为锚点写入 feature，写明数据流、服务层承接方法、触发条件（例如注册时记下初始网络类型，只在蜂窝 → Wi‑Fi 时触发）与目标 API。
2. 为常量取值域写验收项时，逐个取值列出源端调用方和目标承接位置；某个取值没有承接方时写明迁移或裁剪决定。
3. 实现阶段验收项列出多个触发来源时逐个找到调用点；逐项迁移初始化链遇到注册调用，读被注册类后实现等价监听，或登记占位、决策，不静默略过。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-c234d95411230bdbffda](../../../store/cases/case-c234d95411230bdbffda/e3b3d43443778d8a128ba496cab8800cdbd7f3b8edc2f363eb8c78bf0537ecc3.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`e3b3d43443778d8a128ba496cab8800cdbd7f3b8edc2f363eb8c78bf0537ecc3`
