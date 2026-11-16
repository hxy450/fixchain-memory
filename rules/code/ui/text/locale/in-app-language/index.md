# 应用内切换语言与语言名

agent 会看到什么：源端用 AppCompatDelegate.setApplicationLocales / getApplicationLocales、supported_locales 做应用内语言切换并 recreate，或用 Locale.getDisplayName 生成语言名；目标端有 i18n.System.setAppPreferredLanguage / getAppPreferredLanguage、语言表和切换后取串的刷新

## 规矩

- rule-bf89281250ed｜规格要求保存后立即切换语言时，setAppPreferredLanguage 外还要 setLanguage 并刷新文案｜读到：规格验收条目写「保存后应用界面语言立即切换」；源端应用内按 supported_locales 切换语言；写错：只调 i18n.System.setAppPreferredLanguage(...)，注释称无需手动刷新；已显示的 getStringSync 文案不重取
- rule-dced15db178a｜代码里用 getStringSync 取成字符串的文案，语言运行期切换时在同页配置变化回调里重取｜读到：源端在组合期取串拼接运行时值（如 stringResource(R.string.x) + BuildConfig.VERSION_NAME），切换语言靠 Activity recreate 后按新语言重取；写错：页面在 aboutToAppear 里 resourceManager.getStringSync($r('app.string.x').id) 取一次存进 @Local / @State 或作 string 参数下传，配置变化回调里没有重取
- rule-b3073c1fc051｜源端未设语言回退 English 时，另记显式设置的 tag，不只靠 getAppPreferredLanguage｜读到：Locale.lookup(AppCompatDelegate.getApplicationLocales()…) ?: Locale.ENGLISH，未设置应用语言时回退 English；写错：目标用 i18n.System.getAppPreferredLanguage() 匹配当前语言，最后回退 en，没有「未设置 → English」这一分支
- rule-80c0b4036504｜源端用 Locale.getDisplayName(自身) 生成语言名时，按 ICU 实际输出建表，不凭记忆改大小写｜读到：Kotlin 里 map.put(it, it.getDisplayName(it)) 一类，用 Locale.getDisplayName(本 locale) 生成语言自称；写错：目标手写语言表，把 Français、Español、Dansk、Italiano、Русский 这类自称写成首字母大写（ICU 自称是 français、español、dansk、italiano、русский）
