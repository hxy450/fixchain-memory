# 源端 textAllCaps（含 Button 与 AlertDialog 按钮样式默认的全大写）必须显示为全大写，按资源原样不是可接受的降级：取资源字符串后按当前 locale toLocaleUpperCase（Resource 参数先 getStringSync），封装成共享 allCaps 复用；textCase(UpperCase) 只转拉丁字母，不用它代替

ID：`lesson-cce58a1538fedfda3695` · 版本：3 · 阶段：execute/repair · 主题：[ui/text/formatting](index.md)

概要：textAllCaps 按 locale 大写

信号：`textAllCaps`, `AllCapsTransformationMethod`, `toLocaleUpperCase`, `textCase`, `TextCase.UpperCase`, `getStringSync`, `RangeError`, `ResourceStr`

## 何时使用

界面实现或返修阶段，把安卓 textAllCaps（含按钮样式默认的全大写）移植为 ArkUI 文本，确定取字符串方式与 locale 标签，或给多个页面的按钮统一做大小写变换时

## 适用情境

安卓按钮或文本靠 textAllCaps（AllCapsTransformationMethod 按当前 locale 大写）显示全大写，资源串多为首字母大写（Yes/No、New Game）；应用带含非 ASCII 或非拉丁字母的多语言资源（de 的 ü、tr 的 i/İ、ru 的西里尔字母），也可能以只有语言码的应用偏好语言运行；目标按钮参数常是 Resource/ResourceStr，要自己取字符串做大写，并把 resourceManager 配置的 locale（下划线分隔、子标签可能为空，如 fa_Arab_）转成 BCP 47 标签。也包括工程里已有按 locale 大写的私有实现，其他页面又用 textCase 另写一套。

## 原因

来源观察到 ArkUI textCase(TextCase.UpperCase) 没有把 ü 与西里尔字母转成大写，与安卓按 locale 的大写不一致；但这只说明 textCase 不准，不是保留资源原样的理由——另一来源中写者因参数是 ResourceStr、textCase 又被禁止，就放弃了大写。改用 toLocaleUpperCase 后，直接传资源 locale 会抛 RangeError；按单个样本（en_Latn_US）把下划线换成连字符，又会在子标签为空的 locale 下生成非法标签而崩溃。同一工程两套做法并存、只按英文截图验收时，非拉丁语言下的差异会漏掉。

## 做法

1. 按钮或文本参数是 Resource/ResourceStr 时，先经 resourceManager.getStringSync（或 UIContext 宿主 context 的资源管理器）取字符串，再调用 toLocaleUpperCase(tag)，与 AllCapsTransformationMethod 的 toUpperCase(locale) 对齐；封装为共享 allCaps(ctx, text)，语言切换后重算。写跨页文字变换前先 grep 工程已有实现并复用，不另写一套。
2. tag 由资源配置 locale 按 '_' 拆分、丢弃空子标签、再用 '-' 连接；结果为空或调用抛 RangeError 时回落到不带 locale 的 toUpperCase()。

## 可选检查

- 写完后在一种含非 ASCII 字母的资源语言（如 de）、一种非拉丁资源语言（如 ru）与只有语言码的应用偏好语言（如 fa）下各看一次显示，并确认 faultlog 没有新增 jscrash。

来源支持：3 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-4f8a6d24236bd7f92a26](../../../../../store/cases/case-4f8a6d24236bd7f92a26/0e161e85250788166615ae93e3d2c5982d20b63beb412376e211dc6e437feab9.json) · 结论：diagnosis, rec-b66d29790e, rec-fa8637e8c9, rec-6625e3494f, rec-238f17f4c4
  卡片版本：`0e161e85250788166615ae93e3d2c5982d20b63beb412376e211dc6e437feab9`
- [case-641f7da5b5891df89eeb](../../../../../store/cases/case-641f7da5b5891df89eeb/16f46e4f6f215fb2f10e2b7ff5dd6a307552a7daa531cc0d24311d7c8b29b4f0.json) · 结论：diagnosis, rec-b75fcadad7
  卡片版本：`16f46e4f6f215fb2f10e2b7ff5dd6a307552a7daa531cc0d24311d7c8b29b4f0`
- [case-742668c1933f26d6bff9](../../../../../store/cases/case-742668c1933f26d6bff9/eca4846a209c5b252e8c9753aec3c082e8c9307a63e21d016219fcc4eecb4c96.json) · 结论：diagnosis, rec-0bbedff97a, rec-099d8d96ae
  卡片版本：`eca4846a209c5b252e8c9753aec3c082e8c9307a63e21d016219fcc4eecb4c96`
