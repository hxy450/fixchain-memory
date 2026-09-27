# 迁移设置开关时为每个开关落实运行期消费方：只调持久化 setter 不算完成

ID：`lesson-4d0f0176b3d09c33f1eb` · 版本：1

[本主题](index.md)

## 何时使用

功能接线阶段实现设置页开关与偏好仓库，或页面转换遇到按偏好切换的渲染与行为分支时

## 适用情境

源端设置用 DataStore/SharedPreferences 持久化，并被主题、计时器、反馈等运行期代码实时读取；目标端的设置页、偏好仓库、主题状态和消费页面由不同任务编写，靠占位登记传递“持久化并立即生效”的契约。

## 原因

设置页只调持久化 setter 时，开关看起来能切换，行为却不变；消费方在另一个文件，编译和结构审计都不检查。来源中主题与波浪计时器开关只写偏好，主题状态类除默认值外无人读写；步骤提示音与振动开关同样没有消费方，振动封装也没移植；页面转换者以“偏好未知”为由只写了进度样式的一个分支，还是源端默认值之外的那个。

## 做法

1. 为每个开关写出“键 → 读取点 → 效果”：主题类接到全局主题状态（@ObservedV2/@Trace），由应用入口在启动和 onConfigurationUpdate 时应用（如 ApplicationContext.setColorMode）；渲染样式类接到对应组件的分支；反馈类在事件分支里读开关再播放或振动。
2. 页面转换遇到按偏好切换的渲染分支时，两个分支都实现并以源端默认值为初值，或在该位置登记指向设置切片的前向占位；不要静态只写一个分支。
3. 反馈类：本地提示音用 rawfile 加 AVPlayer（resourceManager.getRawFd 设给 fdSrc）；振动移植源端封装，并在 module.json5 的 requestPermissions 声明 ohos.permission.VIBRATE。
4. 收尾 grep 偏好 getter 与状态字段：除默认值和 setter 外没有读取点的开关就是没完成。

## 来源（按需复核）

经验是有适用范围的历史建议。核查来源时同时看结论与 unknown；来源卡未随阅读包复制。

- case-290eac71ee43fe336138 · 结论：diagnosis, recommendation:2
  卡片版本：`16dd6156b038b81c4c28a4b9796519f347850ef11f4d08091a80ff8d310b7376`
- case-470d704a6ec794b4c3c9 · 结论：diagnosis, recommendation:2, recommendation:4
  卡片版本：`13ef866ddad634597d116308c049409fa19b886ac8827aba7a1101eafd7c59af`
