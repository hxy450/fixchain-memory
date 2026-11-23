# 本地音频导入用 AudioViewPicker 并复制进沙箱；photoAccessHelper 只覆盖图片和视频，不作为音频来源

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

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1 步〕PhotoAccessHelper.getAssets 声明的 @permission 是 ohos.permission.READ_IMAGEVIDEO，缺权限时报 201 Permission denied
- 〔适用情境 / 做法第 1 步〕ohos.permission.READ_AUDIO 的权限级别是 system_basic，列在受限开放权限里，普通应用要通过 ACL 跨级申请
- 〔做法第 1 步〕通过 Picker 访问文件时由系统应用引导用户操作，接口本身无需申请权限
- 〔做法第 1 步〕AudioViewPicker.select 返回的 URI 只有临时只读权限，应用退出到后台后失效
- 〔做法第 1 步〕AudioSelectOptions.maxSelectNumber 没设时为 1，取值范围 1 到 500（API 12 起）
- 〔做法第 1 步〕AVMetadataExtractor 取元数据前必须先通过 fdSrc 或 dataSrc 设置数据源
- 〔原因 / 做法第 3 步〕申请 user_grant 权限时要先在配置文件声明，再在运行时调动态申请接口由用户在系统弹框中授权
- 〔原因 / 做法第 3 步〕requestPermissionsFromUser 的 authResults 里 0 已授予、-1 未授予、2 请求无效；errorReasons（API 18 起）里 2 表示申请的权限没有声明
