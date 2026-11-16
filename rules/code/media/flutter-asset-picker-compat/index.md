# Flutter 选图插件的兼容层（AssetPicker.pickAssets / AssetEntity）

agent 会看到什么：读到 Flutter 业务调 wechat_assets_picker 的 AssetPicker.pickAssets、拿 AssetEntity 的宽高和原图做处理，产物里是 OHOS 下替代插件的本地兼容层（走系统选择器、填 AssetEntity 宽高、交出前缩放）

## 规矩

- rule-b1723bf8481a｜选图插件要 READ_IMAGEVIDEO 而应用是普通签名时，在本地兼容包里改走系统选择器｜读到：原生插件的 OHOS 实现走 `photoAccessHelper` 读媒体库，默认申请 `ohos.permission.READ_IMAGEVIDEO` / `ohos.permission.WRITE_IMAGEVIDEO`；写错：选图入口仍走插件的媒体库实现（上层选图包保持托管版本、直接调原生插件），`Platform.isOhos` 下没有改走系统选择器的分支
- rule-5670df0f5266｜冻结业务在 UI isolate 同步处理所选原图时，选图兼容层先按业务上限原生预缩放再交出｜读到：冻结的 Dart 业务对 AssetPicker.pickAssets 选出的图用 package:image 的 decodeImage / copyResize / encodePng 在 UI isolate 同步处理，并有长边上限；写错：兼容层把系统选择器返回的缓存原图按原分辨率直接包装成 AssetEntity 交给业务，并称业务压缩调用不需要改
- rule-91ae01efcba3｜兼容层给 AssetEntity 填宽高时从文件头读，不用 instantiateImageCodec 整图解码｜读到：源 AssetEntity 带 width / height；写错：兼容层用 ui.instantiateImageCodec 对选中的原图整图解码，只为取宽高
- rule-5adea30bbbe8｜选图兼容层为提速去掉解码时，AssetEntity 宽高不写 0，改读文件头尺寸并给非零兜底｜读到：被替代的选图插件（wechat_assets_picker 的 AssetPicker.pickAssets）返回 AssetEntity，兼容层原先用 ui.instantiateImageCodec 解码出宽高再传给 AssetEntity，类注释写明保持既有调用方期望的公开 API；写错：兼容层构造 AssetEntity 时 width / height 写成字面量 0 或别的占位，注释说不必为读尺寸解码原图
