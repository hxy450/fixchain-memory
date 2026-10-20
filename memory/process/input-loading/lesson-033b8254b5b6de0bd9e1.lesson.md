# 页面、控件、算法或实体基类由二进制三方库承载时，按依赖坐标取库制品核对真值，不按调用面推断或以原生组件近似

ID：`lesson-033b8254b5b6de0bd9e1` · 版本：1

[本主题](index.md)

## 何时使用

规格提取与实现阶段，为 build.gradle 二进制依赖（AAR/jar）承载的界面、提示条与对话框、手势、算法输出或实体基类写映射决策、行为契约或自研等价实现，以及为它们登记占位时

## 适用情境

仓库内只有调用面：Activity extends 库类，布局根节点或 UI 快照只剩库的自定义 View 类名，应用侧只留 Style/Configuration 常量或 Builder 调用，实体 extends 库基类，常量或正则来自库类；行为、几何、动画、队列、手势阈值、字段集或输出字符串都在库内。规格或映射参考写成「Toast / 原生组件 / 自研 / 系统 intl 替代」并标 Auto，或写「库源不可见→默认样式即可对齐」；本机 Gradle 缓存可能还没有该制品。

## 例外与边界

- 决策台账里有带编号、经用户批准的范围裁剪或降级，明确该库功能不复刻

## 原因

目标端没有同名库时，写者只看得到应用侧的调用、常量与类名，便按名字、属性或常量反推：库内的队列与出队时机、动画时长与插值、dimens 与布局、截断与行距、手势阈值与惯性、字段集与 equals、序列化字面形态和文案阈值都会丢失。登记成“近似”“待视觉对齐”的占位没有真值可对齐，到交付也兑现不了。坐标与版本就写在构建脚本里，“仓库内无源码”是可补的材料缺口，不等于行为不可知。

## 做法

1. 从 build.gradle（含 gradle.properties、版本目录）读出库坐标与版本，按序取制品：本机 ~/.gradle/caches/modules-2/files-2.1；没有就用 Gradle 解析下载该依赖，或按坐标从 Maven 仓库、JitPack（https://jitpack.io/com/github/<owner>/<repo>/<version>/）、上游仓库对应版本 tag 获取，有 sources jar 时优先。
2. 解包后按库的职责取真值：UI 库读 res 的 layout、values（dimens、styles、strings、integers）、anim/animator、drawable 及其限定目录（layout-land、values-sw600dp 等），并用 javap -p -c 或反编译读控件、管理器与 Builder 的测量、缺省参数、动画、队列与触摸分支；先列出库内全部视图类，再判断目标组件是否足够（图片查看器的缩放、平移、双击、惯性属于库行为，不是可省略的增强）。实体基类读字段集、类型、缺省值、equals/toString 与序列化规则；库里的常量与正则按库值迁移。
3. 算法库（重复规则、相对时间、日期格式、文本拆分与序列化）用 JDK 小程序加载同版本 jar 跑代表输入，把输出的字面形态（时区形态、行尾、文案模板、单位阈值与取整）写成契约；登记常量时同时登记它经库序列化后的字符串。系统 i18n/intl 只在与库输出对代表输入逐字一致时替代；库有自有阈值、模板或资源表时移植算法与资源。
4. 把真值写进规格映射行或组件头注释，注明库内文件、资源名或类方法与版本；映射行的依据只是仓库内调用行、README、单元测试或分析产物里的“建议”时，不标 Auto、不进跨栈硬映射基线，实现也不凭样式常量类自定时长、角度或间距。
5. 确实取不到时，在规格逐项列出缺失的库真值（队列时序、几何、手势、序列化格式、文案）及其影响，登记为阻塞或交用户改判；不写「默认样式即可对齐」，也不把这类占位的兑现交给视觉对齐步骤。派工给出 Android 源码路径时，一并给出库制品缓存路径与可解包提示。

来源支持：17 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-1a09dd649093f650a6fc](../../../store/cases/case-1a09dd649093f650a6fc/da04b374b7092b19b66477caa7b72bf7555cde232a69d7d65bab1fe080a2a458.json) · 结论：recommendation:4
  卡片版本：`da04b374b7092b19b66477caa7b72bf7555cde232a69d7d65bab1fe080a2a458`
- [case-1bee3e42eae9e1092ceb](../../../store/cases/case-1bee3e42eae9e1092ceb/341c9452897eb8bf11090c600c5a436b37e1c719e3b0ce1f9227c30a577fb063.json) · 结论：recommendation:2
  卡片版本：`341c9452897eb8bf11090c600c5a436b37e1c719e3b0ce1f9227c30a577fb063`
- [case-44a53125e4f44a862c80](../../../store/cases/case-44a53125e4f44a862c80/5e62d1276d05aa0f89888247b9ed48150a94fca16b46cc40b6c45d8eb14f5f88.json) · 结论：recommendation:1
  卡片版本：`5e62d1276d05aa0f89888247b9ed48150a94fca16b46cc40b6c45d8eb14f5f88`
- [case-5e7f81b1b1ef0753d249](../../../store/cases/case-5e7f81b1b1ef0753d249/203ae9a24100267c1011c082352849d2f6596b184a230d8213699ec0075fa03b.json) · 结论：recommendation:1
  卡片版本：`203ae9a24100267c1011c082352849d2f6596b184a230d8213699ec0075fa03b`
- [case-6984b2614fabe391f2e7](../../../store/cases/case-6984b2614fabe391f2e7/4e13e5e45b38251a019a68c084e9d1f1d2301fcf064ee28b4c8386bbcbbeb2b3.json) · 结论：diagnosis, recommendation:2
  卡片版本：`4e13e5e45b38251a019a68c084e9d1f1d2301fcf064ee28b4c8386bbcbbeb2b3`
- [case-69a2766b2050118ebd5a](../../../store/cases/case-69a2766b2050118ebd5a/6d5ac1c6e6d2ab3eae9fdfa84fcbe2a5898f18f062dd05c39baed1dcb8862237.json) · 结论：recommendation:4
  卡片版本：`6d5ac1c6e6d2ab3eae9fdfa84fcbe2a5898f18f062dd05c39baed1dcb8862237`
- [case-74b07cb94daa311f36b1](../../../store/cases/case-74b07cb94daa311f36b1/fec951d790df3788a4e544e587922a8b64074abd17fe9d0f10ed1821d72413f8.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`fec951d790df3788a4e544e587922a8b64074abd17fe9d0f10ed1821d72413f8`
- [case-7b71b27d8bbbbbd73267](../../../store/cases/case-7b71b27d8bbbbbd73267/eae79498ed3c968868f59d3c0d5142443209228899494c6d32604f7e84767fc3.json) · 结论：recommendation:3
  卡片版本：`eae79498ed3c968868f59d3c0d5142443209228899494c6d32604f7e84767fc3`
- [case-927e26bb7b18f83f2f38](../../../store/cases/case-927e26bb7b18f83f2f38/e18332363723b7bd11b836789fed1816595b3d6fe4b3ac4982e023090aeef94a.json) · 结论：recommendation:4
  卡片版本：`e18332363723b7bd11b836789fed1816595b3d6fe4b3ac4982e023090aeef94a`
- [case-9cfde635e67a08373fe6](../../../store/cases/case-9cfde635e67a08373fe6/2518eb32a760514e0502b0ebe77fc6cbe0a1431c7916a06f5aaf27ba9bf58985.json) · 结论：recommendation:1, recommendation:3
  卡片版本：`2518eb32a760514e0502b0ebe77fc6cbe0a1431c7916a06f5aaf27ba9bf58985`
- [case-a767fbce6dbdeb152c90](../../../store/cases/case-a767fbce6dbdeb152c90/89be36740c387ae24ae94ed98391b3c233f903f9dfb845c26339844a0cc5108d.json) · 结论：recommendation:1, recommendation:4
  卡片版本：`89be36740c387ae24ae94ed98391b3c233f903f9dfb845c26339844a0cc5108d`
- [case-ac1b65b76f72e7be3fa6](../../../store/cases/case-ac1b65b76f72e7be3fa6/cdb9faac1ebcaa9e773f9d8554ce300513bd212e668336b1f874cbab05359895.json) · 结论：recommendation:2
  卡片版本：`cdb9faac1ebcaa9e773f9d8554ce300513bd212e668336b1f874cbab05359895`
- [case-cfa31a0f8f73caf9c2ab](../../../store/cases/case-cfa31a0f8f73caf9c2ab/55a32e80e90566ff6308fdfe101d216ac8b4845166cf0494f41c7926649575d5.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`55a32e80e90566ff6308fdfe101d216ac8b4845166cf0494f41c7926649575d5`
- [case-d23537ecc4c87801075a](../../../store/cases/case-d23537ecc4c87801075a/82aba2b2aeb3562e5d2c48260683b0f99162c182846f0e6771624298a1d71ff5.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`82aba2b2aeb3562e5d2c48260683b0f99162c182846f0e6771624298a1d71ff5`
- [case-e9189514e875ef00f96f](../../../store/cases/case-e9189514e875ef00f96f/70962a835201462f5cdf9dc9d03b341d51dc0e830922cf32d7761f935762ea1b.json) · 结论：recommendation:3
  卡片版本：`70962a835201462f5cdf9dc9d03b341d51dc0e830922cf32d7761f935762ea1b`
- [case-e91d2b9a9a156d1023ec](../../../store/cases/case-e91d2b9a9a156d1023ec/3558471f038583b62bb0d5d4b2516ab8ea7ee5c983b222032cb253201c25aec8.json) · 结论：diagnosis, recommendation:1, recommendation:4
  卡片版本：`3558471f038583b62bb0d5d4b2516ab8ea7ee5c983b222032cb253201c25aec8`
- [case-f4ebb1d613a2d9343ee5](../../../store/cases/case-f4ebb1d613a2d9343ee5/42debda6548084b597fd3fae3277c26d5564470d9fea934415a27bdc2e0c3a95.json) · 结论：recommendation:1
  卡片版本：`42debda6548084b597fd3fae3277c26d5564470d9fea934415a27bdc2e0c3a95`
