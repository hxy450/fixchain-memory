# 保存媒体到相册或文件：缺写入权限时用 showAssetsCreationDialog，picker 返回的 URI 先 openSync 取 fd

## 何时使用

系统能力与媒体功能实现阶段，编写下载到缓存、保存到相册或文件、复制到剪贴板的调用代码时

## 适用情境

源端用 OkHttp 下载、MediaStore 入库、SAF CreateDocument 存 Downloads、FileProvider URI 复制；目标改用 request.agent、photoAccessHelper、DocumentViewPicker 与 pasteboard，实现者依据参考模板片段或规格映射落码。

## 例外与边界

- 保存的是相机会话刚拍摄的照片或录像：走相机系统资产路线（photoAssetAvailable + saveCameraPhoto、AVRecorder AUTO_CREATE_CAMERA_SCENE），不逐张弹授权框，也不用 createAsset 系列
- 保存由安全控件 SaveButton 的点击触发、在其回调里调 createImageAssetRequest / applyChanges 的：平台已按这次点击临时授权，不需要 WRITE_IMAGEVIDEO，这条写法照留，不改成 showAssetsCreationDialog；工程签名配置里已有受限权限授权、createAsset 能写入的，同样不必换

## 原因

这些 API 的必要步骤与权限不在调用外形上：createAssetRequest 需要 WRITE_IMAGEVIDEO，它是受限开放权限，未声明或未获签名配置中的受限权限授权时写入必失败（返回 201），只在 module.json5 声明并运行时申请不够；picker 返回的是 URI，而 copyFileSync 的目标参数要路径或 fd；request.agent 建任务后不 start 永不完成；应用沙箱 file URI 放进剪贴板，其他应用读不到。只读到模板前半段时，缺的正好是这些步骤。

## 做法

1. 调媒体库写入前，把参考列出的权限与 module.json5、运行时申请逐项对照；WRITE_IMAGEVIDEO 是受限开放权限，除声明与运行时申请外还需签名配置中的受限权限授权（已观察 HarmonyOS API 24 环境下无此授权时写入返回 201），工程没有该授权时用 photoAccessHelper.showAssetsCreationDialog，对返回的媒体库 URI 用 openSync 取 fd 写入，用户拒绝时给出拒绝提示。
2. DocumentViewPicker 或媒体库返回 URI 时，先 fileIo.openSync(uri) 取 fd，再 copyFileSync(源路径, fd)；不把 URI 当路径传入。
3. request.agent 下载按 create → on(completed/failed) → task.start() 的完整生命周期落码，写完核对确有 start()。
4. 图片复制到剪贴板写接收方可读的数据（如 PixelMap），不写应用沙箱 file URI；目标没有系统“已复制”提示时补成功提示。

来源支持：2 张卡 · 已知 1 次迁移（部分未记录） · 已知 1 个应用（部分未记录）

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1 步〕PhotoAccessHelper.createAsset 与 applyChanges 都声明需要 ohos.permission.WRITE_IMAGEVIDEO，没有权限时抛 BusinessError 201
- 〔原因 / 做法第 1 步〕ohos.permission.WRITE_IMAGEVIDEO 是受限开放权限，权限级别 system_basic、授权方式 user_grant；normal 等级的应用要把 HarmonyAppProvision 配置里 bundle-info 的 apl 声明为 system_basic 及以上并重新签名，只在 module.json5 声明和运行时申请拿不到
- 〔原因 / 做法第 1 步〕HarmonyOS API 24 设备上，签名配置里没有受限权限授权时，用 createAsset 系列写入媒体库返回 201
- 〔做法第 1 步〕PhotoAccessHelper.showAssetsCreationDialog 自 API 12 起提供，声明不带 @permission，弹窗让用户授权保存，返回已授权给应用的媒体库文件 uri 列表；弹窗要显示应用名称，依赖 module.json5 abilities 里配置的 label 和 icon；传入沙箱路径的 uri 也能保存，但弹窗里没有预览
- 〔做法第 1 步〕官方示例对 showAssetsCreationDialog 返回的媒体库 uri 用 fileIo.open(uri, OpenMode.WRITE_ONLY) 打开后写入内容
- 〔做法第 1 步〕PhotoAccessHelper.createAssetWithShortTermPermission（API 12 起）创建资产并给应用短时授权，需要的是 ohos.permission.SHORT_TERM_WRITE_IMAGEVIDEO
- 〔做法第 1、2 步〕fileIo.openSync 的 mode 不写时为 OpenMode.READ_ONLY（0o0），写入要传 WRITE_ONLY（0o1）或 READ_WRITE（0o2）
- 〔原因 / 做法第 2 步〕fileIo.copyFileSync 的 src 是源文件路径或 FD，dest 是目标文件路径或已创建文件的 FD；mode 默认 0，也只支持 0
- 〔原因 / 做法第 3 步〕request.agent.create 只创建上传或下载任务并入队，任务要调 Task.start() 才启动；start 需要 ohos.permission.INTERNET，没有权限抛 201
