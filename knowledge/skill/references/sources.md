# 去哪查、出处怎么写、版本怎么记

规则编号见 `rules.md`（N1–N6 是这一份的提要）。

## 1 去哪查（先后和谁说了算）

写知识的人可以联网，但只取一手来源（第 2 节）。按要核的是什么，去不同的地方，各有说了算的一方：

| 要核的 | 看哪里 | 说了算 |
|---|---|---|
| 鸿蒙接口存不存在、签名、从哪一版开始有（`@since`）、废弃没有 | 本机鸿蒙 SDK 的声明文件（`.d.ts`，含注释） | 本机 SDK 声明 |
| 鸿蒙一侧的行为、默认值、单位、时序 | OpenHarmony 文档仓库的最新 master（每次开工先跑 `scripts/sync_ohdocs.py` 同步，读同步目录；单篇也可以取原文链接） | 文档 master |
| 运行时实际表现（设备上看到的、编译器报的） | 来源卡里的上机实测、编译实测 | 卡里实测 |
| 安卓框架的行为和默认值 | 本机 Android SDK 的框架源码和平台资源；本机没有的版本或文件，取 AOSP 源码站 | 源码 / 平台资源 |
| 安卓官方说明 | 安卓官方参考文档 | 和源码不一致时静态事实以源码为准（`rules.md` U1），两者都写 |
| 依赖库的默认样式和行为 | 本机 Gradle 缓存里的 aar / jar（资源；代码看字节码）；或这个版本的源码包、它在官方仓库里对应版本的源码 | 对应版本的库 |

**三者冲突时**（声明、文档、卡里实测说法不一样）：条目里写清各自说了什么、以哪个为准，按上表「说了算」的那一列定；正文需要改的照 `rules.md` U1 写改句。例：文档写「API 10 起默认 true」、声明注释写 `@since 11`——以声明为准，事实写 API 11，可注明文档的说法；声明注释示例是连字符、卡里设备上是下划线——运行时以卡里为准，写清两种写法（`examples.md` 例 1、例 17）。

旧的本机文档副本不作出处，一律用同步的 master。

## 2 一手来源（只用这些；博客、问答、第三方教程一律不用）

| 来源 | 位置或网址 |
|---|---|
| 鸿蒙 SDK 声明 | DevEco Studio 安装目录下 `sdk/default/openharmony/ets/`（`component/`、`api/`、`kits/`），HarmonyOS 专有能力在同级 `hms/ets/`；版本看 `sdk/default/sdk-pkg.json` |
| OpenHarmony 文档 | 仓库 https://gitcode.com/openharmony/docs ，只用 master 的 `zh-cn/application-dev/`；入口 https://gitcode.com/openharmony/docs/blob/master/zh-cn/application-dev/Readme-CN.md ；本机同步目录由 `scripts/sync_ohdocs.py` 建和更新；单篇原文 `https://raw.gitcode.com/openharmony/docs/raw/master/<仓库内路径>`（`gitcode.com/…/raw/…` 返回的是网页，不能用） |
| 安卓框架源码和平台资源 | Android SDK 的 `sources/android-<N>/`、`platforms/android-<N>/data/res/`；本机没有的取 AOSP：https://android.googlesource.com/ 、https://cs.android.com/ |
| 安卓官方参考文档 | https://developer.android.com/reference/ （或 https://developer.android.google.cn/reference/ ） |
| 依赖库 | 本机 Gradle 缓存；源码包和官方仓库：https://maven.google.com/ 、https://dl.google.com/android/maven2/ 、https://repo1.maven.org/maven2/ 、androidx 在 AOSP 的 `platform/frameworks/support` 或 https://github.com/androidx/androidx/ 、Material 组件 https://github.com/material-components/material-components-android/ ；取和应用依赖的版本对应的 tag |
| 来源卡 | 经验库 `store/cases/<卡号>/` 下的卡片 JSON（诊断、建议、没核到的点） |

`scripts/check.py` 把出处里的网址对着这张表的前缀查（`FIRST_HAND`），别的网址报错。

## 3 怎么找

核一条事实要读全，用工具读：文档取整节（`ohdocs_section.py`），安卓资源查全部限定目录、整条 parent 链和库的最旧、最新两版（`android_res.py`），鸿蒙声明列出同名的每一处（`dts_lookup.py`）。这三个工具的默认输出就是「全的」。理由和细则见 `rules.md` V6a：独立抽查里有出入的条目大多是只读了出处的一处——漏了同一小节的例外、同一方法的其他分支，或者安卓 style、主题只看了 `values/` 里那一份。工具的用法和已知限制见 `tools.md`。

安卓资源照 `android_res.py` 小结里「★常见手机竖屏」命中的那一份为主写、同时写出横屏、平板等配置下的取值（只写 `values/` 那一份会漏 `values-h720dp` 这类变体）；「从 X 版起才有」要从 Google Maven、Maven Central 取中间版本逐版确认到「上一版没有、这一版有」，找不准写「至少在 X 版已有，更早未核」；核代码行为要读到调用它的上下游（之前的预处理、字段是否已设），不只读被引用的那个函数（`rules.md` V6a 第 6–8 条）。

- **鸿蒙声明。** 按类型名搜 `declare class X`、`interface X`、`enum X`、`X(value:`。一个方法前常有几段注释，按 `@since` 从旧到新排，最后一段是当前版本的说法，签名紧跟其后；**「从哪一版开始有」取首段的 `@since`**，不取最后一段的。`scripts/dts_lookup.py` 打印匹配行前面最后一段注释和所属类型，并在标题行另外打印首段的 `@since`；默认把同名的每个重载、每处声明都打出来，末尾打总数。
- **文档。** 在同步目录里从 `zh-cn/application-dev/Readme-CN.md` 顺着相对链接找文件，或按文件名找（`scripts/ohdocs_link.py --root <同步目录> --find <文件名>`）；不猜文件名。找到以后用 `scripts/ohdocs_section.py <同步目录> <文件> <小节名或关键词>` 取**整节**来读：从这个标题到下一个同级或更高级标题，「说明」「注意」「警告」块都在内；同名小节（如 deprecated 旧版）一并打出；上级小节开头的说明块（如模块的起始版本）也打出；末尾列出同一文件里别处提到这个关键词的小节标题，逐个看有没有例外。文档讲到的版本超出本机 SDK 的，条目里注明。
- **安卓主题和样式。** 按「控件 style → 祖先布局的 android:theme → Activity 主题 → 应用主题」一层层找到提供值的那一项，再顺着 `@android:color/…`、`?android:attr/…` 解析到值；行为看源码里读属性的那段。用 `scripts/android_res.py` 查：`style <名字> --item <属性>`（主题里的某一项）、`color|dimen|bool|integer <名字>`（平台色值、尺寸）、`attr <名字>`（声明和在常见主题里的取值）；它在全部 `values*` 限定目录里找每一处定义，顺着 parent（显式的和名字里点号的隐式父）查到底并打印每一层的取值，`?attr`、`@color` 解析到字面值（颜色状态列表取默认状态那一项，算上 alpha），`--api` 可给几个 API 级别并排比。**顺着 parent 查时，每一层都要看它在 `values-vNN` 等限定目录里有没有重定义，不能只看 `values/` 里那一份**（重定义可以换掉 parent）。默认值随 API 级别、夜间模式、父主题、库版本变的，照它的「小结」各段分别写出来（第 4 节）。
- **依赖库。** `android_res.py --lib <组:库>` 在 Gradle 缓存里找这个库的各版 aar，**默认对最旧和最新两个正式版各查一遍**并标出两版不同的层，`--version` 指定应用依赖的那一版；库的主题链走到 `android:` 开头的父主题时接着查平台资源（几个库要一起查时 `--lib` 给几次，如 material 加 appcompat）。依赖库至少看最旧和最新两个版本，两版不同的写版本范围。代码事实看字节码，或取同版本的源码包、官方仓库同版本 tag 的源码。
- **卡。** 卡里验证的条目要回到来源卡核：卡里写的是设备上看到的现象，还是一次返修的做法（`rules.md` T1）。卡里引历史会话里模型思考的句子不摘抄、不转述；卡里点到的转录文件和行号、应用源码和迁移工程的路径不去找。

## 4 版本怎么记（两层）

**文件一层**：`sdk` 键记这一份知识核实时的环境（格式见 `knowledge-format.md` 第 1 节）：

| 键 | 写什么 | 例 |
|---|---|---|
| `verified_on` | 核实日期 | `2026-11-21` |
| `docs_commit` | 文档用的是 master 的哪个提交（`sync_ohdocs.py` 打印的） | `e42bd18a89ff75e48e3effdf3d58748376c2caec` |
| `docs_date` | 那个提交的日期 | `2026-11-21` |
| `harmony` | 本机鸿蒙 SDK 的版本，写明 API 几 | `HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）` |
| `android` | 安卓平台资源、源码和各依赖库的版本；没用到写「不涉及」 | `平台资源 android-34（另比对 android-30/33）；源码 android-36.1；appcompat 1.7.1、material 1.12.0` |

**条目一层**：只有随版本变的事实才写条件，不随版本变的不写。

- 文档里写了「从 API version N 开始」「API version N 起行为变更」之类的，把条件写进事实（例：「自 API 11 起默认 true（API 9 默认 false）」）。
- 文档讲的内容超出本机 SDK 版本的（文档 master 比本机 SDK 新），要注明（例：「……（API 26 起，超出本机 SDK 的 API 23）」）。`check.py` 会列出提到的 API 高于本机却没注明的条目。
- 安卓一侧的默认值取决于应用用的父主题和库版本，写成带条件的：哪个父主题、哪个版本范围下是什么（例：「Theme.Material.Light 下 textColorSecondary 的透明度 android-30 为 0.54、android-33 起为 0.60」「Widget.MaterialComponents.Button（material 1.x）……」）。
- 不设条数上限。

## 5 出处（`source`、`basis`）怎么写

几处出处用「；」连。不写本机路径（盘符、用户目录、安装目录的绝对路径）和行号（「文件:行号」「#L12」「;l=12」「第 N 行」）。工具输出里的行号只供自己读，不抄进出处。

| 来源 | 写法 | 例 |
|---|---|---|
| OpenHarmony 文档 | `https://gitcode.com/openharmony/docs/blob/master/zh-cn/application-dev/<路径>.md，<小节名>`；本机同步目录里的路径用 `scripts/ohdocs_link.py` 换成链接 | https://gitcode.com/openharmony/docs/blob/master/zh-cn/application-dev/reference/apis-arkui/arkui-ts/ts-types.md，Length |
| 鸿蒙声明 | 鸿蒙 SDK 的 ets/<相对 ets 的路径>，<类名.成员名>（hms 下写 hms/ets/…） | 鸿蒙 SDK 的 ets/component/image.d.ts，ImageAttribute.draggable |
| 安卓源码 | <包.类>#<成员>；取自 AOSP 时可写 AOSP 的链接（到 tag，不带行号） | android.widget.ImageView#configureBounds |
| 安卓平台资源 | Android SDK 平台资源 data/res/<路径>，<资源名> | Android SDK 平台资源 data/res/values/config.xml，config_minScalingSpan |
| 安卓官方参考文档 | 链接，加成员名 | https://developer.android.com/reference/android/view/ViewConfiguration，getLongPressTimeout |
| 依赖库 | <group:artifact> <版本>，<类或资源名>；资源写「包内 res/…」；看的是字节码的注明；取自源码包或官方仓库的可写链接（到对应版本的 tag） | androidx.compose.foundation:foundation 1.10.3，ImageKt#Image |
| 构建工具 | DevEco Studio 的 <工具>，<相对路径>（<符号>） | DevEco Studio 的 hvigor-ohos-plugin，src/tasks/build-profile-task.js（BuildProfileTask） |
| 卡 | 卡里修好并验证过 / 卡里上机实测（<卡号>，<怎么测的>）/ 卡里编译实测（<卡号>） | 卡里上机实测（case-1071843a480186d94d42） |

链接只写在 `source`、`basis` 里；`fact`、改句的新句里不放链接（交给模型的那段不带出处和链接）。

**旧格式文件的写法（只用来读仓库里已有的旧文件）：** 文档写「文档 <文件名>.md，<小节名>」，按文件名找；版本只在 `sdk` 里写一句（`harmony`、`android` 两个键），没有核实日期和文档提交号。`check.py` 两种写法都认：`sdk` 里没有 `verified_on`、`docs_commit`、`docs_date` 的旧文件不要求链接；新写的文件（或加 `--require-new`）文档出处必须是链接。

## 6 哪些出处能用脚本核

`scripts/check.py --sources`：鸿蒙声明、安卓源码、安卓平台资源、文档（链接按仓库内路径、旧写法按文件名，在 `--docs` 给的同步目录里找文件和小节名）能核；依赖库、卡里、AOSP 和官方参考文档的网址不核，要人看。`--docs` 给了时，文件的 `docs_commit` 和同步目录现在的提交不同会列出来（文档 master 后来更新过）。
