# 源端通知用 setProgress 显示进度条时，目标用 downloadTemplate 模板带进度，不转成文本

审的是：代码
触发（任一种）：
- 读到：源端通知 `setProgress(max, progress, false)` 显示进度条；写错的样子：ArkTS 只发 BASIC 文本通知，把进度写成文字
适用范围：带进度条的通知迁到 notificationManager 时
做法：
- NotificationRequest 加 template: { name: 'downloadTemplate', data: { title, fileName, progressValue } }，progressValue 取源端 progress 对 max 的比例
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- template?: NotificationTemplate：NotificationRequest 的模板字段（出处：鸿蒙 SDK 的 ets/api/notification/notificationRequest.d.ts，NotificationRequest.template）
- name 只支持 downloadTemplate；data 的 title、fileName 必填（string），progressValue 是 number：进度模板的名字和数据（出处：鸿蒙 SDK 的 ets/api/notification/notificationTemplate.d.ts，NotificationTemplate）
未核实：progressValue 的取值范围（0–100 还是别的）声明里没写
来源：1 张卡，1 个应用
- case-f4fef12b5d994df457b2（Cofi）：做法第 1 步 ← 诊断
