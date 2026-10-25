# 保存媒体到相册或文件：缺写入权限时用 showAssetsCreationDialog，picker 返回的 URI 先 openSync 取 fd

ID：`lesson-0ce9fe04eb82e77d219f` · 版本：3

[本主题](index.md)

## 何时使用

系统能力与媒体功能实现阶段，编写下载到缓存、保存到相册或文件、复制到剪贴板的调用代码时

## 适用情境

源端用 OkHttp 下载、MediaStore 入库、SAF CreateDocument 存 Downloads、FileProvider URI 复制；目标改用 request.agent、photoAccessHelper、DocumentViewPicker 与 pasteboard，实现者依据参考模板片段或规格映射落码。

## 例外与边界

- 保存的是相机会话刚拍摄的照片或录像：走相机系统资产路线（photoAssetAvailable + saveCameraPhoto、AVRecorder AUTO_CREATE_CAMERA_SCENE），不逐张弹授权框，也不用 createAsset 系列

## 原因

这些 API 的必要步骤与权限不在调用外形上：createAssetRequest 需要 WRITE_IMAGEVIDEO，它是受限开放权限，未声明或未获签名配置中的受限权限授权时写入必失败（返回 201），只在 module.json5 声明并运行时申请不够；picker 返回的是 URI，而 copyFileSync 的目标参数要路径或 fd；request.agent 建任务后不 start 永不完成；应用沙箱 file URI 放进剪贴板，其他应用读不到。只读到模板前半段时，缺的正好是这些步骤。

## 做法

1. 调媒体库写入前，把参考列出的权限与 module.json5、运行时申请逐项对照；WRITE_IMAGEVIDEO 是受限开放权限，除声明与运行时申请外还需签名配置中的受限权限授权（已观察 HarmonyOS API 24 环境下无此授权时写入返回 201），工程没有该授权时用 photoAccessHelper.showAssetsCreationDialog，对返回的媒体库 URI 用 openSync 取 fd 写入，用户拒绝时给出拒绝提示。
2. DocumentViewPicker 或媒体库返回 URI 时，先 fileIo.openSync(uri) 取 fd，再 copyFileSync(源路径, fd)；不把 URI 当路径传入。
3. request.agent 下载按 create → on(completed/failed) → task.start() 的完整生命周期落码，写完核对确有 start()。
4. 图片复制到剪贴板写接收方可读的数据（如 PixelMap），不写应用沙箱 file URI；目标没有系统“已复制”提示时补成功提示。

来源支持：2 张卡 · 已知 1 次迁移（部分未记录） · 已知 1 个应用（部分未记录）

## 来源（按需复核）

- [case-149fd657e7134bf86261](../../../store/cases/case-149fd657e7134bf86261/76fbb9c3cf5c8c90f368c676283ddd9f80585443f0d66eee63ccee0b2aaaf3b2.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`76fbb9c3cf5c8c90f368c676283ddd9f80585443f0d66eee63ccee0b2aaaf3b2`
- [case-58c3f872e3c907fb4b68](../../../store/cases/case-58c3f872e3c907fb4b68/8f81496786965152a90c44e6cfca277833ac24fc4296e7268a881109215d0a36.json) · 结论：recommendation:3, recommendation:4
  卡片版本：`8f81496786965152a90c44e6cfca277833ac24fc4296e7268a881109215d0a36`
