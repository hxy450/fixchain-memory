# AlarmManager 定时提醒和它的 BroadcastReceiver

agent 会看到什么：读到源端 AlarmManager.setExact 到点由 BroadcastReceiver.onReceive 自绘通知（按钮各带 PendingIntent、Parcel 还原快照后写库、RRULE 重复提醒由应用链式重挂）；产物里 reminderAgentManager.publishReminder 的失败和上限回退、actionButton 和 subscribeReminderState，以及到点写回 DB 的逻辑

## 规矩

- rule-a2f635134d84｜publishReminder 失败或超出条数上限时回退本地通知，并保留应用侧链式重挂｜读到：源端 AlarmManager 精确闹钟到点自绘通知，重复提醒（RRULE）到点后由应用链式挂下一次；写错：publishReminder 失败只记日志、返回 0，没有条数上限处理，也没有 notificationManager 本地通知回退；重复提醒只发布首个发生
- rule-030595c3d5cd｜提醒按钮用 subscribeReminderState 回调分派、贪睡写 timeInterval，不以系统型按钮近似｜读到：源端提醒通知的按钮各带 PendingIntent：贪睡 = 现在加偏好分钟，推迟 = 弹时间选择器；写错：ReminderRequest.actionButton 只写 ACTION_BUTTON_TYPE_SNOOZE / ACTION_BUTTON_TYPE_CLOSE 当「最大近似」，不设 timeInterval，不订阅按钮状态，按钮动作只能经点通知本体到达
- rule-6b193c9b7e63｜源端以 Parcel 快照写回时，目标按快照覆盖写回，不改成 DB 现值优先或跳过｜读到：Java `BroadcastReceiver.onReceive` 用 Parcel 反序列化还原快照对象，直接 set 字段后 update 写库，没有读回或存在性检查；写错：ArkTS 写回前先按 id 读 DB 现值，读回为 null（已删）或已置位就 `return`；注释写「以 DB 现值优先（快照仅兜底）」「有据偏离」，台账里没有对应决策
