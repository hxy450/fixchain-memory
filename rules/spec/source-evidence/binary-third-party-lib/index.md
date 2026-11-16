# 仓库里没有源码的三方库（二进制依赖）

agent 会看到什么：读到 Gradle 依赖里的三方库坐标（implementation、@aar、jar、libs.versions.toml），源码只 extends 或调用库类、布局里只有库的自定义 View，库的源码和资源不在仓库里；规格写「源码不在本仓库」「内部 UI 不可见 → 自研」「默认样式即可对齐」「待核自由度」，或跨栈映射只写「→ Toast / 自研 / 自实现」、把猜出的库行为写成确定契约

## 通用查法

### 外观或行为由仓库外三方库决定时，按坐标取库制品写真值，取不到登记缺口

审的是：规格
触发（任一种）：
- 读到：依赖里有三方库坐标（implementation、@aar），源码只 extends 或调用库类、布局里只有库的自定义 View，仓库里没有库源码；写错的样子：规格写「源码不在本仓库」「内部 UI 不可见 → 自研」「默认样式即可对齐」「待核自由度」，或跨栈映射只写「→ Toast / 自研」，没有库里的尺寸、缺省值、行为和出处，也没登记缺库真值
适用范围：规格里写由 AAR / jar 三方库决定的外观和行为时
做法：
- 从构建脚本 dependencies、libs.versions.toml 或 import 包名读出 group:artifact:version，到 Gradle 缓存 modules-2/files-2.1/<group>/<artifact>/<version>/ 下取 aar、jar 或 sources jar；没有就解析依赖或从库的官方仓库取同版本
- 解包读 res/layout*、res/values*、res/drawable，反编译 classes.jar 或用 javap -p -c -constants 读构造缺省和常量，把尺寸、缺省值、行为连同库版本写进规格
- 确实取不到制品时登记缺库真值的阻塞或待核，不写无证据的替代裁定或确定契约
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 只有编译后的 jar、没有 sources jar 也能读：javap -p -c -constants 反汇编出缺省值和常量：「库源不可查」不成立（出处：卡里修好并验证过）
针对本应用要查的：
- 三方库的坐标、版本和制品：源工程 Gradle 构建脚本的 dependencies、版本目录 libs.versions.toml、源文件的 import 包名；Gradle 用户缓存 caches/modules-2/files-2.1/<group>/<artifact>/<version>/ 下的 aar、jar、sources jar，或解包后的 transforms 目录；缓存里有就解包；没有就让 Gradle 解析依赖或按版本从库的官方仓库取，再读 res 和类
未核实：生成环境能否联网或运行 Gradle 解析依赖，卡里没有记录
来源：3 张卡，3 个应用
- case-087050b57a3e1a6ac4ce（jerboa）：做法第 1 步 ← 建议 1；做法第 3 步 ← 建议 1
- case-49a2270970314f62c95f（GameOfLife）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1；取值 1 ← 诊断
- case-74b07cb94daa311f36b1（omni-notes-hmos）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1；做法第 3 步 ← 建议 1

## 规矩

- rule-935d18e8df29｜第三方 TextView/Dialog 库登记进跨栈基线时，写明截断策略、行距倍数和默认装饰｜读到：Gradle 构建脚本的 implementation 里有第三方 UI 库的二进制依赖（如 pixlui、material-dialogs），布局用库里的 TextView / EditText / Dialog 子类；写错：跨栈映射基线里这个库只登记成「自定义字体 TextView → ArkUI Text .fontFamily()，L2 Auto」或「→ CustomDialog」，没有截断策略、行距倍数、默认装饰三项
- rule-480f89de4812｜实体继承二进制依赖里的基类时，规格逐项写基类契约，查不到的标「未知」｜读到：源实体 `class X extends` 一个来自 Maven/JitPack 二进制依赖的基类，主工程里没有基类源码；写错：规格字段表和序列化契约只写「主仓无源码」，基类的字段类型、无参构造缺省值、equals/isChanged/toString、JSON 键序与类型既没有给出契约，也没有标「未知」，后面靠可见的子类代码推断
- rule-d118daaf9a79｜UI 由三方库渲染时，规格先取库制品写真值，取不到就登记缺库真值，不写默认样式可对齐｜读到：源码只有 extends 三方库类（如 extends AppIntro2）、壳布局或调用代码；UI 快照只剩库的自定义 View 类名（如 com.appeaser.sublimepickerlibrary.SublimePicker、com.larswerkman.holocolorpicker.ColorPicker）；依赖里有该库坐标和版本；写错：页面规格的转换决策写「三方库内部 UI 不可见 → 原生组件自研 / 二选一」「默认样式即可对齐」「源码不在本仓库 → 无 anchor」，没有库内几何和交互，也没有缺库真值的阻塞项
- rule-f8f7b40172b5｜三方手势控件在仓库里没源码时，规格去 AAR 核对交互或登记缩放双击缺口｜读到：源布局用三方库的缩放图片或画廊控件（如 `TouchImageView`、自定义 `ViewPager`），仓库里找不到它的源码；写错：规格写「三方库无源码 → Swiper + Image 自渲染」，没写缩放、双击行为，也没登记行为缺口
- rule-5171465e444e｜三方 UI 库布局不在仓库时，规格记依赖坐标并盘点 aar 里的 layout-land 等变体｜读到：源工程依赖三方 UI 库（选择器、弹窗等），它的布局不在仓库源码里，只在 aar 资源中；写错：规格没记这个库的依赖坐标，也没盘点它的 layout-land、layout-w<N>dp、values-h<N>dp 等变体；以「源码不在本仓库」当作没有横屏分支的依据
- rule-e10d29166ff6｜源调用只给二进制三方库组件部分参数时，规格写库缺省的实值，不标「待核自由度」｜读到：源码调用三方库组件（Kotlin 类构造带缺省参数）只显式传了几个参数，其余外观与运动参数没传；仓库里没有库源码；写错：规格映射行或验收写「库内部默认参数源码未出现——待核自由度，不写成判据（未在本机核对）」，没有缺省颜色、形状、尺寸、寿命等实值
- rule-9fe2ceb08b71｜承载 UI 行为的第三方库只映射成 Toast / 自研时，规格写出库的契约字段或登记 PD-*｜读到：Gradle 依赖清单里有承载提示条、FAB 菜单、对话框、色板的第三方库（如 de.keyboardsurfer.android.widget:crouton、com.getbase:floatingactionbutton、material-dialogs、HoloColorPicker，常带 @aar）；写错：跨栈映射行只写「promptAction Toast / 自定义 toast 组件」或「ArkUI 自研」一词并标 Auto，没有库本身的队列、时序、尺寸、动画、触摸语义字段，也没登记 PD-*
- rule-aa1009ee1e10｜规格把 prettytime 这类第三方格式化库映射成自实现时，写清库的行为契约和移植来源｜读到：依赖清单里有 org.ocpsoft.prettytime:prettytime 这类格式化库，源函数体只是调用 PrettyTime(Locale.getDefault()).formatDuration(...)；写错：跨栈映射写成「prettytime | 自实现（已有算法可直译）」，没写 locale 来源、单位与舍入、语言回退、只在 en 生效的缩写分支，也没指明移植来源
- rule-ec3ff7561080｜源端功能由二进制三方库决定、库实现取不到时，规格把库行为标为待核，不写成确定契约｜读到：源端调用二进制三方库完成导出导入（如 RoomDBExportImport(...).export(ctx, uri) / import(ctx, uri, true)），库源码和 AAR 本地查不到；写错：规格把库内部行为（归档条目名、参数语义、调用后的链路）写成精确常量、AC 真值或跨端工件契约，没有登记待核或阻塞
- rule-e8e47343855f｜调用点的布尔实参不从值推断含义，核库签名；恢复后重启就把「应用重启」写进 AC｜读到：源端调用点只露出含义不明的布尔实参，如 import(ctx, uri, true)；写错：规格按实参猜含义（如解释成整库替换 replace），导入链写成「替换 → 重开连接 → 内存状态重载 → Toast」，AC 拿调用行作真值
