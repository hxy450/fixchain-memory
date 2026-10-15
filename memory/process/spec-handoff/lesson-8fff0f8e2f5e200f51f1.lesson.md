# Activity 的 screenOrientation（含未声明）要写成鸿蒙方向配置，不只写“横竖屏双布局”

ID：`lesson-8fff0f8e2f5e200f51f1` · 版本：1

[本主题](index.md)

## 何时使用

规格提取与工程配置阶段，为每个 Activity 确定窗口方向、在决策账本写“横竖屏”结论，或落 module.json5 的 abilities 配置时

## 适用情境

源各 activity 未声明 android:screenOrientation（安卓缺省随传感器与系统自动旋转开关旋转），并提供 layout-land/values-land 等横屏资源；或某 activity 在 manifest 声明锁定方向（如 sensorLandscape），Java 源码只见全屏标志。目标 EntryAbility 来自工程模板，module.json5 的 abilities 没有 orientation，页面已按 mediaquery 或 onConfigurationUpdate 写了横竖两套布局。

## 例外与边界

- 源码运行时调用 setRequestedOrientation 覆盖 manifest：以代码设置为准

## 原因

鸿蒙 EntryAbility 不写 orientation 就不随传感器旋转，只迁两套布局时横屏分支永不出现；锁定方向只声明在 manifest，规格与页面元数据又没有方向字段时，实现者会以“规格未覆盖”跳过。

## 做法

1. 逐个 activity 读 screenOrientation 与代码中的 setRequestedOrientation；未声明（随系统旋转）时在 module.json5 的 EntryAbility 写 orientation: auto_rotation_restricted（受系统旋转锁控制；取值见 SDK toolchains/modulecheck/module.json 的 orientation 枚举），与权限并列列为 module.json5 必做项。
2. 声明锁定方向的页写成“进入页 window.setPreferredOrientation(对应方向，如 sensorLandscape 对应 @ohos.window.d.ts 的 Orientation.AUTO_ROTATION_LANDSCAPE)、离开恢复”的验收条目。
3. 落 module.json5 时读全 abilities 段，对照决策账本的方向结论核对 orientation；页面实现了横屏分支而 abilities 没有 orientation 时，登记为缺口交回主流程。

## 可选检查

- 解除旋转锁并转 90°，窗口宽高互换、横屏分支出现。

来源支持：3 张卡 · 3 次迁移 · 3 个应用

## 来源（按需复核）

- [case-5e35bb283520acf3bd35](../../../store/cases/case-5e35bb283520acf3bd35/954c420a6eb53234d9a40e9851863e13e6a2b9e3e2195abc6f71fcfe048dcf4f.json) · 结论：recommendation:1
  卡片版本：`954c420a6eb53234d9a40e9851863e13e6a2b9e3e2195abc6f71fcfe048dcf4f`
- [case-c6c056189eaa36176e28](../../../store/cases/case-c6c056189eaa36176e28/2cb68533b47b0adbcc44f6714eab0ed4eee48b603073820527988ebacca82229.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`2cb68533b47b0adbcc44f6714eab0ed4eee48b603073820527988ebacca82229`
- [case-cc22f6cc1041c8cc1129](../../../store/cases/case-cc22f6cc1041c8cc1129/ec6e60182fe19865967b7c173312ac2be6c4dbf45c87407c6da85b673b5778f3.json) · 结论：recommendation:4
  卡片版本：`ec6e60182fe19865967b7c173312ac2be6c4dbf45c87407c6da85b673b5778f3`
