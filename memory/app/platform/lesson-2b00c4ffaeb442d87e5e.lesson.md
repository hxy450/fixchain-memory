# 接入 identifier.getOAID 时同批声明 APP_TRACKING_CONSENT 并在隐私同意后申请；全零串按未授权处理

ID：`lesson-2b00c4ffaeb442d87e5e` · 版本：1

[本主题](index.md)

## 何时使用

服务层实现阶段，把源端 OAID（MSA 或厂商通道）采集迁到鸿蒙 identifier.getOAID 时

## 适用情境

源端在隐私协议同意后静默采集 OAID，写缓存、上送归因接口并发布就绪事件；鸿蒙 getOAID 需要 user_grant 权限 ohos.permission.APP_TRACKING_CONSENT，未授权时返回全零串；Android 端没有对应的运行期授权。

## 原因

只换采集 API 而不声明、不申请权限，getOAID 恒返回全零串，归因静默失效；申请时机在源端没有对应行为，需要显式决定。来源中采集 worker 读 d.ts 后发现缺口，但 module.json5 不在其写域，只能记为决策缺口，后一轮才补。

## 做法

1. 在 module.json5 声明 ohos.permission.APP_TRACKING_CONSENT（reason 用各语言目录的 $string，usedScene 指向入口 Ability）；在隐私协议同意门之后 checkAccessToken/requestPermissionsFromUser，再调用 identifier.getOAID；申请不推迟启动门闩，超时兜底照常先行武装。
2. 把返回的全零串视为未授权：记日志并按源端语义继续，不当作有效标识；派工时把 module.json5 与字符串资源一并划入写域。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-5c6be3ec08184086fd79](../../../store/cases/case-5c6be3ec08184086fd79/c810aaf2a57238a08e8f5f345b00a2df05d06d9887d763dc1d4de5f56ff633f0.json) · 结论：diagnosis, recommendation:2
  卡片版本：`c810aaf2a57238a08e8f5f345b00a2df05d06d9887d763dc1d4de5f56ff633f0`
