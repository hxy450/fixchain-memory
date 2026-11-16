# 常驻通知的发布者和生命周期

agent 会看到什么：源端通知帮助类按固定 ID notify / cancel 常驻通知、只在特定回调里调用；产物里 notificationManager.publish 写在哪个页面、ViewModel 或服务里，页面离开时是否停掉

## 规矩

- rule-c6b028a4a5d3｜开关控制的常驻通知做成应用级单例服务，装配处 restore、前台 reconcile，页面离开不释放其订阅｜读到：源端通知帮助类以固定 ID、setOngoing(true) 发布常驻通知，cancel 只在关闭开关时调用；写错：通知更新写在页面 ViewModel 的回调里，页面 aboutToDisappear 里移除回调、停止观察；冷启动时偏好开着也不恢复监听
- rule-d01d2754f156｜只在源端真正调用通知的回调里发布通知，二级页不新增通知发布者｜读到：二级页 Activity 的监听回调只刷新列表或弹连接成功框，不调用通知帮助类，onDestroy 里注销监听；写错：二级页的 ViewModel 回调里也调通知更新（如连接变化时以电量 -1 覆盖电量文本），出现第二个通知发布者
