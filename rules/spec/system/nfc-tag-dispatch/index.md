# NFC 贴卡的系统派发入口和前台派发

agent 会看到什么：源端 Manifest 的 activity / activity-alias 带 android.nfc.action.TECH_DISCOVERED，偏好里用 setComponentEnabledSetting 启停这个 alias，onResume 里 enableForegroundDispatch，规格里写成「无对等 → 应用内开关模拟」或让开关连前台派发一起拦

## 规矩

- rule-7f7148f9febd｜清单 TECH_DISCOVERED 贴卡入口和启停它的开关分两行映射，入口对到 TAG_FOUND skill｜读到：AndroidManifest 里 activity 或 activity-alias 的 intent-filter 带 android.nfc.action.TECH_DISCOVERED，meta-data 指向 tech-list 资源；偏好里用 PackageManager.setComponentEnabledSetting 启停这个 alias；写错：映射基线把 TECH_DISCOVERED 入口写成「无对等 → 应用内开关模拟」并和 setComponentEnabledSetting 并成一个决策，或写「贴卡以 tag 回调事件替代 ACTION_TECH_DISCOVERED Intent」；规格里没有 skill 声明和 want 解析；HARD-DIV 行没写查证依据
- rule-3e73b94fca1a｜源开关只启停系统派发入口时，替代开关也只拦系统派发，规格写明前台派发不受影响｜读到：偏好保存时只对 activity-alias 调 setComponentEnabledSetting(…ENABLED/DISABLED, DONT_KILL_APP)；基类 onResume 无条件 enableForegroundDispatch；写错：替代方案写成「开关 true = 注册前台 tag listener，false = 不注册」，验收条目要求开关两态下前台贴卡响应 / 不响应
