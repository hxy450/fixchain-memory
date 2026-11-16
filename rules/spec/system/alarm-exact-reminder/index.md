# AlarmManager 精确闹钟和它到点发的通知

agent 会看到什么：读到源端 AlarmManager 精确闹钟到点自绘通知、按钮各带 PendingIntent（贪睡、推迟）；规格把代理提醒的按钮写成带 wantAgent 的 actionButton，或以「系统托管」降级到点副作用和开机恢复，没写发布失败码、有效提醒条数上限和到点无回调

## 规矩

- rule-80cf269119de｜规格写代理提醒替代路径时逐字段对照 reminderAgentManager 声明，不嫁接通知按钮的 wantAgent｜读到：源端 AlarmManager 精确闹钟到点自绘通知，按钮各带 PendingIntent（贪睡 = 现在加偏好分钟、推迟 = 弹选择器）；写错：规格把提醒按钮写成 actionButton{title, wantAgent = 拉起 UIAbility 的 Want}，或以「系统托管」裁决降级到点副作用和开机恢复，没写发布失败码、有效提醒条数上限、到点无回调
