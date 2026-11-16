# 接收别的应用分享来的 ACTION_SEND

agent 会看到什么：读到源端入口 Activity 从 getIntent() 的 ACTION_SEND 读 EXTRA_TEXT、EXTRA_SUBJECT、EXTRA_STREAM 后打开页面，处理完 setResult + finish()；产物里 EntryAbility 或承接 Ability 的 onCreate / onNewWant 怎么取分享内容（systemShare.getSharedData、want.parameters 的键）、怎么传给页面、内容为空时开不开页、结束的是谁

## 规矩

- rule-661a999f6a62｜接收分享用 getSharedData(want).getRecords() 按 utd 取数，不读猜的或自造的键｜读到：源端从 intent 的 EXTRA_TEXT / EXTRA_STREAM 取分享文本和图片；写错：目标按 want.parameters 的 ohos.extra.param.key.shareContent 等猜的键名和 want.uri 取分享内容，没调 systemShare.getSharedData
- rule-d2a4a43c841e｜分享承接 Ability 用 getSharedData 取数据、经 LocalStorage 传页面，只结束自己｜读到：源码只在 onCreate 读 getIntent() 的 EXTRA_TEXT，没有 onNewIntent，处理完 setResult + finish()；写错：唯一的 EntryAbility 在 onCreate 和新加的 onNewWant 里都解析分享 want，经全局事件或静态中转变量送页面；页面在分享分支里调 terminateSelf()，关掉整个应用
- rule-e6c7452bc727｜源端收到 SEND 即打开目标页时，目标不加「内容全空就丢弃」｜读到：源端收到 ACTION_SEND 后 EXTRA_TEXT ?: ""，无论有没有内容都打开目标页；写错：目标分享处理里写了 `if (url === '' && body === '' && image === '') return;`，或以各槽全空判为「无分享」不打开页面
