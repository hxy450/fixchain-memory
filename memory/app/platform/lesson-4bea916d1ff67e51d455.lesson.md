# 打开系统设置的显式 Want 包名随设备与系统版本变化：写前在目标设备核对，启动失败要可观察，不照抄参考里标“已验证”的值

ID：`lesson-4bea916d1ff67e51d455` · 版本：1

[本主题](index.md)

## 何时使用

系统能力实现阶段，为“打开系统设置/应用权限页”编写 startAbility 显式 Want（bundleName/abilityName）时；维护迁移 skill 参考中的系统应用包名时

## 适用情境

源端经 Settings.ACTION_* 一类 Intent 跳转系统设置（全部文件访问、应用详情等）；目标为 HarmonyOS NEXT 应用，需要以显式 Want 指定系统设置应用，规格与源码都不给目标包名，可查到的参考文档给出硬编码的厂商设置包名并标注已验证。

## 原因

系统设置应用的包名是与设备、系统版本相关的常量，参考里的“已验证”只对其当时的设备成立；startAbility 被拒后若只在 catch 里记日志，按钮在用户看来就是点了没反应。来源中实现者照抄参考中的 com.huawei.settings，HarmonyOS NEXT 真机上的设置应用为 com.huawei.hmos.settings，两个权限页的“打开设置”都失效，直到视觉验证才发现。

## 做法

1. 有设备时写前用 hdc shell bm dump -a 查找设置应用包名，再用 bm dump -n <包名> 取 Ability 名（来源 HarmonyOS NEXT 手机为 com.huawei.hmos.settings / com.huawei.hmos.settings.MainAbility）；生成期无法核对时，在交付报告或验证清单登记“打开设置需真机确认”。
2. startAbility 失败要让调用方可观察（返回结果或给用户提示），不只 hilog 后吞掉。
3. 维护参考文档时为系统应用包名注明验证时的系统版本与设备，HarmonyOS NEXT 与旧版 EMUI/HarmonyOS 分开写。

## 来源（按需复核）

- case-5aa1e2ae875c4bef3df1 · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`79cd1c853dee477a1bccffcc2cf69a629ae5e85fa6d0295db4ac62c31ef45d45`
