# 源端推进后主动预取后续图片时，目标用 ImageSource 解码到有上限的缓存做真实预取，不以 Image 组件缓存替代

ID：`lesson-cde53c6eab199d1262b2` · 版本：4

[本主题](index.md)

## 何时使用

ViewModel 或页面逻辑迁移阶段，处理源端图片预加载、缓存预热等性能行为，决定实现、平台替代还是登记缺口时

## 适用情境

源端 ViewModel 在加载或每次推进后按规则挑出后续若干项（如跳过已处理、已跳过项和视频）并主动预取（如 Coil imageLoader.enqueue、Glide.preload），规格含对应的性能验收项；目标页面只用 Image 组件按需显示当前项，没有独立的预加载服务。

## 例外与边界

- 已有批准的决策放弃该性能行为，并在迁移报告或占位登记中留有记录

## 原因

Image 组件缓存只作用于已经渲染过的图片，源端预取的是尚未显示的后续项，两者不等价；在差异清单写“由组件承担”既没有实现，也没有留下可追踪的占位，缺口直到验收才暴露。

## 做法

1. 按源端规则在推进后选出后续 N 项（N 与跳过条件取当前源码）。按资源类型取可解码输入：image.createImageSource 接受本地路径、fd、ArrayBuffer 或 rawfile 描述符（@ohos.multimedia.image.d.ts），网络图片先下载为 ArrayBuffer，媒体库或 picker URI 先用 fileIo 打开取 fd；再 createPixelMap，放入以稳定 key（条目 ID 或原 URI）索引的内存缓存。
2. 缓存设上限，并写明回收：解码完成、不再使用的 ImageSource 调用 release()；缓存替换、淘汰或页面退出时，PixelMap 只在显示端和其他使用者都不再用、相关异步操作已完成后才 release()，仍交给 Image 显示的不随删除缓存键立即释放（OpenHarmony PixelMap 文档：释放前须完成该实例的全部异步操作，2026-10-15 访问；本机 @ohos.multimedia.image.d.ts：release 后访问内部数据的调用都会失败）。显式缓存要被显示端读取才起作用，已观察的修法没有记录显示端如何消费：显示时按 key 先取缓存的 PixelMap 交给 Image、未命中再按原 uri 加载，并在交付说明写明这一接法未经验证。
3. 写“无对等 API”前先查当前 SDK 的图片解码与缩略图接口；确实不能实现时按工程约定登记占位或决策，让对应验收项仍能被追踪，不只写在差异清单里。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-d9fc3c9129fee3f38c91](../../../store/cases/case-d9fc3c9129fee3f38c91/e59cc13b105334857fde72d014dceae630889a4a34e5a42ded01c5c4d92f765e.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`e59cc13b105334857fde72d014dceae630889a4a34e5a42ded01c5c4d92f765e`
