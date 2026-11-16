# 源端取设备语言和语言映射的逻辑

agent 会看到什么：读到源端取设备语言后做映射（严格 `=== 'zh'` 才强制映射、取语言的 async 函数没被 await、同步跑 i18n.use(LanguageDetector).init({ lng })），目标系统语言接口返回 zh-Hans-CN 这类 BCP 47 标签；规格把匹配条件放宽到任意 script/region 变体，或照异步分支写初始语言的 AC

## 规矩

- rule-08d534fb3bb7｜不扩大源端的语言匹配条件；BCP 47 标签按 script/region 分别列映射并各给 AC 样例｜读到：源端只在设备语言严格 `=== 'zh'` 时做强制映射；目标系统语言接口返回带 script/region 的 BCP 47 标签（如 zh-Hans-CN、zh-Hant-TW）；写错：规格写成「主标签 zh 的任意 script/region 变体都映射为 zh-TW」，判据含 zh-Hans-CN→zh-TW
- rule-f970ebfc9795｜源端初始语言由未 await 的异步赋值和同步检测插件共同决定时，契约写 init 那刻实际生效的结果｜读到：源端取设备语言的 `async` 函数没被 `await`，同时同步执行 `i18n.use(LanguageDetector).init({ lng: … })`，init 时 lng 还是空串；写错：规格 AC 照异步分支的映射写（如裸 zh 强制映射为繁体），与 init 那刻由检测插件实际裁决的语言不同
