# 选出的图要写进持久配置时，先复制到 filesDir 校验非空，再存 file:// 路径

审的是：代码
触发（任一种）：
- 写错的样子：目标把 PhotoViewPicker 返回的 photoUris[0]，或者落在 cacheDir 下的中间副本路径，直接写进会保存、之后重新读取的配置
适用范围：从选择器或选择页拿到的图片要写进会保存、之后反复读取的配置（如背景图）时
做法：
- 先把选择结果复制到 context.filesDir 下的应用目录，复制后校验目标文件非空（statSync(目标).size > 0），再用 fileUri.getUriFromPath(目标) 得到 file:// 路径写进配置
- 不保存 Picker 返回的临时授权 URI，也不保存 cacheDir 里的中间副本
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- photoUris: Array<string>，只能凭临时授权用 photoAccessHelper.getAssets 访问：Picker 返回的是临时授权的媒体 URI（出处：鸿蒙 SDK 的 ets/api/@ohos.file.photoAccessHelper.d.ts，PhotoSelectResult.photoUris）
- 临时授权在应用退出后或者设备重启后会清除：存下来的 Picker URI 下次启动读不到（出处：file-persistPermission.md，场景介绍）
- filesDir：默认长期保存的文件路径；cacheDir：超配额或系统空间不足时自动清理，不要存重要数据：持久配置引用的文件放 filesDir，不放 cacheDir（出处：app-sandbox-directory.md，应用文件目录与应用文件路径；鸿蒙 SDK 的 ets/api/application/Context.d.ts，Context.filesDir、Context.cacheDir）
- fileIo.openSync(uri, fileIo.OpenMode.READ_ONLY) 打开媒体 URI 得到 fd：读选择结果的方式（出处：photoAccessHelper-photoviewpicker.md，指定URI读取文件数据）
- copyFile(src: string | number, dest: string | number, mode?: number): Promise<void>：src 可以是路径或 fd，dest 是目标路径（出处：鸿蒙 SDK 的 ets/api/@ohos.file.fs.d.ts，copyFile）
- statSync(file: string | number): Stat，Stat.size 是字节数：复制后校验非空（出处：鸿蒙 SDK 的 ets/api/@ohos.file.fs.d.ts，statSync、Stat.size）
- getUriFromPath(path: string): string（@since 15）：沙箱路径转 file:// URI（出处：鸿蒙 SDK 的 ets/api/@ohos.file.fileuri.d.ts，fileUri.getUriFromPath）
- 复制到 filesDir 下的子目录并校验非空后再写配置的 url，真机回填正常：改法的效果；改前持久配置里存的只是缓存副本（出处：卡里修好并验证过）
未核实：文档说不能在 picker 回调里直接用返回的 uri 打开文件，卡里没写复制发生在哪一步
来源：1 张卡，1 个应用
- case-d465b188d96e33a7ffad（组件岛Widget Island）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2；取值 8 ← 诊断
