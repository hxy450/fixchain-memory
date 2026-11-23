# 本地音频导入用 AudioViewPicker 并复制进沙箱；photoAccessHelper 只覆盖图片和视频，不作为音频来源

ID：`lesson-62ac5e65ac4aa51128bd` · 版本：2

[本主题](index.md)

## 何时使用

平台能力映射与实现阶段，为 Android MediaStore 本地音频扫描选择 HarmonyOS 读取方式与权限链时；编译修复遇到缺失的媒体类型枚举时

## 适用情境

源端申请 READ_EXTERNAL_STORAGE/READ_MEDIA_AUDIO 后查询 MediaStore.Audio 列出本地音频；目标受“不申请图片/视频媒体权限、优先 picker”约束，候选方案涉及 photoAccessHelper(MediaLibraryKit)、READ_AUDIO 与 AudioViewPicker。

## 例外与边界

- 换成 AudioViewPicker 后要保留源端一次拿到多首音频的能力：AudioSelectOptions.maxSelectNumber 不设时只能选 1 首，要按需设大（上限 500）；select 返回的 URI 只有临时只读权限、应用退到后台就失效，复制进沙箱要在拿到结果后立即完成，不只保存 URI

## 原因

photoAccessHelper 的资源类型只有图片和视频（PhotoType 没有 AUDIO），“媒体库查询音频 + 音频权限门”在目标上不成立；规格把它写成确定映射后，实现者可能自拟不存在的枚举，编译修复再删掉约束换取通过，整条链最终静默为空（权限未声明时申请恒被拒绝，界面表现为点击无响应）。

## 做法

1. 映射本地音频扫描时先核目标媒体库 API 覆盖哪些资源类型、需要什么权限；在禁申图片/视频权限的约束下，写成 AudioViewPicker 选择导入并复制进应用沙箱（持久可播），列表扫描沙箱目录；确认不了就登记待决，不写成确定映射。
2. 规格指定的 API 与参考或 SDK 声明对不上时，不自拟枚举成员，把“目标平台没有此能力”作为规格问题回报；编译修复遇到缺失枚举说明能力缺失时，不删约束换取编译通过，标明该功能链不可达。
3. 实现权限门时核对所申请的权限正是后续 API 需要的权限；module.json5 的声明变动后，复核所有 requestPermissions 调用点。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-1607d055621c41c4c087](../../../store/cases/case-1607d055621c41c4c087/749b041f8fc4fe0cbf6a7d45c8b653dd0dd049028fdeeb48d6d466ee3164e85f.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`749b041f8fc4fe0cbf6a7d45c8b653dd0dd049028fdeeb48d6d466ee3164e85f`
