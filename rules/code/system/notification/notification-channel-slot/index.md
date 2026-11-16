# 通知渠道和通知槽（NotificationChannel、SlotType）

agent 会看到什么：读到源端 new NotificationChannel(id, name, NotificationManager.IMPORTANCE_*) 后 createNotificationChannel；产物里 addSlot 和 NotificationRequest 用的 SlotType，以及有没有源渠道 id、名称、重要度到目标槽的映射

## 规矩

- rule-706f70809d11｜源端建具名高重要度通知渠道时，写出渠道到 SlotType 的显式映射并声明这项替代｜读到：new NotificationChannel(id, name, NotificationManager.IMPORTANCE_HIGH) 后 createNotificationChannel；写错：addSlot 和 NotificationRequest 直接用通用 SlotType.SERVICE_INFORMATION，代码里没有源渠道 id、名称、重要度到目标槽的映射，交付汇报也没声明这项替代
