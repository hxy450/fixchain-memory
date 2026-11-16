# 分享接收入口的 Ability 和 skills 声明

agent 会看到什么：参考规格写分享接收是 SEND + DEFAULT + mimeType text/plain、launchMode 未声明即 standard；台账或派工把 actions=[ohos.want.action.sendData]、entities=[entity.system.home]、type=text/plain 挂在入口 Ability 上，或写「EntryAbility onCreate/onNewWant 分支有确定写者」

## 规矩

- rule-37055f06496e｜派工定分享接收入口时，写独立 multiton Ability 和 utd 声明，不把源 MIME 当 type｜读到：参考规格写分享接收是 SEND + DEFAULT + mimeType text/plain，launchMode 未声明即 standard；写错：台账或派工把字段定成「actions=[ohos.want.action.sendData] entities=[entity.system.home] type=text/plain」挂在入口 Ability 上，或写「EntryAbility onCreate/onNewWant 分支有确定写者」
