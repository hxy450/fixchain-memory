# 应用身份和外壳派工的核对范围（app.json5 configuration）

agent 会看到什么：读到决策台账判大字体为迁移，或源端有随系统字号缩放的文本；应用身份 / 应用外壳的派工范围只列 app_name、versionName、versionCode、icon，没有 app.json5 的 configuration，完成自检里也没有核对 profile

## 规矩

- rule-4d835b4ce9c1｜派应用身份或外壳任务时，把 app.json5 的 configuration 与 icon、版本号并列核对｜读到：决策台账判大字体为迁移，或源端有随系统字号缩放的文本；写错：应用身份 / 应用外壳的派工范围只列 app_name、versionName、versionCode、icon，没有 app.json5 的 configuration，完成自检里也没有核对 profile
