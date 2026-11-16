# 开关控制的常驻通知做成应用级单例服务，装配处 restore、前台 reconcile，页面离开不释放其订阅

审的是：代码
触发（任一种）：
- 读到：源端通知帮助类以固定 ID、setOngoing(true) 发布常驻通知，cancel 只在关闭开关时调用；写错的样子：通知更新写在页面 ViewModel 的回调里，页面 aboutToDisappear 里移除回调、停止观察；冷启动时偏好开着也不恢复监听
适用范围：目标端实现由开关控制、由设备事件驱动的常驻通知时
做法：
- 写一个应用级单例通知服务，提供 setEnabled / restore / reconcile / release；在能力装配处 restore（偏好开启就常驻监听），回到前台时 reconcile 复核系统许可
- 事件到达时用 notificationManager.publish({ id: <固定 ID>, isOngoing: true, … }) 以同一 ID 更新；页面 ViewModel 只转发开关动作，aboutToDisappear 不释放通知所需的订阅，release 不撤销通知
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- function publish(request: NotificationRequest): Promise<void>：发布通知（出处：鸿蒙 SDK 的 ets/api/@ohos.notificationManager.d.ts，notificationManager.publish）
- NotificationRequest.id?: number，缺省 0；同一 ID 已存在时更新通知内容：源端固定通知 ID 对到这里，同 ID 发布即更新（出处：鸿蒙 SDK 的 ets/api/notification/notificationRequest.d.ts，NotificationRequest.id）
- NotificationRequest.isOngoing?: boolean：源端 setOngoing(true) 对应的常驻标记（出处：鸿蒙 SDK 的 ets/api/notification/notificationRequest.d.ts，NotificationRequest.isOngoing）
- function cancel(id: number, label?: string): Promise<void>：只在关闭开关时调用（出处：鸿蒙 SDK 的 ets/api/@ohos.notificationManager.d.ts，notificationManager.cancel）
- function isNotificationEnabled(): Promise<boolean>：reconcile 时复核系统许可（出处：鸿蒙 SDK 的 ets/api/@ohos.notificationManager.d.ts，notificationManager.isNotificationEnabled）
来源：1 张卡，1 个应用
- case-2bb1f7385338bea7e396（骑行记录）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2、诊断
