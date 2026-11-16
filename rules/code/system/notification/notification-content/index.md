# 通知的正文和模板

agent 会看到什么：源端 NotificationCompat.Builder 的 setContentText / setProgress；产物里 NotificationRequest 的 normal.text 和通知模板

## 规矩

- rule-7a191c6682db｜源端通知正文拼了多个字段时，目标通知 text 逐字段照输出，快照字段都要消费｜读到：源端通知构建处 setContentText(…) 传入拼接的正文（如数值文本后接 " (m:ss)" 时长）；写错：目标 publish 的 normal.text 只输出其中部分字段，某个字段只在另一字段缺失时才作为退路显示；服务快照 interface 里为正文定义的字段没被渲染函数读取
- rule-7f2aa2c31300｜源端通知正文可为空时，NotificationBasicContent.text 不给空串，用不可见占位｜读到：源端 `setContentText(...)` 的值可为 null，完成通知只有标题没有正文；写错：ArkTS 写 `text: text !== null ? text : ''` 或完成通知 `text: ''`
- rule-2e4fc0160fe6｜源端通知用 setProgress 显示进度条时，目标用 downloadTemplate 模板带进度，不转成文本｜读到：源端通知 `setProgress(max, progress, false)` 显示进度条；写错：ArkTS 只发 BASIC 文本通知，把进度写成文字
- rule-df5159a1146b｜通知封装按源端 builder 默认值填齐 smallIcon 和默认大图标，再由调用方覆盖｜读到：源端通知 helper 的 builder 默认调 setSmallIcon(...) 和 setLargeIcon(...)（默认大图标来自应用 drawable）；写错：NotificationRequest 没写 smallIcon，largeIcon 只在调用方传入时才写，没有默认大图标
