# 服务卡片按实际宽高选布局：由 FormExtensionAbility 取尺寸下发，V1 卡片页的派生值写成普通方法

ID：`lesson-7ad5a7d149de5bcec7da` · 版本：1

[本主题](index.md)

## 何时使用

服务卡片实现阶段，卡片需要按实际宽高选择布局档位，或在 V1 @Entry 卡片页里由尺寸等状态派生布局值时

## 适用情境

源端 Glance AppWidget 用 SizeMode.Exact/LocalSize 按卡片实际宽高选布局（宽度断点、按高度显示标题栏等）；目标为 ArkTS 服务卡片（V1 卡片页 + FormExtensionAbility + form_config 离散规格），实现者准备在卡片页用通用尺寸事件取宽高，或只按 FormDimension 档位一档对一形态。

## 原因

卡片页可用的事件与组件受限：onAreaChange 等通用尺寸事件的 SDK 注释不带 @form，编译会拒绝；只按离散规格一档对一形态时，档位与源端宽度阈值不一定对应。来源中 V1 卡片页 struct 的 get 访问器在转译产物里不存在，运行时取到 undefined，卡片恒走默认分支（修复者查看编译产物确认，未在其他 SDK 版本复核）。

## 做法

1. onAddForm 后调用 formProvider.getFormRect(formId)，并实现 onSizeChanged(formId, newDimension, newRect)，把 vp 宽高经 formProvider.updateForm 写进卡片数据；卡片页用 @LocalStorageProp 读取，按源端阈值派生档位（来源 SDK 中 getFormRect 标注为 API 20）。
2. 离散规格只作兜底提示：按目标设备上该规格的实际 vp 宽度对照源阈值换算档位，冲突时上报，不强行一档对一形态。
3. V1 卡片页里由状态派生的值写成 build 内调用的普通方法，不写 struct getter。
4. 拿不准某个通用事件或组件能否用在卡片里时，查 SDK .d.ts 注释是否带 @form；本地 skill 检索无结论不等于可用。

## 可选检查

- 派生值是否生效有疑问时，查编译产物中该方法仍在，或在卡片加日志确认档位随尺寸变化。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-77c6596fcdf362f9e832](../../../store/cases/case-77c6596fcdf362f9e832/c81c56fb66d294cfd767c2c43e5bcfb480ef9cccbdcfc212d5d607410c13675a.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`c81c56fb66d294cfd767c2c43e5bcfb480ef9cccbdcfc212d5d607410c13675a`
