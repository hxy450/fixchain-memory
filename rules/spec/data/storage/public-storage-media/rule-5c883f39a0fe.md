# 源端写公共目录并做媒体扫描、目标改落沙箱时，规格那条链要写出导出步骤

审的是：规格
触发（任一种）：
- 读到：源码先查 WRITE_EXTERNAL_STORAGE、下载到外部存储公共目录（如 /sdcard/Download/…），成功后发 ACTION_MEDIA_SCANNER_SCAN_FILE；映射参考写「下载目录 → 沙箱 filesDir + picker 导出」；写错的样子：规格的下载链写成 request.agent 完成 → 提示成功 → 入库，数据流、服务接口和验收条目里都没有导出步骤
- 写错的样子：实现映射把媒体扫描标为「不迁移（picker 保存副本后系统媒体库自行可见）」，而这条链里没有 picker 步骤，导出只写在同功能的另一条链上
适用范围：规格提取时，源端产物落公共目录、目标端因权限改落应用沙箱的每条业务链路
做法：
- 逐条链路标注产物的用户可见性：源端写公共目录并做媒体扫描的，记为用户可见
- 用户可见的链改落沙箱时，在该链的数据流、服务接口和验收条目里写出导出步骤 DocumentViewPicker.save，并写明时点：导出成功后才提示成功并入库，取消时静默，写入失败提示重试
- 移除媒体扫描等平台调用时，替代理由引用的步骤（如「picker 保存后可见」）必须在同一条链里；一个决策覆盖多条链时逐链核对
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- ACTION_MEDIA_SCANNER_SCAN_FILE：请求媒体扫描器扫描文件并加入媒体库：源端发了它，说明产物要让用户在媒体库或文件里看得到（出处：android.content.Intent#ACTION_MEDIA_SCANNER_SCAN_FILE）
- request.agent 的 Config.saveas 只支持应用存储的 base 目录及其子目录：request.agent 下载的产物只落沙箱，用户看不到，要另有导出（出处：鸿蒙 SDK 的 ets/api/@ohos.request.d.ts，request.agent.Config.saveas）
- save(option?: DocumentSaveOptions): Promise<Array<string>>：拉起文档保存页，返回保存文件的 URI 数组（出处：鸿蒙 SDK 的 ets/api/@ohos.file.picker.d.ts，DocumentViewPicker.save）
未核实：卡里的修复出自 API 24（6.1.1），本机声明是 API 23
来源：1 张卡，1 个应用
- case-959edb6659d37f79f8d6（免费来电多多）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1、诊断；做法第 3 步 ← 建议 2
