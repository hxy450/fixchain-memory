# startWindowIcon 指向的 startIcon.png 仍是模板图时，换成安卓启动图标缩放的图

审的是：资源
触发（任一种）：
- 读到：安卓有 `mipmap-*/ic_launcher`、`ic_launcher_round` 启动图标（AndroidManifest 的 android:icon / android:roundIcon）；写错的样子：目标 module.json5 的 `startWindowIcon` 指向的 `startIcon.png` 仍是脚手架模板图（尺寸、哈希与模板相同）
适用范围：迁移工程落地 App 身份时 entry 模块 base/media 下的启动窗图标
做法：
- 取安卓最高密度的启动图标（mipmap-xxxhdpi 的 ic_launcher_round，或自适应图标的前景）缩放成 144×144，写入 entry/src/main/resources/base/media/startIcon.png，module.json5 abilities 的 startWindowIcon 仍指向它
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- startWindowIcon：UIAbility 启动页面图标资源文件的索引，不可缺省：module.json5 abilities 里的必填项，指向 base/media 下的启动图标（出处：module-configuration-file.md，abilities标签）
- startWindowIcon 的图标资源在启动页面上按实际大小居中显示，不随窗口缩放：图的像素尺寸就是显示尺寸，要先缩放好再写入（出处：launch-page-config.md，配置简易启动页）
- mipmap-xxxhdpi 的 ic_launcher_round 缩放成 144×144 写入 startIcon.png：修复时的做法，替换后启动窗不再是模板图（出处：卡里修好并验证过）
针对本应用要查的：
- 安卓端用的启动图标：源工程 AndroidManifest.xml 的 application 标签的 android:roundIcon / android:icon，顺着 @mipmap/ 找到 res/mipmap-xxxhdpi 下的位图；mipmap-anydpi-v26 下是 adaptive-icon 时看它的 foreground；取最高密度的位图（或前景图）作为缩放来源
来源：1 张卡，1 个应用
- case-1f6d95134bba8edf5ba6（jerboa）：做法第 1 步 ← 诊断、建议 2；取值 3 ← 诊断
