# 孤儿检测报 NO_IMPORTER 的页面和弹窗

agent 会看到什么：读到孤儿检测对 dialogs/ 或 pages/ 下的组件报 NO_IMPORTER，而规格写了它的 ArkTS output、ui-manifest 记为 verified 或 feature-index 列为范围内页面；产物里收口补丁 Delete File 删了这个 .ets，或给它补了源码里没有的调用方

## 规矩

- rule-44bd9013dace｜孤儿检测报无调用方的弹窗或页面已在规格和清单里登记时，保留文件、上报缺的触发点，不删｜读到：孤儿检测对 dialogs/ 或 pages/ 下的组件报 `NO_IMPORTER`，而页面规格写了它的 ArkTS output、ui-manifest 记为 verified 或 feature-index 列为范围内页面；写错：收口补丁 `Delete File` 删了这个 .ets（回执只写 Removed …），或给它补了源码里不存在的调用方（伪接线）
