# 工具用法和已知限制

`scripts/` 下八个脚本都只用 Python 标准库（`sync_ohdocs.py` 和 `check.py --docs` 调 git），都只读（`render.py --out`、`candidates.py --out` 只写指定的地方）。本机路径一律从参数或环境变量来，脚本里不写。下面尖括号里换成自己机器上的路径。

## 1 常用命令

```
py -3.12 -B -X utf8 scripts/sync_ohdocs.py <文档同步目录> [--show | --dry-run]
py -3.12 -B -X utf8 scripts/candidates.py --from-case-files links --memory <memory> [--base-memory <归并前的阅读包> [--new-cards-only]] lesson-<id> …
py -3.12 -B -X utf8 scripts/candidates.py --from-case-files <库>/store/cases --memory <库>/memory lesson-<id> …
py -3.12 -B -X utf8 scripts/ohdocs_link.py --root <文档同步目录> --find <文件名.md>
py -3.12 -B -X utf8 scripts/ohdocs_section.py <文档同步目录> <文件名或路径> <小节名或关键词> [--also 关键词 …] [--all]
py -3.12 -B -X utf8 -I scripts/dts_lookup.py <.d.ts 文件> <正则> [maxhits]
py -3.12 -B -X utf8 scripts/android_res.py style <名字> [--item <属性>] [--theme <主题>] [--api N …] [--lib 组:库 …] [--version V | 组:库=V …]
py -3.12 -B -X utf8 scripts/android_res.py color|dimen|bool|integer|fraction <名字> [--theme <主题>] [--api …] [--lib …]
py -3.12 -B -X utf8 scripts/android_res.py attr <名字> [--theme <主题> …] [--lib …]
    android_res.py 都可加：--sdk <安卓 SDK> --gradle <Gradle caches 目录> --phone sw=360-412,h=660-915,dpi=xxhdpi --tablet sw=600-800,h=960-1280,dpi=xhdpi
py -3.12 -B -X utf8 scripts/check.py <知识文件或目录 …> --memory <memory> --require-new --docs <文档同步目录> [--app-name <被迁移应用名> …]
        [--sources --oh-ets <鸿蒙 SDK>/openharmony/ets --hms-ets <鸿蒙 SDK>/hms/ets --android-platforms <安卓 SDK>/platforms --android-src <安卓 SDK>/sources/android-<N>]
py -3.12 -B -X utf8 scripts/render.py <知识文件或目录> [--memory <memory>] [--out <目录>]
```

每个脚本 `--help` 打印用法。

## 2 两个检查脚本、两个渲染脚本的分工

| | skill 里的（`knowledge/skill/scripts/`） | 仓库里的（`knowledge/`） |
|---|---|---|
| 谁用 | 写知识、复核、抽查的人 | 并入仓库、维护仓库的人 |
| `check.py` | 新格式的全部格式规则；`--memory` 或 `--bodies` 核改句套得上；`--app-name` 查应用名；`--docs` 比文档提交；`--sources` 拿出处到本机的鸿蒙 SDK、安卓 SDK、文档同步目录里核 | 同一套新格式规则，外加第三版、第七版两种旧格式；只对仓库里的 `memory/` 核改句；**不核本机出处** |
| `render.py` | 给任意目录的知识文件和正文出预览（`--with-source` 可带出处给人看） | 渲染仓库里的全部知识文件到 `knowledge/rendered/` |

两个渲染脚本对新格式文件、同一份正文的输出逐字节相同；仓库那份认新格式的判据是「`sdk` 里有 `docs_date` 或 `docs_commit`」。写完、复核完用 skill 的 `check.py` 把错误改到 0；并入仓库时再跑仓库的 `check.py`（不加 `--legacy-ok`，留作评测的应用名用 `--app-name` 传，不写进仓库）和 `render.py`。

## 3 收候选：卡里哪些字段带平台事实

一张卡（schema `migloop-case/*`）：`title`、`when`、`description`（情境）；`summary`（= 结论 diagnosis：调查经过、上机或编译看到的现象、返修怎么改的）；`recommendations[N-1]`（= recommendation:N：给下次的做法，常带接口名、取值、默认值、错误码）；`graphs[].nodes[].reason`（谁读了什么、在哪写错，常引历史会话里模型的思考）；`unknown`（没核到的点）；`metadata.environment`（鸿蒙 SDK、安卓 compileSdk、工具链版本）。

- `candidates.py --from-case-files` 机械收的：建议句、诊断里的现象 / 修法 / 声明文档句、没核到的点、环境版本（`rules.md` C5）。
- 收不到、要人读卡另列的：没有接口名的平台行为、和思考记录同句的平台表现、现象的成立条件、修法接口在声明文档里的事实（签名、@since、同族接口）、源端背后的安卓框架或库行为（`rules.md` C6）。
- 经验引了哪几张卡、引的哪条结论，看阅读包里这条经验的「## 来源」：每张卡一行「- [卡号](相对链接) · 结论：diagnosis, recommendation:N」，下一行「  卡片版本：`…`」。只有 `export --link-cards` 导出的阅读包有链接；`links` 模式靠它找卡，store 挪过位置时改给 `--from-case-files <store>/cases`。
- `--base-memory` 给归并开工前的阅读包，脚本据此列出正文改了哪几部分（「改动的部分」）、哪几张是新卡；`--new-cards-only` 只收新卡。

已知限制：句子的筛法是正则——没有标识符的平台行为句收不到；建议里「不要凭记忆」一类的话照收（那是制卡人写的）；应用自己的变量名、类名认不全，行里会留着，写知识时不带进去。带思考字样的整句（到句号）跳过，会连带丢掉同句里的平台事实，这是故意的，靠 C6 人读补。

## 4 文档：`sync_ohdocs.py`、`ohdocs_link.py`、`ohdocs_section.py`

- `sync_ohdocs.py`：目录不存在就浅克隆、稀疏检出 `zh-cn/application-dev/**/*.md`；存在就拉到最新 master（工作区有改动时不拉）。打印的提交号和日期填进 `sdk`。几个人共用一个同步目录时，只由协调的人在开工前拉一次，写的人只跑 `--show`（只读，不联网）；拉的时候脚本加锁，已有锁就不拉。要 git 2.25 以上。
- `ohdocs_link.py`：同步目录里的路径 ↔ 出处链接；`--find` 按文件名找文件。
- `ohdocs_section.py`：标题全等（忽略 `<sup>`、反引号、大小写）优先，没有再按包含；打印整节（到下一个同级或更高级标题，不截断），同名小节（如 deprecated 旧版）都打；各级上级小节开头的「说明 / 注意 / 警告」引用块和提到关键词的段落；同一文件里别处提到关键词的小节标题和处数；出处写法（链接加小节名）。例：`ts-universal-attributes-drag-drop.md draggable` 那一节写「默认情况下，组件不允许拖拽」，而上级小节开头写 Search、TextInput 等默认支持拖出——只读那一节会漏，工具在「上级小节开头提到关键词的段落」里打出来。

已知限制（`ohdocs_section.py`）：只在一个文件里找，类型定义在别的文件的（如 `SystemBarProperties` 在 `arkts-apis-window-i.md`）要另跑一次；「说明」块只认 `>` 引用块，表格单元格里的「说明：」随整节打出、不单列；关键词按子串、不分大小写匹配，短关键词列出的小节多。工具输出里有行号，只供自己读，出处不带行号。

## 5 鸿蒙声明：`dts_lookup.py`

打印匹配行前面最后一段注释、所属类型，标题行另打首段 `@since`（起始版本取它）；默认列出同名的每个重载、每处声明，末尾打总数；给 maxhits 时截断并说还剩几处。

## 6 安卓资源和依赖库：`android_res.py`

- 在平台 `data/res` 的全部 `values*` 目录和 aar 的 `res/values*` 里找定义；style 顺着显式 parent 和点号隐式父走，**每层的每个限定变体各打一行**（目录、parent、属性原值），变体换了 parent 就两条路都走；`?attr`（按主题链）、`@color` / `@dimen`（按限定目录选）、`res/color*/` 的颜色状态列表（取可用、未按下的那一项，算上 alpha）解析到字面值。
- `--api` 默认本机最新的平台，并列出其余可选；`--lib` 在 Gradle 缓存 `modules-2` 里找各版 aar，默认最旧、最新两个正式版；几组并排时，后面的组只打和第一组不同的层。查库时 `android:` 开头的父主题和资源用 `--api` 那一版平台资源解析。单次 0.5–2 秒。
- Android SDK 目录：`--sdk`，或环境变量 `ANDROID_SDK_ROOT`、`ANDROID_HOME`；都没有就报错。Gradle caches：`--gradle`，或 `GRADLE_USER_HOME` 下的 `caches`，再不行取 Gradle 自己的默认位置（用户主目录下 `.gradle/caches`）。
- **小结分四段，都要看**：① 参考配置下实际命中——★常见手机竖屏（默认 sw 360–412dp、可用高 660–915dp、xxhdpi）、手机横屏（宽、高对调）、平板（sw 600–800dp、长边 960–1280dp、竖横屏、xhdpi）三行，各写命中哪一份、值是多少；范围里命中不同的按条件分行（如「sw 360–399dp：40dp〔values-w360dp-port-v13〕；sw 400–412dp：48dp〔values-w400dp-port-v13〕」）；库模式还按 API 段、有夜间变体时按日夜分。② 各限定变体——每个带 `sw`/`w`/`h<N>dp`、`land`/`port`、密度、屏幕尺寸、长屏、圆屏、界面模式、布局方向、触屏的目录一行：条件、只满足这个条件时的取值，常见手机竖屏会命中的行首加 ★。③ 只按 API 和日夜。④ 另有以下变体，要逐个看——语言、地区、运营商、语法性别、广色域、HDR、键盘、导航键这些限定的目录，不归纳，列出目录名。
- 命中判法照安卓的资源匹配（`ResTable_config::match` 和 `isBetterThan`）：先淘汰矛盾的（密度不淘汰），再按 布局方向 > sw > w、h（配置值减目录值之和小的胜）> 屏幕尺寸 > 长屏 > 圆屏 > 横竖屏 > 界面模式 > 日夜 > 密度 > 触屏 > vNN 逐个比。范围按见到的阈值切段取样，不会漏掉范围中间的切换点。

已知限制：

- 第 ④ 段那些限定不归纳，含它们的目录一律当不命中；两份目录在已实现的限定上全打平时取带限定的那份；参考配置的宽、高是 `screenWidthDp` / `screenHeightDp` 口径，横屏的高直接取 sw、没扣系统栏；「各限定变体」那一段只满足该目录自己的限定，物理上不一定有这样的设备，实际谁胜看参考配置那一段；参考配置的默认范围是经验值，没有按机型统计核过。
- 不跟 `@style/…` 和 `textAppearance`、`actionBarTheme`、`materialThemeOverlay` 这类间接引用和主题覆盖层（停下并写明「不再解析」）；控件 style 的 `?attr` 要 `--theme` 才解析；drawable、string、array 不解析；颜色状态列表只取默认状态那一项，`lStar` 不计算。
- 查库时平台那一层只用一个 `--api` 的资源；真机低 API 用的是它自己那版框架资源。平台属性本身从哪个 API 起才有（如 `statusBarColor` 是 21）工具不判断。
- 库只找 Gradle 缓存 `modules-2/files-2.1` 下的 aar（不看 `transforms-*` 解包目录、mavenLocal、工程里的 aar）；几个 `--lib` 一起查时按「最旧配最旧、最新配最新」配对；分段从各库 minSdk 的最大值起。缓存里没有的中间版本要自己去官方仓库取（`rules.md` V6a 第 7 条）。

## 7 为什么接在 apply、lint 之后，而不是 apply 之前

想过在归并写好提案之后、apply 之前配知识，把核出来的改句直接改进提案、只 apply 一次。没这样做，原因：

1. **新经验的 ID 在 apply 时才定。** 没写 id 的按标题和证据算指纹；改句一改标题或证据，ID 就变，知识文件名对不上。
2. **提案里放不下条目。** 提案里一条经验只认固定的几个字段（id、title、topic、when、description、unless、why、how、check、evidence、requires、status），多一个键就报错；条目只能另放文件。
3. **没有正文文件可核。** 检查、渲染脚本按导出的 `.lesson.md` 定位改句，`--from-case-files links` 也要「## 来源」的链接；apply 之前只有提案。
4. **改旧经验有门槛。** 作者对改已有经验要求每处改动有依据、改动最小；知识核出的改句多出自声明和文档，放进归并提案会把两件事搅在一起。

所以知识接在 apply、lint 之后、export 之前：用一份开发版导出拿正文，配完知识；改句要进正文时另写一份提案，单独 apply、lint、export。写这份提案时注意：

- 改句要落在单个字段里：提案里 how、unless 是列表，导出时才拼成「1. …」「- …」，跨字段（比如连着小节标题、跨做法的两步）的原句搬不回提案（`rules.md` U2）。
- 内容变了的经验版本号加一；`requires` 它、又不在同一提案里的经验会被标 `needs_review`。
- lint 对本次改动的经验查「无出处的色值与尺寸/时长数值」和「待核/近似」字样；知识改句常补数值和条件，新句里带上「默认」「API N」「版本」这类字样，或在归并的说明里逐条交代。
- 配知识要几十次工具调用；这期间 store 上若有别的 apply，提案的 base_revision 会过期，照维护流程重读变化再修订。
