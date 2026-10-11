# textAllCaps 按当前 locale 做大写：取资源字符串后调用 toLocaleUpperCase，locale 标签按子标签解析并留回落，不用 textCase(UpperCase) 代替

ID：`lesson-cce58a1538fedfda3695` · 版本：1

[本主题](index.md)

## 何时使用

界面实现或返修阶段，把安卓 textAllCaps（含按钮样式默认的全大写）移植为 ArkUI 文本，并为大小写转换确定 locale 标签时

## 适用情境

安卓按钮或文本靠 textAllCaps（AllCapsTransformationMethod 按当前 locale 大写）显示全大写；应用带含非 ASCII 字母的多语言资源（如 de 的 ü、tr 的 i/İ、el 的重音），也可能以只有语言码的应用偏好语言运行；目标要自己取字符串做大写，并把 resourceManager 配置的 locale（下划线分隔、子标签可能为空，如 fa_Arab_）转成 BCP 47 标签。

## 原因

来源观察到 ArkUI textCase(TextCase.UpperCase) 没有把 ü 转成大写，与安卓按 locale 的大写不一致。改用 toLocaleUpperCase 后，直接传资源 locale 会抛 RangeError；按单个样本（en_Latn_US）把下划线换成连字符，又会在子标签为空的 locale 下生成非法标签而崩溃。

## 做法

1. 取资源字符串后调用 toLocaleUpperCase(tag)，与 AllCapsTransformationMethod 的 toUpperCase(locale) 对齐。
2. tag 由资源配置 locale 按 '_' 拆分、丢弃空子标签、再用 '-' 连接；结果为空或调用抛 RangeError 时回落到不带 locale 的 toUpperCase()。

## 可选检查

- 写完后在一种含非 ASCII 字母的资源语言（如 de）与只有语言码的应用偏好语言（如 fa）下各看一次显示，并确认 faultlog 没有新增 jscrash。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-4f8a6d24236bd7f92a26](../../../store/cases/case-4f8a6d24236bd7f92a26/0e161e85250788166615ae93e3d2c5982d20b63beb412376e211dc6e437feab9.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`0e161e85250788166615ae93e3d2c5982d20b63beb412376e211dc6e437feab9`
