# 前台服务转成的 backgroundModes 声明

agent 会看到什么：源端前台服务 startForeground(...)、foregroundServiceType（如 dataSync），目标 module.json5 里 backgroundModes 写在 abilities 还是 extensionAbilities 条目上

## 规矩

- rule-d34befd42ead｜backgroundModes 只写在 UIAbility 条目上，不写进 extensionAbilities｜读到：安卓源前台服务 startForeground(...)，foregroundServiceType 如 dataSync；或注册指引里写着扩展条目带 backgroundModes；写错：module.json5 的 extensionAbilities 条目里写了 "backgroundModes": ["dataTransfer"]
- rule-a25631ccf129｜申请 AUDIO_PLAYBACK 长时任务时，module.json5 补 backgroundModes 和权限｜写错：代码里有 startBackgroundRunning(…BackgroundMode.AUDIO_PLAYBACK…)，module.json5 的 abilities 项没有 "backgroundModes": ["audioPlayback"]，requestPermissions 里没有 ohos.permission.KEEP_BACKGROUND_RUNNING
