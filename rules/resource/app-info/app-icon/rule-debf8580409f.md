# AppScope 分层图标用安卓 launcher 图标生成，不留模板占位图

审的是：资源
触发（任一种）：
- 读到：AndroidManifest 的 application android:icon 指向 launcher 图标（drawable 或 mipmap 资源）；写错的样子：AppScope/resources/base/media 下分层图标的 foreground、background 仍是模板占位图
适用范围：在已有模板工程上迁移、进 Stage 1 前落地应用身份时
做法：
- 用安卓 launcher 图标生成前景和背景资源放进 AppScope/resources/base/media，替换模板占位图；app_layered_image.json 写 {"layered-image": {"background": "$media:background", "foreground": "$media:foreground"}}，app.json5 的 icon 引用它
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- {"layered-image": {"background": "$media:background", "foreground": "$media:foreground"}}，放在 AppScope/resources/base/media：分层图标资源文件的写法（出处：layered-image.md，配置分层图标和应用名称）
- app.json5 的 icon：应用图标，取值为图标资源文件的索引，支持单层和分层图标，不可缺省：AppScope 图标的引用位置（出处：app-configuration-file.md，配置文件标签）
针对本应用要查的：
- 安卓 launcher 图标文件：源工程 AndroidManifest.xml 的 application android:icon（及 android:roundIcon）指向的资源，在 res/mipmap-*/ 或 res/drawable-*/ 下按名字找；取最高密度的那份（或 adaptive-icon 的前景、背景）生成鸿蒙的 foreground、background
未核实：卡里图标是由脚本从安卓 launcher 图标重新生成的，二进制内容只能从回执核对
来源：1 张卡，1 个应用
- case-224eb9de83aa652829f4（android-panorama-map-vest7）：做法第 1 步 ← 建议 2、诊断
