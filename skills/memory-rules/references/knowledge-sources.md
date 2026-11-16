# 知识库来源：怎么找、出处怎么写

写规矩时查事实只用下面三类来源，另加卡本身。每条事实在 `refs` 里留一条出处（给检查脚本核对原文），在 `values` 的 `source` 里写一个换一台机器也能用的出处（给审的人看）。

**本机的根目录和出处的写法。** `refs` 是库的一部分，换一台机器也要能核对，所以 `where` 只写来源里的相对路径（下面各节写明从哪一级算起），不写盘符、用户目录、安装目录、Gradle 缓存里带哈希的目录这类本机路径；路径一律用 `/`。各来源在这台机器上的根目录配在分支根目录下的 `work/sources.local.json`（不进版本库，样例和说明见 `skills/memory-rules/sources.example.json`；没配的按惯例找）。要打开来源文件时，先跑 `py -3 skills\memory-rules\scripts\check_rules.py --roots` 看根目录，用根目录接上相对路径；写进 `refs` 的只有相对的那一段。

## 1. 鸿蒙 SDK 的声明文件

**在哪。** DevEco Studio 安装目录下的 `sdk\default\openharmony\ets\`（Windows 上常见在 Program Files 下的 `Huawei\DevEco Studio\`）。HarmonyOS 专有的能力在 `sdk\default\hms\ets\`。版本看 `sdk\default\sdk-pkg.json` 里的 `apiVersion` 和 `version`。

- `ets\component\`：组件和它们的属性方法。一个组件一个文件，如 `text.d.ts`（`TextAttribute`）、`canvas.d.ts`（`CanvasRenderingContext2D` 等）、`image.d.ts`、`list.d.ts`；所有组件共有的属性（宽高、边距、背景、阴影、命中测试等）在 `common.d.ts` 的 `CommonMethod` 里，`ShadowOptions` 这类公共参数类型也在 `common.d.ts`。
- `ets\api\`：接口模块，文件名是模块名，如 `@ohos.window.d.ts`、`@ohos.multimedia.image.d.ts`；`ets\api\arkui\` 下是 UI 相关的类型（如 `Graphics.d.ts` 里的 `LengthMetricsUnit`）。

**怎么找。** 按类型名全文搜 `declare class X`、`declare interface X`、`enum X`、`X(value:`。一个方法前面常有好几段注释，按 `@since` 从旧到新排，最后一段是当前版本的说法，签名紧跟在最后一段注释后面。默认值、单位多写在注释的说明行或 `@default` 里。

**同族接口。** 做法落在某个参数类型或枚举上时，用它搜一遍（如 `(value: ShadowOptions`、`unit?: LengthMetricsUnit`），看还有哪些类的方法带它；写进 `values` 的最多 3 个最常用的，写出完整签名和所属的类，`meaning` 里注明「同族接口」，其余只在 `siblings_checked` 里写数量。落在事件名、通用方法这类没有专门参数类型可搜的接口上的，`siblings_checked` 写「无：」加原因。

**版本。** 卡里记的 SDK 版本（卡文件「环境」一行）和本机的不同时，照本机的声明核实，`version` 写本机的版本；卡里观察到的行为出自别的版本的，在规矩的 `unverified` 里注明。声明里写明的版本要求（`@since`）可以写进规矩的 `scope`，注明出自声明。

**出处怎么写。**
- `refs`：`kind` 写 `harmony-dts`；`where` 写相对鸿蒙 SDK 根目录（`sdk/default`）的路径，空一格再写符号名（`类名.成员名`），如 `openharmony/ets/component/text.d.ts TextAttribute.textShadow`、`hms/ets/api/@hms.collaboration.systemShare.d.ts ShareController.show`；`quote` 照抄原文（检查脚本去掉空白后比对，跨行的注释要把行首的 `*` 一起抄上），不超过 200 字；`version` 写如「API 23（HarmonyOS 6.1.0）」。
- `values.source`：「鸿蒙 SDK 的 ets/component/text.d.ts，TextAttribute.textShadow」——相对 `ets/` 的路径加符号名。`hms` 下的写「鸿蒙 SDK 的 hms/ets/…，符号名」。

## 2. 安卓 SDK：平台资源和框架源码

**在哪。** `%LOCALAPPDATA%\Android\Sdk\`。

- 平台资源：`platforms\android-<N>\data\res\`。`values\attrs.xml` 是属性的定义和格式（`format="float"`、`dimension`、`color`…），`values\themes*.xml`、`values\styles*.xml` 是主题和控件默认样式，`values\colors*.xml`、`values\dimens*.xml` 是框架的颜色和尺寸，`drawable*\`、`layout\` 是框架自带的图和布局。按应用的 compileSdk 取对应的平台；本机装了哪些平台，看 `platforms\` 下的目录。
- 框架源码：`sources\android-<N>\`，按包路径找，如 `android\widget\TextView.java`、`android\graphics\Bitmap.java`。

**怎么找。** 主题和样式按「控件 style → 祖先布局的 android:theme 覆盖 → Activity 主题 → 应用主题」一层层找到提供值的那一项，再顺着 `@android:color/…`、`?android:attr/…` 引用解析到具体值。行为看源码里读属性的那段（如 `readTextAppearance` 里的 `getFloat`、`getDimensionPixelSize`）。

**出处怎么写。**
- `refs`：`kind` 写 `android-sdk`；`where` 写相对 Android SDK 根目录、带平台版本的路径，加资源名或「类#方法」，如 `platforms/android-36/data/res/values/attrs.xml TextAppearance shadowRadius`、`sources/android-36.1/android/widget/TextView.java TextView#readTextAppearance`；`version` 写平台目录名，如「android-36」。
- `values.source`：平台资源写「Android SDK 平台资源 data/res/values/attrs.xml，资源名（按应用的 compileSdk 取对应平台）」；源码写类和方法，如「android.widget.TextView#setShadowLayer」。

## 3. 依赖库：Gradle 缓存里的资源

**在哪。** `%USERPROFILE%\.gradle\caches\`。解包后的 aar 在 `transforms-<N>\<hash>\transformed\<artifact>-<version>\`，较新的 Gradle 在 `<gradle 版本>\transforms\<hash>\transformed\<artifact>-<version>\`，资源在其中的 `res\` 下（合并的值多在 `res\values\values.xml`）。坐标里的 group 看 `modules-2\files-2.1\<group>\<artifact>\<version>\`。同一个库可能缓存了好几个版本，按应用依赖的版本取。

**依赖库的代码。** 本机的 Gradle 缓存里依赖库多半只有编译产物（jar、aar 里的 class），没有源码。依赖库代码里的事实（不是资源文件）查不到原文的，按卡写，并记进 `gaps`。

**出处怎么写。**
- `refs`：`kind` 写 `android-lib`；`where` 写库的坐标「group:artifact:version」，空一格写包内路径，再写资源名，如 `androidx.appcompat:appcompat:1.7.1 res/values/values.xml Base.TextAppearance.AppCompat`（不写 Gradle 缓存里带哈希的目录；坐标里的 group 看 `modules-2/files-2.1/` 下的目录）；`version` 写「group:artifact 版本」。检查脚本按坐标在本机的 Gradle 缓存里找（先找 aar，再找解包后的 transforms 目录），本机没有这个库时报「没能核对」，不算引文错。
- `values.source`：「androidx.appcompat:appcompat 包内 res/values/values.xml，资源名（按应用依赖的版本）」——坐标加包内路径加资源名。

## 4. OpenHarmony 官方文档（本地副本）

**在哪。** 分支根目录下的 `work\ohdocs\zh-cn\application-dev\`，只有 .md 文件，共 5,537 个、约 99 MB。现有的这份是从 GitHub 镜像 `https://github.com/openharmony/docs` 部分克隆加稀疏检出的（只取这个目录下的 .md），对应提交 `f41b9345badd47c7ab0c263344cd7f4b5a549afb`（2026-05-26，取于 2026-11-15；GitHub 镜像停在这一次，不再更新）。以后重建或更新改从 `https://gitcode.com/openharmony/docs.git` 克隆（它的 master 是新的），命令见 SKILL.md。现有引文（`version` 写「docs f41b9345」的）都是对着 f41b9345 核的；副本换了版本之后，要对全部候选和规矩重跑 `check_rules.py`，对不上的引文重新核对，并把这里和下面 `version` 的写法改成新的提交号。不进版本库。查文档只读这份副本，不联网。

**怎么找。** 总目录页是其中的 `Readme-CN.md`；目录页里的链接是相对路径，从当前文件所在的目录接上去就是文件。各部分有自己的目录页，例如 `ui\Readme-CN.md`（开发指南）、`reference\Readme-CN.md`（API 参考，每个 Kit 是 `reference\apis-<kit>\Readme-CN.md`）。从目录页顺着链接找确切的文件，不用猜。文档和本机声明文件不一致时以声明为准（副本的版本可能比本机 SDK 旧）。

**出处怎么写。**
- `refs`：`kind` 写 `oh-docs`；`where` 写文档库里的相对路径（从 `zh-cn/` 算起），空一格再写小节名，如 `zh-cn/application-dev/quick-start/app-configuration-file.md 配置文件标签`；`quote` 照抄原文，检查脚本照本机文件核对；`version` 写「docs f41b9345」。
- `values.source`：文件名加小节名，写成「<文件名>.md，<小节名>」。

## 5. 源端不是安卓的

源端是 Web 框架、Flutter 等时，三类来源里多半查不到源端的行为。查不到的写进 `lookups`（去源工程的哪类文件里按什么找）或 `gaps`，不硬凑出处。

## 6. 出自卡的

卡里修好并上机验证过的做法和观察到的行为，`values.source` 写「卡里修好并验证过」，`support` 标卡的结论（多半是 `diagnosis`）。卡里的做法和知识库冲突时不改做法，冲突记进卡一级的 `conflicts`；`gaps` 只记想查而没查实的。

## 呈现的各栏里不能有的

规矩的各栏都会给审的人看、用于召回，或者随库发布（`refs`），都不能出现：盘符路径（`C:\`）、用户目录（`Users\…`、`AppData`、`%LOCALAPPDATA%`、`%USERPROFILE%`）、`Program Files`、`.gradle`，以及「文件名:行号」这种写法。要指一个文件时用上面各节「`values.source`」那一行的写法。
