# EntryAbility 里依赖 UIContext 的步骤放进 loadContent 成功回调，之前调 getUIContext 抛 1300002

ID：`lesson-63fe5e10a98fe3cd3f5d` · 版本：2

[本主题](index.md)

## 何时使用

入口实现阶段，在 EntryAbility.onWindowStageCreate 中安排依赖 UIContext 的步骤（getUIContext、px2vp 换算避让区、setKeyboardAvoidMode 等）相对 loadContent 的时机时；改动 EntryAbility 生命周期后自检时

## 适用情境

目标在 EntryAbility 里做窗口全屏、系统栏或键盘避让设置，并测量避让区换算成 vp 写入共享窗口模型；这些步骤写在 onWindowStageCreate 中、位于 windowStage.loadContent 调用之前，或在其回调之外同步执行；模板只说“窗口设置放在 onWindowStageCreate”，没写与 loadContent 的先后。

## 原因

UIContent 只在 loadContent 成功后建立，之前调用 mainWindow.getUIContext() 会抛 1300002（@ohos.window.d.ts：This window state is abnormal），冷启动即闪退；d.ts 签名只说明成员存在，不说明此刻可调用，不运行应用的编译门也发现不了。

## 做法

1. 凡依赖 UIContext 的步骤放进 windowStage.loadContent 的成功回调（err.code 为 0 之后）；loadContent 之前只做不依赖 UIContent 的窗口调用。
2. 核对 SDK 调用时，除成员签名外读该 API 的注释与 @throws；已推出“此时可能还没有 UIContext”这类时序疑点时，以文档或模板的回调顺序消解，不以成员存在推定此刻可调用。

## 可选检查

- 改动 EntryAbility 生命周期后静态核对：onWindowStageCreate 中位于 loadContent 之前或其回调之外同步执行的代码不调用 getUIContext、不依赖 UIContent。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-6817a796af2e744ddf8a](../../../store/cases/case-6817a796af2e744ddf8a/df87ceea0b7873522ff4397241c86a2adcda39f491e73a41e0450b00543fb4af.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`df87ceea0b7873522ff4397241c86a2adcda39f491e73a41e0450b00543fb4af`
