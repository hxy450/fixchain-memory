# 迁移设置开关、设置保存与持久化的界面状态时为每项落实运行期消费方：只调持久化 setter、只写远端设置不算完成

ID：`lesson-4d0f0176b3d09c33f1eb` · 版本：5 · 阶段：execute · 主题：[app/cross-cutting](index.md)

概要：设置开关逐项落实运行期消费方，只调 setter 不算完成

信号：`DataStore`, `SharedPreferences`, `preferences`, `@ObservedV2`, `@Trace`, `ApplicationContext.setColorMode`, `onConfigurationUpdate`, `ohos.permission.VIBRATE`, `setAppPreferredLanguage`, `ApplicationContext.setLanguage`

## 何时使用

功能接线阶段实现设置页开关与偏好仓库，或页面转换遇到按偏好切换的渲染与行为分支时；迁移设置页的保存逻辑，或切换即持久化的界面状态（如首页视图位置）时

## 适用情境

源端设置用 DataStore/SharedPreferences 持久化，并被主题、计时器、反馈等运行期代码实时读取；目标端的设置页、偏好仓库、主题状态和消费页面由不同任务编写，靠占位登记传递“持久化并立即生效”的契约。也包括源端设置保存除远端同步外还更新本地配置缓存并发刷新事件（如排序设置保存后各列表按新配置排序），目标只写远端设置；以及源端切换视图即写偏好、启动时读取恢复，目标只改内存状态。也包括应用内语言选择只调用持久化的偏好语言接口，而规格要求保存后立即切换。

## 原因

设置页只调持久化 setter 时，开关看起来能切换，行为却不变；消费方在另一个文件，编译和结构审计都不检查。来源中主题与波浪计时器开关只写偏好，主题状态类除默认值外无人读写；步骤提示音与振动开关同样没有消费方，振动封装也没移植；页面转换者以“偏好未知”为由只写了进度样式的一个分支，还是源端默认值之外的那个。另一应用的排序设置保存只写远端设置，列表查询不读任何本地排序配置，重构时又原样抽进 ViewModel；首页视图位置的持久化规格获批后没有排期，视图选择只写内存，重启总回默认视图。

## 做法

1. 为每个开关写出“键 → 读取点 → 效果”：主题类接到全局主题状态（@ObservedV2/@Trace），由应用入口在启动和 onConfigurationUpdate 时应用（如 ApplicationContext.setColorMode）；渲染样式类接到对应组件的分支；反馈类在事件分支里读开关再播放或振动。
2. 页面转换遇到按偏好切换的渲染分支时，两个分支都实现并以源端默认值为初值，或在该位置登记指向设置切片的前向占位；不要静态只写一个分支。
3. 反馈类：本地提示音用 rawfile 加 AVPlayer（resourceManager.getRawFd 设给 fdSrc）；振动移植源端封装，并在 module.json5 的 requestPermissions 声明 ohos.permission.VIBRATE。
4. 收尾 grep 偏好 getter 与状态字段：除默认值和 setter 外没有读取点的开关就是没完成。
5. 迁移设置页保存逻辑时列出源端保存处理的全部副作用（远端同步、本地配置缓存、刷新事件），每一项在目标端指明消费者；配置键或加载函数在仓库、查询服务中没有调用点就是未接通。
6. 切换即持久化、启动恢复的界面状态，写入与恢复两端都落地：切换时先持久化再更新状态，恢复放在偏好异步加载完成之后，非法值按源端规则回退。
7. 应用内语言切换核对所选 API 的生效时机：偏好语言接口（setAppPreferredLanguage）按偏好在应用启动时加载资源；要求保存后立即切换时另行让当前进程即时生效（来源采用 ApplicationContext.setLanguage），并刷新已显示的代码内取值文案，以 SDK 声明或真机确认。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [解前向占位按触发文本逐项兑现，写常量不算闭合](../../process/deferred-fulfillment/lesson-eb4de4fd7452308a0483.lesson.md)（共享 2 张卡）
- [拆层后各层方法按源端覆写与调用全集核对](../../process/enumeration-gaps/lesson-61a9fc7190c51c663697.lesson.md)（共享 1 张卡）
- [功能对齐以代码落点为准，空回调不算实现](../../process/claimed-without-receipt/lesson-9147be4d87153de9c5b6.lesson.md)（共享 1 张卡）
- [点击无响应先设备复现定位，未上机结论标未验证](../../process/unverified-as-fact/lesson-afae8d13e00941efe808.lesson.md)（共享 1 张卡）
- [语言目录按源 values-* 全集与粒度镜像](../../ui/text/copy/lesson-b58df29f032cc6a8c9d6.lesson.md)（共享 1 张卡）

来源支持：6 张卡 · 已知 3 次迁移（部分未记录） · 已知 3 个应用（部分未记录）

## 来源（按需复核）

- [case-290eac71ee43fe336138](../../../../store/cases/case-290eac71ee43fe336138/36fe85bdc79e77054719ea97a0169df35b9ef6bf2d243da993b6623a7ca4e681.json) · 结论：diagnosis, rec-e360b9b8fd
  卡片版本：`36fe85bdc79e77054719ea97a0169df35b9ef6bf2d243da993b6623a7ca4e681`
- [case-470d704a6ec794b4c3c9](../../../../store/cases/case-470d704a6ec794b4c3c9/e7b22c984628feae31f593f0a2b3ecb03c60fc956620aa16dc545800bc3c3def.json) · 结论：diagnosis, rec-abc394020b, rec-7bfd5e05d2
  卡片版本：`e7b22c984628feae31f593f0a2b3ecb03c60fc956620aa16dc545800bc3c3def`
- [case-7f25b9e411fd7ea08eb8](../../../../store/cases/case-7f25b9e411fd7ea08eb8/b0032836632c952424844dd36317b057e3978e311730fb0f18415b55dc9cec96.json) · 结论：rec-5a5f561ec5
  卡片版本：`b0032836632c952424844dd36317b057e3978e311730fb0f18415b55dc9cec96`
- [case-8a522021d6d10fded125](../../../../store/cases/case-8a522021d6d10fded125/695193a757e708a77ef3560a9f73b4caf829f00fdfad9ee70368e51f842a04f9.json) · 结论：rec-0467c710bf
  卡片版本：`695193a757e708a77ef3560a9f73b4caf829f00fdfad9ee70368e51f842a04f9`
- [case-dce365054567a94bd4db](../../../../store/cases/case-dce365054567a94bd4db/49d99db19d9b511c1e6e070605c989289944f7be60de1d7dbcec50a5c3b2e218.json) · 结论：diagnosis, rec-53e684c999
  卡片版本：`49d99db19d9b511c1e6e070605c989289944f7be60de1d7dbcec50a5c3b2e218`
- [case-ea1fc6a0711a8176b79c](../../../../store/cases/case-ea1fc6a0711a8176b79c/7eacf7d6fe6f97cf98c91ebecec4431cc188b0bc40b4866c5d4f39bc62b18a23.json) · 结论：diagnosis, rec-7cdb26e889, rec-053470abd8
  卡片版本：`7eacf7d6fe6f97cf98c91ebecec4431cc188b0bc40b4866c5d4f39bc62b18a23`
