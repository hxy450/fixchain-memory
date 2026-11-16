# 派应用身份或外壳任务时，把 app.json5 的 configuration 与 icon、版本号并列核对

审的是：计划与派工
触发（任一种）：
- 读到：决策台账判大字体为迁移，或源端有随系统字号缩放的文本；写错的样子：应用身份 / 应用外壳的派工范围只列 app_name、versionName、versionCode、icon，没有 app.json5 的 configuration，完成自检里也没有核对 profile
适用范围：派发应用身份、应用外壳一类改 AppScope/app.json5 的任务时
做法：
- 派工核对项里把 app.json5 的 configuration 与 label、icon、版本号并列；完成自检写明：configuration 引用的 profile 文件存在，fontSizeScale 等取值与决策一致
来源：1 张卡，1 个应用
- case-a824609ada4969e6d96c（2048）：做法第 1 步 ← 建议 3
