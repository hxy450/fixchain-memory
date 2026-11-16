# 占位、规格与测试

派工、占位登记或代码注释里有 FWD-REF、PLACEHOLDER、P-ID 条目，规格的 AC、台账里的「平台无对等」，孤儿检测报 NO_IMPORTER，或单测、派工的要求和源端不同时

## 触发族

- [代码里的 FWD-REF 占位](fwd-ref/index.md)（11 条）：读到派工、占位登记表或代码注释里的 FWD-REF 标记（P-ID 条目、要实现的源方法、外链常量、平台切片、页面壳的钩子），交回的代码生成、替换或删掉了这个标记
- [源端没有的入口控件](extra-entry/index.md)（2 条）：派工、修复条目或台账要求补一个入口（按 Android 可达入口补 UI、在对等页面补替代页入口），交回的代码新增了源布局里没有的 Button、Row 或 Image
- [规格 AC、状态接口和对接点要的行为](spec-ac-behavior/index.md)（16 条）：读到规格的 AC、状态接口（'idle' | 'success' | 'error'）、端点和门控或对接点写明的行为，交回的代码少了它要的渲染分支、端点，或和已读源码冲突时把偏差写成契约、没回报
- [占位登记条目的兑现](placeholder-resolve/index.md)（9 条）：读到占位登记里 FWD-REF、P-S*、forward-ref 条目的触发文本和 resolve_by；产物里这个占位被换成了只做一半的实现：自拟的状态机、只写持久化、留 no-op、恒 return null
- [带求交过滤的初始化分支的单测](filter-intersect-unit-test/index.md)（2 条）：读到源端或已有实现先合并再与可用列表 .filter 求交，产物里是这段分支的单测夹具（mock 的可用列表）和 expect 断言，或为让 RED 变绿改动的产品过滤
- [第三方 SDK 的占位登记](sdk-placeholder/index.md)（1 条）：读过的领域 skill 写明 SDK 可从 ohpm 取（如 @tencent/wechat_open_sdk）并给了调起和回调写法，占位登记却写着待入仓；交回的代码里留着 PLACEHOLDER、FWD-REF 空实现
- [写着「等价于源端谓词」的占位](predicate-placeholder/index.md)（1 条）：读过的占位登记要求实现「等价于源端某谓词」；交回的代码闭合了占位，却只剩一个 id 相等比较，传给行组件 @Param 的在播或选中标志漏了条件
- [写成恒 false 的「平台无对等」能力和标志](no-equivalent-stub/index.md)（4 条）：读到规格或台账写「平台无对等 → 恒 false」、账本里 approved 的等价实现，或源端在多处 if 里消费的标志；产物里写成 readonly … = false 的恒 false、两个分支返回同一值（? X : X）、persist 恒返回 false，注释写「HarmonyOS 无…」「契约位保留」「本管线无入口」
- [指定为唯一尺寸来源的布局信息](size-single-source/index.md)（1 条）：读到用户或派工指定某个布局信息为预览尺寸唯一来源、源端 Kotlin 按尺寸类型 when 分支返回固定宽高；产物里尺寸函数在取布局盒之前先按内容比例另行 return，并有单测锁定这个旁路
- [孤儿检测报 NO_IMPORTER 的页面和弹窗](orphan-no-importer/index.md)（1 条）：读到孤儿检测对 dialogs/ 或 pages/ 下的组件报 NO_IMPORTER，而规格写了它的 ArkTS output、ui-manifest 记为 verified 或 feature-index 列为范围内页面；产物里收口补丁 Delete File 删了这个 .ets，或给它补了源码里没有的调用方
- [比源端更严的 RED 测试契约](red-test-stricter-than-source/index.md)（1 条）：读到问题文件把某个用例标 RED、要求的区分度或行为超出源端算法（如 dHash 逐行 right > left 取 64 位、没有亮度分量）；产物里产品代码加了源端没有的分量，或按别的用例期望反推实现，只为让用例转 GREEN
- [派工或壳注释点名要接通的控件](named-control-wiring/index.md)（1 条）：读到派工的 cross_slice_edits、壳页 handler 注释或 FWD-REF 登记点名了源端 ImageButton 一类控件要接通；产物里只有 handler 函数和能力门控，build() 里没有调用它的 Button 或显隐分支
