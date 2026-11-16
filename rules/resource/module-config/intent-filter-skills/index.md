# intent-filter 对应的 module.json5 skills

agent 会看到什么：源 AndroidManifest 的 <intent-filter> 带 VIEW / BROWSABLE 和 <data android:scheme / host / pathPrefix>、android:autoVerify，或 NFC 的 TECH_DISCOVERED；module.json5 的 skills 只有 entity.system.home 一项，uris 漏了源端的 scheme、host 或加了源端没有的，缺 domainVerify，或没有 TAG_FOUND skill

## 规矩

- rule-d7384bd9cbd7｜深链 intent-filter 要映射成 module.json5 的 skills，不只解析 want.uri｜读到：Activity 的 <intent-filter> 带 VIEW 和 <data android:scheme/android:host/android:pathPrefix>；写错：该 UIAbility 的 skills 只有 entity.system.home 那一项，没有带 viewData 和 uris 的 skill，代码里却在解析 want.uri
- rule-9125f594a852｜深链 skills 照 manifest 注册全部 scheme 和 host，不加源端没有的 scheme｜读到：AndroidManifest 的 <intent-filter android:autoVerify="true"> 有 <data android:scheme="https"> 与 <data android:scheme="http">、android:host；写错：module.json5 的 skills uris 注册了源端没有的自定义 scheme，漏掉 http，或没写 domainVerify
- rule-943c5f24056c｜带 autoVerify 的深链迁成 skill 时，同时写 "domainVerify": true｜读到：AndroidManifest 里 VIEW/BROWSABLE 的 intent-filter 带 android:autoVerify="true"，data 是 http/https；写错：module.json5 新增的 browsable skill（entity.system.browsable + ohos.want.action.viewData + uris）里没有 "domainVerify": true
- rule-f53d2fa2de3f｜TECH_DISCOVERED 入口要在 module.json5 声明 TAG_FOUND skill｜读到：<intent-filter> 里 <action android:name="android.nfc.action.TECH_DISCOVERED"/>，同名 <meta-data> 指向的 tech-list 列着 android.nfc.tech.NfcA 等；写错：module.json5 的 skills 只有 entity.system.home / ohos.want.action.home，只在 requestPermissions 追加了 ohos.permission.NFC_TAG
- rule-eb65a46ec79d｜module.json5 skills 按源 intent-filter 逐条登记，各 action 不合并｜读到：AndroidManifest.xml 的 <intent-filter> 有 android.intent.action.SEARCH、SEND、SEND_MULTIPLE、VIEW + <data android:scheme=…>；写错：module.json5 的 skills 只有一条 ohos.want.action.sendData（uris 只有 "type": "*/*"），没有 ohos.want.action.search、ohos.want.action.sendMultipleData，分享项没有 utd、maxFileSupported
- rule-19e03204cfbb｜分享接收的 sendData skill 在 uris 里写 utd，不把源 MIME 写成 type｜读到：AndroidManifest 的 intent-filter 有 <action android:name="android.intent.action.SEND"/> + <data android:mimeType="text/plain"/>（或 "image/*"）；写错：module.json5 的 sendData skill 里 uris 只有 {"type": "text/plain"} / {"type": "image/*"}，没有 utd 和 maxFileSupported；或挂在 EntryAbility 上带 entity.system.home
- rule-655f56b016d6｜源 manifest 没有对应 intent-filter 时，module.json5 不加相机等 skill｜读到：源 AndroidManifest.xml 没有相机相关 <intent-filter>，代码只调用系统相机（目标端用 cameraPicker.pick）；写错：module.json5 的 skills 里加了 {"entities": ["entity.system.camera"], "actions": ["ohos.want.action.camera"]}，理由是「cameraPicker.pick 前置」
- rule-1359e13d3041｜深链 host 和 wants.bundleName 写包名前，先确认 app.json5 已是最终值｜读到：源端 AndroidManifest 的深链 intent-filter 或快捷方式用到应用自己的包名；目标 app.json5 的 bundleName 读出来是 com.example.* 模板值；写错：module.json5 skills 的 uris 里 host 是 com.example.* 模板包名，shortcuts 的 wants.bundleName 同样是模板值
