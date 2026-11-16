# 清单 intent-filter 声明的外部动作和分享接收

agent 会看到什么：读到 AndroidManifest 入口 Activity 下的多条 intent-filter（SEND、SEND_MULTIPLE、SEARCH、PROCESS_TEXT、自定义 scheme 的 VIEW）和代码里读的 EXTRA_TEXT / EXTRA_STREAM / EXTRA_SUBJECT；规格把它们合成一条 sendData skill、按 want.parameters 自造键取数，或写成不路由

## 规矩

- rule-259a37390442｜规格把 Manifest 每条 intent-filter 逐条映射成 skills，不合并、不移交｜读到：AndroidManifest.xml 的入口 Activity 下有多条独立 intent-filter（如 SEARCH、VIEW 自定义 scheme、SEND、SEND_MULTIPLE、PROCESS_TEXT）；写错：规格把 SEND 与 SEND_MULTIPLE 合成一条 sendData skill（uris 只有 type */*，没有 utd、maxFileSupported），SEARCH 写成「交给应用内搜索组件」或「不路由（域外）」而不登记 skill
- rule-5d7bd1f49255｜ACTION_SEND 分享接收的规格写 utd 声明和 getSharedData 取数，依据写出处｜读到：AndroidManifest 里 intent-filter 带 action.SEND + category.DEFAULT 和 mimeType（text/plain、image/*），代码从 EXTRA_TEXT / EXTRA_STREAM 取分享内容；写错：规格映射行写「sendData + type 注册；EntryAbility 读 want.parameters」，取数契约按 want.parameters 和 want 的 uri 写，依据栏只写「grill 确认」；验收写「skills 含两类 type 声明」
- rule-c82fcd2b614b｜规格里的入口载荷键不自造：安卓 EXTRA_* 原键与鸿蒙标准键并列写，查不到来源的标未知｜读到：源端入口分发读 Intent.EXTRA_SUBJECT / EXTRA_TEXT / EXTRA_STREAM；写错：规格自造「参数映射表」把它们定为 params.subject / params.text / 文件 uri，没注明键的来源，也没列安卓原键和鸿蒙标准键
