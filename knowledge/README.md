# 经验后面挂的「已核实的平台事实」（试验分支 `memory/shadow-v7-20261121`）

## 这个分支相对 main 改了什么

派生自 main `369bbbf3`（store `e797fb15`，active 651 条、retired 1 条）。相对 main：

1. **store**：照维护流程写提案、apply（共 7 次：建分支时一次，之后每并入一批带正文改动的知识一次，见「并入记录」），store 版本 `e797fb15` → `8d2cf9a9`（`8d2cf9a9d5254db909eebc8f922fb905910a00762d81a5ec0037fb5322cb6273`）。
   - 退役 4 条通用审查式经验（没有具体触发情景，要求把某一类东西全部核一遍或交付前做通用动作）：`lesson-6e558834938be19c04e2`、`lesson-25bc0b7518d335a947d6`、`lesson-42df1ac4d4030421da34`、`lesson-0c9e222422d81871b464`；理由写在 store 快照的 `retirement_reason` 里。
   - 235 条经验按本目录知识文件里核实过的 `changes` 改正文（各次的处数见「并入记录」；被换掉的知识文件的改句仍在正文里，不在现在的知识文件里），版本比 main 高 1–2（先后被两批知识改过正文的经验高不止 1）；`evidence`、`requires`、`topic`、`status` 原样。
   - 现在 active 647 条、retired 5 条（其中 1 条在 main 上就已退役）。
2. **memory/**：从新 store 用维护脚本重新导出（开发版，带卡片链接，`--link-cards`），通过发布脚本用的严格校验（manifest 的版本等于 store HEAD、每个文件 sha256 对得上、没有多余文件）；`MEMORY.md` 的发布版本行同步改了。和 main 比：4 个退役经验的文件没了，235 个经验文件和 59 个索引 / manifest 文件变了，其余经验文件逐字节相同。
3. **新增两个目录**：`knowledge/`（本目录）和 `shadow/`（定向核对版影子的提示词和用法）；`.gitignore` 放行这两个目录。仓库根 `README.md` 没改。

## 并入记录

建分支之后每并入一批知识文件记一行：知识文件拷进 `lessons/`；有改句的经提案 apply 进 store、从新 store 重新导出 `memory/`（严格校验）；重新渲染；一批一个提交。

| 批 | 日期 | 经验（id 前 8 位） | 条目 | 正文改动 | store | 知识的规则和复核 |
|---:|---|---|---:|---|---|---|
| 1 | 2026-11-21 | 9 条：`2fcb6612`、`4f81eeea`、`7083c6ad`、`92aee54a`、`99080bd3`、`bc5b8558`、`c8e645a5`、`cf111aad`、`eb4de4fd` | 37 | 7 处、5 条经验：`7083c6ad` 3、`92aee54a` 1、`99080bd3` 1、`bc5b8558` 1、`c8e645a5` 1 | `7312cbfe` → `09bd22c2` | 第七版规则，写完后经另一个人逐条独立复核 |
| 2 | 2026-11-21 | 24 条：`08e71bb7`、`1696967d`、`18d9c9a3`、`29744eb6`、`3f3e1ff0`、`4567f9f7`、`4a4f8d84`、`4d0f0176`、`55f44e2e`、`776ed5eb`、`8a881c2e`、`8b145360`、`8d297954`、`9147be4d`、`943544ce`、`b58df29f`、`c4af68b3`、`d80ced7b`、`d9143de0`、`dcb3c5e6`、`ea965b7b`、`f6b95d7d`、`f80ae7c3`、`f88b9c82` | 86 | 9 处、5 条经验：`18d9c9a3` 1、`4a4f8d84` 2、`943544ce` 3、`b58df29f` 1、`f88b9c82` 2 | `09bd22c2` → `1e791453` | 第七版规则，写完后经另一个人逐条独立复核 |
| 3 | 2026-11-21 | 24 条：`0a26e0cf`、`19dd006e`、`1e972af4`、`31ab9f59`、`39d1dee4`、`6d6ba721`、`6dae0bf2`、`783faf27`、`824031d5`、`8390913d`、`8953e390`、`8e0e9fe5`、`94a3f7a5`、`a58ebfe7`、`a6ed8a9c`、`ad6f23b8`、`ae093ded`、`b1916207`、`c1968bdf`、`c4a6eaaf`、`cf018b76`、`dbfae443`、`fb996956`、`feec63f6` | 72 | 21 处、12 条经验：`0a26e0cf` 2、`19dd006e` 2、`6d6ba721` 2、`824031d5` 2、`8953e390` 1、`8e0e9fe5` 1、`a58ebfe7` 3、`b1916207` 2、`c4a6eaaf` 2、`cf018b76` 1、`dbfae443` 1、`feec63f6` 2 | `1e791453` → `b5e76f80` | 第七版规则，写完后经另一个人逐条独立复核 |
| 4 | 2026-11-22 | 263 条：`009212ca`、`03786d9b`、`046c8bbb`、`08c38f95`、`08e71bb7`、`09a0bcea`、`0a26e0cf`、`0b72c197`、`0caaa4ef`、`0cbafc2a`、`0cc7ae4e`、`0ce9fe04`、`0d7d6e73`、`0deb5117`、`1150c0c7`、`1267d6ca`、`14509c64`、`148a3e67`、`14b7f409`、`1696967d`、`16c24b9a`、`1856958f`、`187c725b`、`18d9c9a3`、`18fca50f`、`19dd006e`、`1a315093`、`1c27b6c7`、`1cebb531`、`1d3ab8b9`、`1e972af4`、`1f366fe4`、`1f6e36f8`、`1fa08bf9`、`21db515a`、`22f5100f`、`237091b9`、`24625282`、`24bc4929`、`2622bc32`、`27d9e16a`、`29b42ac7`、`29f62d17`、`2a2924aa`、`2cf26148`、`2e4279c4`、`2ed8c219`、`2fcb6612`、`300200dd`、`30643cd3`、`3117bc94`、`31ab9f59`、`32af50a1`、`32c7d4b2`、`3348c580`、`338f1184`、`351ce34d`、`35a68486`、`35b9cdfd`、`35f4f9b3`、`39077e66`、`39d1dee4`、`39f137ee`、`3af52968`、`3b4a9614`、`3f3e1ff0`、`3f6b5d0b`、`4030f978`、`40fc63b1`、`420023d4`、`42364ad3`、`4283cc34`、`42cf412c`、`43a90502`、`4567f9f7`、`46a0d7f2`、`47faf26b`、`488a3bd7`、`4a4f8d84`、`4a7c04b8`、`4b5903a8`、`4bea916d`、`4c93cca5`、`4ce3a1c1`、`4d0f0176`、`4d1c980b`、`4e306a66`、`4f81eeea`、`5034b56b`、`51138567`、`52d7edb9`、`5475edc4`、`55f44e2e`、`5754b7be`、`57a52be7`、`5990184d`、`5bc9af19`、`5c101b4b`、`5c6217b0`、`5c703b4b`、`5caf7ead`、`5d6e099f`、`5e235f28`、`5f669c37`、`5f883372`、`605038b0`、`617ffbd8`、`624248be`、`65358a02`、`666a7460`、`66e08237`、`67118603`、`67ab02ab`、`68717b80`、`69229aa8`、`69e07207`、`6a3a7f46`、`6c474c15`、`6d3ac9a5`、`6d6ba721`、`6dae0bf2`、`6e74f064`、`7083c6ad`、`716d06e7`、`73a7dd4f`、`74295d12`、`74d535af`、`7508ddc5`、`776ed5eb`、`7827e070`、`783faf27`、`786a0484`、`7b19b801`、`7caea06a`、`7ed00c55`、`7f5eba1b`、`80e1d2c0`、`824031d5`、`836a5414`、`8390913d`、`8534b92d`、`871d3751`、`8953e390`、`8a752faf`、`8a7d2595`、`8a881c2e`、`8b145360`、`8b7c4ece`、`8bc258c2`、`8d297954`、`8e0e9fe5`、`9147be4d`、`92aee54a`、`931ef95a`、`94a3f7a5`、`953309e0`、`95aa64d6`、`96c89001`、`96eea0fe`、`9769c8f7`、`97bf3cf5`、`9886f489`、`99080bd3`、`99a8d470`、`9d42548e`、`9de33221`、`9f2d3b8b`、`a078efd3`、`a3ac761b`、`a45be200`、`a4e6bcfb`、`a4ee90ea`、`a5aeed3d`、`a6121cc7`、`a6ed8a9c`、`a6f300f9`、`a7f81d00`、`aae5f345`、`ac7a2e17`、`ad6f23b8`、`adad817f`、`ae78da6f`、`afae8d13`、`b0405a29`、`b366cf7a`、`b3bb0bc3`、`b3f534eb`、`b58df29f`、`b58f26f0`、`b661a3a6`、`b714378f`、`b73a1ac8`、`b742fb72`、`b92a8a56`、`ba0cb144`、`bc5b8558`、`bc79621b`、`bdb97da6`、`c066489f`、`c1968bdf`、`c3a3797d`、`c46f182c`、`c4a6eaaf`、`c4af68b3`、`c55c5644`、`c61ac79c`、`c73deaf6`、`c7ee1769`、`c883a0ff`、`c8e645a5`、`caa043fb`、`ccccf83d`、`cde4120a`、`cf018b76`、`cf670f80`、`d0736ecd`、`d0aad947`、`d442eb6e`、`d53223f4`、`d715fa78`、`d77baa74`、`d7c148c4`、`d838f923`、`d9143de0`、`dbfae443`、`dc3f2589`、`df1f6917`、`dfcdbb19`、`e01c6f82`、`e17b45a2`、`e6b1f909`、`e9890889`、`e9f03fcc`、`ea965b7b`、`ea9a6cfe`、`eb4de4fd`、`ecbaa172`、`ed555632`、`edae4e27`、`ef93bb20`、`efb94f2d`、`efff9374`、`f0a40d99`、`f1069f51`、`f122d4c4`、`f1963297`、`f1a98587`、`f395cbdf`、`f3e614f2`、`f64afc22`、`f6b95d7d`、`f80ae7c3`、`f86b02e9`、`f876887b`、`f9f923ac`、`faec7be0`、`fb996956`、`fd3add71`、`fe10bd24`、`feec63f6`、`fef54f39`、`ff19b091`、`ff5e8fbf`（其中覆盖已有的 57 个） | 1108 | 210 处、176 条经验：`03786d9b` 1、`08c38f95` 1、`0b72c197` 1、`0caaa4ef` 1、`0cc7ae4e` 3、`0ce9fe04` 1、`0d7d6e73` 1、`0deb5117` 1、`1150c0c7` 2、`1267d6ca` 1、`14509c64` 2、`148a3e67` 1、`14b7f409` 1、`1696967d` 1、`16c24b9a` 1、`1856958f` 2、`187c725b` 2、`18fca50f` 1、`19dd006e` 1、`1c27b6c7` 1、`1cebb531` 1、`1e972af4` 1、`1f366fe4` 1、`1f6e36f8` 1、`21db515a` 1、`22f5100f` 1、`237091b9` 1、`24625282` 1、`24bc4929` 1、`2622bc32` 1、`29b42ac7` 1、`2a2924aa` 1、`2cf26148` 1、`2ed8c219` 1、`2fcb6612` 2、`300200dd` 1、`30643cd3` 1、`31ab9f59` 1、`32c7d4b2` 1、`3348c580` 1、`338f1184` 1、`39077e66` 2、`39d1dee4` 1、`3b4a9614` 1、`3f3e1ff0` 1、`3f6b5d0b` 2、`4030f978` 1、`40fc63b1` 1、`42364ad3` 2、`4283cc34` 1、`42cf412c` 2、`43a90502` 1、`4567f9f7` 1、`488a3bd7` 1、`4a4f8d84` 1、`4a7c04b8` 1、`4b5903a8` 1、`4bea916d` 1、`4ce3a1c1` 1、`4d0f0176` 1、`4e306a66` 1、`5034b56b` 1、`51138567` 1、`52d7edb9` 1、`5475edc4` 1、`55f44e2e` 1、`57a52be7` 1、`5990184d` 1、`5bc9af19` 1、`5c101b4b` 1、`5c6217b0` 1、`5c703b4b` 1、`5caf7ead` 1、`5d6e099f` 2、`5f669c37` 1、`605038b0` 1、`617ffbd8` 2、`624248be` 1、`65358a02` 1、`666a7460` 2、`66e08237` 1、`67118603` 1、`69229aa8` 1、`69e07207` 1、`6c474c15` 1、`6d3ac9a5` 1、`6d6ba721` 2、`6e74f064` 1、`7083c6ad` 1、`716d06e7` 2、`74295d12` 1、`74d535af` 1、`7508ddc5` 1、`776ed5eb` 1、`7827e070` 1、`783faf27` 1、`7b19b801` 1、`80e1d2c0` 1、`824031d5` 2、`836a5414` 2、`8534b92d` 1、`871d3751` 1、`8a752faf` 1、`8a7d2595` 1、`8a881c2e` 3、`8bc258c2` 1、`8d297954` 2、`8e0e9fe5` 2、`9147be4d` 1、`92aee54a` 1、`94a3f7a5` 1、`953309e0` 1、`9769c8f7` 1、`97bf3cf5` 1、`9886f489` 1、`99a8d470` 1、`9d42548e` 1、`a078efd3` 3、`a45be200` 1、`a4e6bcfb` 2、`a4ee90ea` 1、`a5aeed3d` 2、`a6121cc7` 3、`a6ed8a9c` 1、`a6f300f9` 1、`aae5f345` 1、`adad817f` 2、`afae8d13` 1、`b0405a29` 2、`b3bb0bc3` 2、`b58f26f0` 1、`b714378f` 1、`b742fb72` 1、`ba0cb144` 1、`bc5b8558` 1、`bc79621b` 1、`c1968bdf` 1、`c3a3797d` 1、`c46f182c` 1、`c4a6eaaf` 1、`c4af68b3` 1、`c61ac79c` 1、`c7ee1769` 2、`c883a0ff` 1、`caa043fb` 1、`ccccf83d` 1、`cf018b76` 1、`d0736ecd` 1、`d0aad947` 1、`d442eb6e` 1、`d53223f4` 1、`d715fa78` 1、`d838f923` 1、`dbfae443` 1、`dc3f2589` 1、`df1f6917` 1、`e01c6f82` 1、`e9f03fcc` 1、`ea965b7b` 1、`ea9a6cfe` 2、`eb4de4fd` 1、`edae4e27` 1、`efb94f2d` 1、`f1069f51` 2、`f122d4c4` 1、`f1a98587` 1、`f3e614f2` 1、`f64afc22` 1、`f6b95d7d` 1、`f86b02e9` 1、`faec7be0` 1、`fb996956` 1、`fd3add71` 1、`fe10bd24` 1、`feec63f6` 1、`ff19b091` 1 | `b5e76f80` → `fc763e4c` | 照第三版的写法写（每条经验最多 24 条、只留编译查不出来的那类）；另核过适用情境和例外与边界，有依据的补进正文 |
| 5 | 2026-11-22 | 28 条：`033b8254`、`0457a04c`、`22432022`、`29744eb6`、`2e636699`、`368c4592`、`396d5447`、`51651155`、`5a82d62f`、`5d1c2c78`、`652974ce`、`75f4743d`、`771d1ba1`、`8335bc40`、`943544ce`、`9c4de55a`、`9fa98065`、`a23ad0b5`、`a58ebfe7`、`ad1db0aa`、`ae093ded`、`b1916207`、`cf111aad`、`d80ced7b`、`dcb3c5e6`、`e3077bf6`、`edc9465d`、`fde79829`（其中覆盖已有的 21 个） | 355 | 72 处、28 条经验：`033b8254` 5、`0457a04c` 3、`22432022` 2、`29744eb6` 3、`2e636699` 1、`368c4592` 4、`396d5447` 4、`51651155` 1、`5a82d62f` 5、`5d1c2c78` 2、`652974ce` 3、`75f4743d` 5、`771d1ba1` 4、`8335bc40` 3、`943544ce` 2、`9c4de55a` 3、`9fa98065` 1、`a23ad0b5` 2、`a58ebfe7` 2、`ad1db0aa` 3、`ae093ded` 2、`b1916207` 3、`cf111aad` 2、`d80ced7b` 1、`dcb3c5e6` 1、`e3077bf6` 1、`edc9465d` 2、`fde79829` 2 | `fc763e4c` → `6fe45861` | 照第三版的写法写（每条经验最多 24 条、只留编译查不出来的那类）；另核过适用情境和例外与边界，有依据的补进正文 |
| 6 | 2026-11-22 | 23 条：`08b9064f`、`0e1c8468`、`0ef2cd00`、`11e9d15d`、`1a66114f`、`447ba581`、`47785524`、`4da9eabc`、`4e9507a2`、`51bf52bc`、`68023ac5`、`73894333`、`7708f650`、`803ba029`、`80dd4e62`、`843a70af`、`94715d0d`、`a2f6a4ae`、`a8452bfe`、`b1991f63`、`bdc493f5`、`c3bd9c8b`、`cce58a15`（其中覆盖已有的 23 个） | 271 | 25 处、20 条经验：`08b9064f` 3、`0e1c8468` 1、`0ef2cd00` 1、`11e9d15d` 1、`1a66114f` 1、`447ba581` 1、`47785524` 1、`4da9eabc` 2、`4e9507a2` 1、`73894333` 1、`7708f650` 1、`803ba029` 1、`80dd4e62` 2、`843a70af` 1、`94715d0d` 1、`a2f6a4ae` 1、`a8452bfe` 1、`b1991f63` 2、`bdc493f5` 1、`cce58a15` 1 | `6fe45861` → `8d2cf9a9` | 照第三版的写法写（每条经验最多 24 条、只留编译查不出来的那类）；另核过适用情境和例外与边界，有依据的补进正文 |

## 是什么

每条经验后面挂几条已经核实过的平台事实：默认值、单位、取值范围、调用时序、实际行为、两个平台的差异、安卓框架和依赖库的默认外观和行为。交给模型时接在经验正文后面（写法见下面「怎么渲染」），模型照着经验去写或去核代码时直接用，不再自己查。事实和具体应用无关；其中的默认值只在应用自己没有另设时成立。

知识文件里的 `changes` 是对经验正文某句的改动（核到的事实和正文对不上、或缺条件时）；本分支已经把它们经提案发布进 store 和 `memory/`，交出去的正文只有一个说法。

## 目录

| 路径 | 内容 |
|---|---|
| `lessons/lesson-<id>.json` | 每条经验的知识源文件（格式见下） |
| `rendered/<主题>/lesson-<id>.md` | 渲染好的样子（交给模型的那一段），给人看；由 `render.py` 生成 |
| `render.py` | 把 `memory/` 里的正文和知识文件渲染成交给模型的那一段 |
| `check.py` | 检查知识文件（字段、条数、本机路径、应用名、改句是否已在正文里） |
| `RULES.md` | 新写的知识照哪份规则（指到 `skill/`） |
| `RULES-v7.md` | 第七版规则的原文（留档，读和维护按它写的旧文件时用） |
| `skill/` | 配知识的 skill：流程、规则、工具脚本、任务书（见下一节） |

## 怎么写新的知识

照 `skill/` 做。`skill/SKILL.md` 是流程，有两个入口：① 新卡归并出新经验或改了旧经验之后，接在归并的 apply、lint 之后、export 之前，给这些经验配知识；② 给库里现有的经验按使用频次分批补知识。两个入口共用同一套步骤：同步 OpenHarmony 文档 master → 读正文 → 收候选 → 逐条核实并补查 → 统一写法 → 清理 → 检查 → 渲染 → 安卓平台和依赖库两类条目加全部正文改句交给另一个人专门复核 → 每批抽查。

- `skill/references/`：规则（`rules.md`）、去哪查和出处版本（`sources.md`）、文件格式（`knowledge-format.md`）、例子（`examples.md`）、工具用法和已知限制（`tools.md`）。
- `skill/scripts/`：写的人用的脚本（同步文档、收候选、查文档整节、查安卓资源和依赖库、查鸿蒙声明、换文档链接、检查、渲染）。其中 `check.py` 带核对本机出处的选项；本目录的 `check.py`、`render.py` 是仓库一侧的检查和渲染，不核本机出处。两个 `render.py` 对新格式文件的输出逐字节相同。
- `skill/briefs/`：任务书模板——写新卡归并后的经验（`write-new-cards.md`）、给现有经验补知识（`write-backfill.md`）、专门复核（`review.md`）、每批抽查（`audit.md`）。

照 skill 写出的是下面「格式」里的新格式文件，放进 `lessons/`。

## 格式

现在有两种格式：旧格式（下面前两种，第三版和第七版规则的文件，`sdk` 只记 `harmony`、`android`）和 2026-11-21 起的新格式（第三种）。已经换成新格式的经验 314 条（active 314 条）：`009212ca`、`033b8254`、`03786d9b`、`0457a04c`、`046c8bbb`、`08b9064f`、`08c38f95`、`08e71bb7`、`09a0bcea`、`0a26e0cf`、`0b72c197`、`0caaa4ef`、`0cbafc2a`、`0cc7ae4e`、`0ce9fe04`、`0d7d6e73`、`0deb5117`、`0e1c8468`、`0ef2cd00`、`1150c0c7`、`11e9d15d`、`1267d6ca`、`14509c64`、`148a3e67`、`14b7f409`、`1696967d`、`16c24b9a`、`1856958f`、`187c725b`、`18d9c9a3`、`18fca50f`、`19dd006e`、`1a315093`、`1a66114f`、`1c27b6c7`、`1cebb531`、`1d3ab8b9`、`1e972af4`、`1f366fe4`、`1f6e36f8`、`1fa08bf9`、`21db515a`、`22432022`、`22f5100f`、`237091b9`、`24625282`、`24bc4929`、`2622bc32`、`27d9e16a`、`29744eb6`、`29b42ac7`、`29f62d17`、`2a2924aa`、`2cf26148`、`2e4279c4`、`2e636699`、`2ed8c219`、`2fcb6612`、`300200dd`、`30643cd3`、`3117bc94`、`31ab9f59`、`32af50a1`、`32c7d4b2`、`3348c580`、`338f1184`、`351ce34d`、`35a68486`、`35b9cdfd`、`35f4f9b3`、`368c4592`、`39077e66`、`396d5447`、`39d1dee4`、`39f137ee`、`3af52968`、`3b4a9614`、`3f3e1ff0`、`3f6b5d0b`、`4030f978`、`40fc63b1`、`420023d4`、`42364ad3`、`4283cc34`、`42cf412c`、`43a90502`、`447ba581`、`4567f9f7`、`46a0d7f2`、`47785524`、`47faf26b`、`488a3bd7`、`4a4f8d84`、`4a7c04b8`、`4b5903a8`、`4bea916d`、`4c93cca5`、`4ce3a1c1`、`4d0f0176`、`4d1c980b`、`4da9eabc`、`4e306a66`、`4e9507a2`、`4f81eeea`、`5034b56b`、`51138567`、`51651155`、`51bf52bc`、`52d7edb9`、`5475edc4`、`55f44e2e`、`5754b7be`、`57a52be7`、`5990184d`、`5a82d62f`、`5bc9af19`、`5c101b4b`、`5c6217b0`、`5c703b4b`、`5caf7ead`、`5d1c2c78`、`5d6e099f`、`5e235f28`、`5f669c37`、`5f883372`、`605038b0`、`617ffbd8`、`624248be`、`652974ce`、`65358a02`、`666a7460`、`66e08237`、`67118603`、`67ab02ab`、`68023ac5`、`68717b80`、`69229aa8`、`69e07207`、`6a3a7f46`、`6c474c15`、`6d3ac9a5`、`6d6ba721`、`6dae0bf2`、`6e74f064`、`7083c6ad`、`716d06e7`、`73894333`、`73a7dd4f`、`74295d12`、`74d535af`、`7508ddc5`、`75f4743d`、`7708f650`、`771d1ba1`、`776ed5eb`、`7827e070`、`783faf27`、`786a0484`、`7b19b801`、`7caea06a`、`7ed00c55`、`7f5eba1b`、`803ba029`、`80dd4e62`、`80e1d2c0`、`824031d5`、`8335bc40`、`836a5414`、`8390913d`、`843a70af`、`8534b92d`、`871d3751`、`8953e390`、`8a752faf`、`8a7d2595`、`8a881c2e`、`8b145360`、`8b7c4ece`、`8bc258c2`、`8d297954`、`8e0e9fe5`、`9147be4d`、`92aee54a`、`931ef95a`、`943544ce`、`94715d0d`、`94a3f7a5`、`953309e0`、`95aa64d6`、`96c89001`、`96eea0fe`、`9769c8f7`、`97bf3cf5`、`9886f489`、`99080bd3`、`99a8d470`、`9c4de55a`、`9d42548e`、`9de33221`、`9f2d3b8b`、`9fa98065`、`a078efd3`、`a23ad0b5`、`a2f6a4ae`、`a3ac761b`、`a45be200`、`a4e6bcfb`、`a4ee90ea`、`a58ebfe7`、`a5aeed3d`、`a6121cc7`、`a6ed8a9c`、`a6f300f9`、`a7f81d00`、`a8452bfe`、`aae5f345`、`ac7a2e17`、`ad1db0aa`、`ad6f23b8`、`adad817f`、`ae093ded`、`ae78da6f`、`afae8d13`、`b0405a29`、`b1916207`、`b1991f63`、`b366cf7a`、`b3bb0bc3`、`b3f534eb`、`b58df29f`、`b58f26f0`、`b661a3a6`、`b714378f`、`b73a1ac8`、`b742fb72`、`b92a8a56`、`ba0cb144`、`bc5b8558`、`bc79621b`、`bdb97da6`、`bdc493f5`、`c066489f`、`c1968bdf`、`c3a3797d`、`c3bd9c8b`、`c46f182c`、`c4a6eaaf`、`c4af68b3`、`c55c5644`、`c61ac79c`、`c73deaf6`、`c7ee1769`、`c883a0ff`、`c8e645a5`、`caa043fb`、`ccccf83d`、`cce58a15`、`cde4120a`、`cf018b76`、`cf111aad`、`cf670f80`、`d0736ecd`、`d0aad947`、`d442eb6e`、`d53223f4`、`d715fa78`、`d77baa74`、`d7c148c4`、`d80ced7b`、`d838f923`、`d9143de0`、`dbfae443`、`dc3f2589`、`dcb3c5e6`、`df1f6917`、`dfcdbb19`、`e01c6f82`、`e17b45a2`、`e3077bf6`、`e6b1f909`、`e9890889`、`e9f03fcc`、`ea965b7b`、`ea9a6cfe`、`eb4de4fd`、`ecbaa172`、`ed555632`、`edae4e27`、`edc9465d`、`ef93bb20`、`efb94f2d`、`efff9374`、`f0a40d99`、`f1069f51`、`f122d4c4`、`f1963297`、`f1a98587`、`f395cbdf`、`f3e614f2`、`f64afc22`、`f6b95d7d`、`f80ae7c3`、`f86b02e9`、`f876887b`、`f9f923ac`、`faec7be0`、`fb996956`、`fd3add71`、`fde79829`、`fe10bd24`、`feec63f6`、`fef54f39`、`ff19b091`、`ff5e8fbf`；其余 5 个知识文件还是旧格式。

共同：`sdk` 是核实时用的版本（`harmony`、`android` 两个键；新格式另有三个键）；`changes` 每项有 `where`（正文哪一部分）、`before`（原句）、`after`（新句）、`basis`（依据）、`type`（改动类别）；`entries` 是平台事实；`device_todo` 是要上机才能定的事项，只留给维护的人；`dropped_notes` 是配的人删掉的条数。交给模型的只有正文（已含改句）和条目的 `step`、`fact`、`scope`；`source`、`code`、`origin`、`basis`、`device_todo` 不交。

- **第三版规则的格式（4 个文件）**：顶层 `id`、`sdk`、`changes`、`entries`、`device_todo`、`dropped_notes`（个别有 `note`）。条目栏 `step`、`fact`、`source`、`kind`（鸿蒙接口 / 安卓平台 / 依赖库 / 卡里验证）、`origin`，个别带 `code`；**没有 `scope`**，条数比第七版多（共 35 条，一条经验最多 19 条）。
- **第七版规则的格式（1 个文件）**：顶层 `lesson`、`sdk`、`changes`、`entries`、`device_todo`、`dropped_notes`、`note`。条目栏 `step`、`fact`、`scope`（成立范围：对什么成立、什么条件下成立、最常见的不成立情形）、`source`、`kind`（鸿蒙接口 / 安卓平台 / 依赖库）、`origin`，可选 `code`；每条经验最多 6 条（共 5 条）。规则见 `RULES.md`。
- **新格式（2026-11-21 起，314 个文件）**：和第三版同一种结构（顶层 `id`、`sdk`、`changes`、`entries`、`device_todo`、`dropped_notes`，没有条目时有 `note`），`sdk` 另记 `verified_on`（核实日期）、`docs_commit`、`docs_date`（核实时用的 OpenHarmony 文档 master 的提交和日期）。条目栏 `step`、`fact`、`source`、`kind`（鸿蒙接口 / 安卓平台 / 依赖库 / 卡里验证）、`origin`；没有 `scope`，条数不设上限（共 1734 条，一条经验最多 24 条）。渲染时段头在鸿蒙 SDK 版本后面多写文档 master 的日期和提交，条目不带成立范围。

## 覆盖

319 个知识文件。其中 4 个对应本分支退役的经验（文件原样留着，不渲染，它们的 8 处改句没有套）；其余 **315 / 647 条 active 经验**有知识文件（第三版 0 条、第七版 1 条、新格式 314 条），其中 288 条有条目（`08e71bb7`、`1fa08bf9`、`22f5100f`、`31ab9f59`、`35b9cdfd`、`35f4f9b3`、`447ba581`、`5c703b4b`、`5f883372`、`6a3a7f46`、`6d3ac9a5`、`6e74f064`、`8390913d`、`8a7d2595`、`9147be4d`、`931ef95a`、`95aa64d6`、`99a8d470`、`aae5f345`、`ae78da6f`、`b92a8a56`、`c1968bdf`、`d9143de0`、`dbfae443`、`dfcdbb19`、`ed555632`、`f395cbdf` 是流程类经验，没有可挂的条目）。其余 active 经验还没有知识。

| id | 主题 | 规则 | 条目（带成立范围） | 改句（已进正文） | 标题 |
|---|---|---|---:|---:|---|
| `lesson-2fcb6612ee4106b34e17` | app/base-page | 新格式 | 7（0） | 2（是） | Android 业务基类的横切行为逐方法映射到组合式 BasePag… |
| `lesson-7ed00c55221c0f935d95` | app/bluetooth | 新格式 | 4（0） | 0 | 封装 startBLEScan 等声明为 void 的同步系统接口时… |
| `lesson-51651155ed8226212e55` | app/entry | 新格式 | 9（0） | 1（是） | 源 Activity 的 SEND 分享接收入口（standard … |
| `lesson-67118603fcc769a5edc9` | app/entry | 新格式 | 5（0） | 1（是） | ohos.ability.shortcuts 挂在承载快捷方式的 U… |
| `lesson-8a881c2e07f80f83447c` | app/entry | 新格式 | 5（0） | 3（是） | 源端靠依赖注入或全局静态工具就绪的基础设施改成需显式 init 的封… |
| `lesson-94715d0df4c03a8fb5a5` | app/entry | 新格式 | 14（0） | 1（是） | 源 Activity 未声明 configChanges 时，旋转（… |
| `lesson-a23ad0b53c75e49ca117` | app/entry | 新格式 | 10（0） | 2（是） | intent-filter 逐条映射为 module.json5 s… |
| `lesson-b0405a29415547485ecb` | app/entry | 新格式 | 12（0） | 2（是） | 源端返回栈靠框架在进程回收后重建（rememberNavContro… |
| `lesson-c46f182cf1d01a97e05f` | app/entry | 新格式 | 4（0） | 1（是） | 只经桌面快捷方式或通知点击进入的页面：module.json5 快捷… |
| `lesson-d77baa7494930d485425` | app/entry | 新格式 | 13（0） | 0 | 深链 intent-filter 迁移时声明 module.json… |
| `lesson-dcb3c5e66dec2d126234` | app/entry | 新格式 | 7（0） | 1（是） | 源端在入口 onCreate 首帧前按偏好设主题时，目标在 Entr… |
| `lesson-ea965b7baf2488be23cd` | app/entry | 新格式 | 7（0） | 1（是） | 裁定“大字体”是否迁移时看源端是否有随系统字号缩放的文本，而不是有无… |
| `lesson-03786d9b08a145f0cc6e` | app/identity | 新格式 | 1（0） | 1（是） | productFlavors 工程按选定 flavor 一次解析身份… |
| `lesson-55f44e2efdc1a49ac387` | app/identity | 新格式 | 7（0） | 1（是） | 落地应用显示名时同时改 AppScope 的 app_name 与入… |
| `lesson-a6ed8a9c6017ddb73beb` | app/identity | 新格式 | 2（0） | 1（是） | 源端 BuildConfig.VERSION_NAME/VERSIO… |
| `lesson-c4af68b3ee1456525e8e` | app/identity | 新格式 | 8（0） | 1（是） | 启动窗按源端实际启动画面映射：未自定义 SplashScreen 时… |
| `lesson-fb996956b33a1ba65861` | app/identity | 新格式 | 6（0） | 1（是） | 沿用脚手架 bundleName/vendor 前核对所引部署期决策… |
| `lesson-feec63f65102f5396e51` | app/identity | 新格式 | 6（0） | 1（是） | 应用级图标只认 app.json5 里写的引用，AppScope 同… |
| `lesson-11e9d15d947b30d2ce7e` | app/logging | 新格式 | 4（0） | 1（是） | 新增错误日志沿用工程的 hilog 约定，不写 console.* |
| `lesson-0ce9fe04eb82e77d219f` | app/media | 新格式 | 9（0） | 1（是） | 保存媒体到相册或文件：缺写入权限时用 showAssetsCreat… |
| `lesson-ad1db0aa0434c2e766fd` | app/media | 新格式 | 11（0） | 3（是） | 从图库选图用系统 PhotoViewPicker 并复制进应用目录：… |
| `lesson-3af52968ce5762501cd3` | app/modules | 新格式 | 2（0） | 0 | BuildConfig.DEBUG 映射为 hvigor 生成的 B… |
| `lesson-b58f26f0fdb7fb00db9e` | app/modules | 新格式 | 1（0） | 1（是） | 页面与组件共用的非 UI 函数放进普通模块：不从路由页面模块具名导出… |
| `lesson-a4ee90eabe3eef99ddbe` | app/nfc | 新格式 | 5（0） | 1（是） | Android Activity 级 NFC 前台派发迁到 Harm… |
| `lesson-16c24b9a44153d703f04` | app/platform | 新格式 | 4（0） | 1（是） | Android 前台服务改用扩展能力承载时，先在项目 SDK 确认基… |
| `lesson-30643cd3f209b896ffd1` | app/platform | 新格式 | 7（0） | 1（是） | 后台 Worker 计时与带动作的进度通知迁到 HarmonyOS … |
| `lesson-35a684862ee500f08912` | app/platform | 新格式 | 4（0） | 0 | 用应用内计时加长时任务替代后台 Worker 时，恢复入口共用逐步扣… |
| `lesson-4b5903a870344121e97e` | app/platform | 新格式 | 6（0） | 1（是） | 源端拉起系统能力前的可用性预检、权限申请与无接收方回退逐段落成目标显… |
| `lesson-4bea916d1ff67e51d455` | app/platform | 新格式 | 2（0） | 1（是） | 打开系统设置的显式 Want 包名随设备与系统版本变化：写前在目标设… |
| `lesson-5990184d75275f4df4ff` | app/platform | 新格式 | 9（0） | 1（是） | AlarmManager 到点通知改用代理提醒时，按 reminde… |
| `lesson-652974ce64a9243faebc` | app/platform | 新格式 | 17（0） | 3（是） | 写目标权限清单时按每个已映射系统 API 在 SDK d.ts 中的… |
| `lesson-716d06e75b7c2102c36c` | app/platform | 新格式 | 4（0） | 2（是） | 源端通知迁到 NotificationRequest：按钮与每次构建… |
| `lesson-9769c8f754044944d3ad` | app/platform | 新格式 | 2（0） | 1（是） | 源端 Material You 动态取色迁到 HarmonyOS：用… |
| `lesson-a45be20055d942e12052` | app/platform | 新格式 | 3（0） | 1（是） | 源端 Activity 画中画映射到 @ohos.PiPWindow… |
| `lesson-e9890889e591196c3d0d` | app/platform | 新格式 | 2（0） | 0 | Android 依赖厂商 SDK（地图、登录、支付、账号等）时，先查… |
| `lesson-e9f03fcc7f1e781c4b24` | app/platform | 新格式 | 3（0） | 1（是） | 开关控制的常驻通知由应用级服务订阅与发布，不绑在页面 ViewMod… |
| `lesson-ea9a6cfecca9e091c7ea` | app/platform | 新格式 | 5（0） | 2（是） | 源端 Activity 对自身 getWindow() 加的标志（F… |
| `lesson-efb94f2d70d4df1c65d7` | app/platform | 新格式 | 7（0） | 1（是） | 决策已批准等价实现的平台能力要真实现，只在运行期按实际结果降级；判定… |
| `lesson-1267d6cabb117824c67a` | app/playback | 新格式 | 11（0） | 1（是） | AVPlayer 播放应用包内 rawfile 资源时用 getRa… |
| `lesson-1a3150939a5e45c02b0e` | app/playback | 新格式 | 3（0） | 0 | 源端同一 release() 用在不同作用域时，目标封装拆成两个方法… |
| `lesson-511385674c16eb68c88c` | app/playback | 新格式 | 2（0） | 1（是） | 异步 AVPlayer 装载使用代数令牌与实例归属，停止服务时显式复… |
| `lesson-5475edc47af05c1c6a5b` | app/playback | 新格式 | 5（0） | 1（是） | MediaPlayer 短提示音迁 AVPlayer 时保留源端隐式… |
| `lesson-d0736ecd82af68edb87a` | app/playback | 新格式 | 5（0） | 1（是） | AVPlayer 错误只经一条通道上报，Promise 调用接 ca… |
| `lesson-4e306a66aba5f1d76fdf` | app/resources | 新格式 | 5（0） | 1（是） | VectorDrawable 转 SVG 时 viewBox 取 v… |
| `lesson-66e082374dc8992f48ae` | app/resources | 新格式 | 1（0） | 1（是） | 转换快捷方式等图标资源时同时落实画布尺寸与图形显示区；测量墨迹范围后… |
| `lesson-74d535afb21b2270119e` | app/resources | 新格式 | 2（0） | 1（是） | Compose Material 图标（Icons.Rounded、… |
| `lesson-783faf2767a952034514` | app/resources | 新格式 | 3（0） | 1（是） | 8 位颜色保持 #AARRGGBB 字节序，转换后与源逐项往返核对 |
| `lesson-94a3f7a5ec5ad8f8a3e8` | app/resources | 新格式 | 3（0） | 1（是） | values 批量转 element JSON 按目标格式出口：颜色… |
| `lesson-d838f9236f7452b82738` | app/resources | 新格式 | 4（0） | 1（是） | adaptive-icon 转 layered-image 时前景与… |
| `lesson-f88b9c824280ce239dea` | app/resources | 第七版 | 5（5） | 2（是） | strings.xml 转 string.json 按 aapt2 … |
| `lesson-f9f923ac13560dc4a114` | app/resources | 新格式 | 3（0） | 0 | 语言限定目录只放源端 values-<locale> 实际有的资源类… |
| `lesson-24bc4929b771a9a33ef4` | app/settings | 新格式 | 3（0） | 1（是） | 源端 SharedPreferences.Editor 累积 put… |
| `lesson-4283cc343b875489b851` | app/settings | 新格式 | 3（0） | 1（是） | 设置页由 addPreferencesFromResource/Pr… |
| `lesson-4d0f0176b3d09c33f1eb` | app/settings | 新格式 | 9（0） | 1（是） | 迁移设置开关、设置保存与持久化的界面状态时为每项落实运行期消费方：只… |
| `lesson-9fa98065e5de983b7c01` | app/settings | 新格式 | 6（0） | 1（是） | SharedPreferences 迁移保留同步时序：onCreat… |
| `lesson-95aa64d6b0a5c041d326` | app/startup | 新格式 | 0（0） | 0 | 源端首启无已选项、需先选择才进主界面时，目标定义“无已选项”状态：不… |
| `lesson-99a8d47085e4b1ae44de` | app/startup | 新格式 | 0（0） | 1（是） | 延后无对等 API 的采集通道时，单独移植源端与采集无关的超时兜底，… |
| `lesson-338f11844f0010e46bc3` | arkts/async | 新格式 | 4（0） | 1（是） | 同步读取改成异步 initialize 后，失败分支要复位状态并让页… |
| `lesson-47faf26b44bb4075b0d2` | arkts/async | 新格式 | 4（0） | 0 | 源 API 用返回值表示“被拒”、用异常表示故障，而目标 SDK 两… |
| `lesson-5c703b4b1128e37dbef5` | arkts/async | 新格式 | 0（0） | 1（是） | 需授权、需初始化或依赖定位坐标的仓库方法，前置条件缺失时按源端分支处… |
| `lesson-843a70afd7e08bfed97c` | arkts/async | 新格式 | 7（0） | 1（是） | 异步初始化里，用户可编辑的输入状态在第一个 await 之前写入初值… |
| `lesson-b19162077a2ab886d809` | arkts/async | 新格式 | 7（0） | 3（是） | Kit API 的 catch 值按 BusinessError 取… |
| `lesson-b1991f633e5307abdc4d` | arkts/async | 新格式 | 7（0） | 2（是） | 源端阻塞到完成才返回的 void 方法（排空队列、关闭设备、停录）改… |
| `lesson-ba0cb144aa48f9584060` | arkts/async | 新格式 | 2（0） | 1（是） | 源端连续的同步平台调用（先取消再振动、先停止再启动）映射到返回 Pr… |
| `lesson-8b145360b447a10d52ef` | arkts/decorators | 新格式 | 1（0） | 0 | V2 组件成员装饰器裸写（@Local/@Param/@Once/@… |
| `lesson-c1968bdf112ed3e6b259` | arkts/decorators | 新格式 | 0（0） | 1（是） | 自定义组件的成员不与组件通用属性方法同名（position、widt… |
| `lesson-0deb51172ebdd2e056a9` | arkts/numeric | 新格式 | 4（0） | 1（是） | Kotlin/Java Float 的运算与比较迁到 ArkTS 时… |
| `lesson-52d7edb9042110e30eb4` | arkts/numeric | 新格式 | 1（0） | 1（是） | 迁移比值与进度计算时保留源端的零分母分支与范围钳制：ArkTS nu… |
| `lesson-5f669c379cfcdb14ad10` | arkts/numeric | 新格式 | 3（0） | 1（是） | Java long 常量进入 SQL 或字符串时检查 JS 安全整数… |
| `lesson-0cbafc2ad4096001d0e8` | arkts/stdlib | 新格式 | 16（0） | 0 | Java/ICU 正则、String/List 方法与 Androi… |
| `lesson-237091b9b04bc4cd340b` | arkts/stdlib | 新格式 | 15（0） | 1（是） | Java 文本读行、split/trim、BOM、String.fo… |
| `lesson-ae093dedda604fddf17e` | arkts/stdlib | 新格式 | 8（0） | 2（是） | DecimalFormat、BigDecimal 舍入与 Float… |
| `lesson-ecbaa1723e2beb9b1aec` | arkts/stdlib | 新格式 | 3（0） | 0 | 手写 getString/String.format 的位置参数插入… |
| `lesson-1696967d1320c7735732` | arkts/strict-mode | 新格式 | 1（0） | 1（是） | ArkTS 里给对象字面量写显式 class/interface 类… |
| `lesson-6e74f064efe2649fc295` | arkts/strict-mode | 新格式 | 0（0） | 1（是） | SDK 把观察者或回调类型声明为 class 时不写 impleme… |
| `lesson-931ef95a3d0cf202fe5b` | arkts/strict-mode | 新格式 | 0（0） | 0 | 只含方法签名的自定义接口用 implements 它的具名类实现：不… |
| `lesson-dbfae443e671c568e14e` | arkts/strict-mode | 新格式 | 0（0） | 1（是） | catch 中继续抛出时先把异常收窄为 Error，不直接 thro… |
| `lesson-f80ae7c3747420ef16f7` | arkts/strict-mode | 新格式 | 2（0） | 0 | 静态字段初始化器或模块级常量里把类当值使用时，该类要声明在使用者之前… |
| `lesson-08e71bb72d05b1d79d28` | arkts/ui-syntax | 新格式 | 0（0） | 0 | build() 与 @Builder 里每个组件、条件与循环渲染各占… |
| `lesson-18d9c9a34c1952f43f53` | arkts/ui-syntax | 新格式 | 3（0） | 0 | justifyContent/alignItems 只属于 Colu… |
| `lesson-39d1dee415d4a252fc5c` | arkts/ui-syntax | 新格式 | 2（0） | 1（是） | stateStyles 各状态只写 @Styles 方法引用、全局 … |
| `lesson-3f6b5d0b0ea6806a1b0c` | data/files | 新格式 | 5（0） | 2（是） | fileIo.mkdirSync 对已存在目录会抛 13900015… |
| `lesson-4c93cca5dde48080b008` | data/files | 新格式 | 4（0） | 0 | OutputStream 覆盖写改成 fileIo：打开加 TRUN… |
| `lesson-8534b92df38e546092fe` | data/files | 新格式 | 7（0） | 1（是） | 文件导入导出按源端运行时与库默认语义实现：OOM 兜底不改成读前大小… |
| `lesson-ff5e8fbfb9ed491d99ee` | data/files | 新格式 | 3（0） | 0 | 源端在后台线程执行的文件拷贝与导入改用异步 IO 或 taskpoo… |
| `lesson-22f5100f6718eaecc66f` | data/model | 新格式 | 0（0） | 1（是） | 宿主或适配层给展示型 UI 模型赋值时逐字段按源端绑定取值：code… |
| `lesson-7caea06acbf8f99d6128` | data/model | 新格式 | 2（0） | 0 | SDK 序列化的枚举分开写线上形态与本地持久化形态：kotlinx.… |
| `lesson-9f2d3b8b099a927b53f4` | data/model | 新格式 | 1（0） | 0 | 模型字段按源端类型与构造路径建模：装箱数值不改成字符串域，null … |
| `lesson-b92a8a56aee6db5e9c52` | data/model | 新格式 | 0（0） | 0 | 把以字符串持久化的模型枚举映射到页面本地类型时，按模型枚举成员逐一 … |
| `lesson-c066489fcf35ab37378c` | data/model | 新格式 | 3（0） | 0 | 服务器下发的大整数 id 在 JSON.parse 之前保住原文：源… |
| `lesson-c73deaf6f27d3426c4e9` | data/model | 新格式 | 2（0） | 0 | 逐字段搬运 Builder 或构造调用时，同时核对两端模型字段的单位 |
| `lesson-246252824c631aa6eff5` | data/network | 新格式 | 2（0） | 1（是） | 服务地址与环境沿地址键名追到源端常量与取址逻辑：分清各接口族的 ho… |
| `lesson-faec7be031b7f64752c4` | data/network | 新格式 | 5（0） | 1（是） | 源端声明 INTERNET（及 ACCESS_NETWORK_STA… |
| `lesson-0caaa4efc70dad90a15f` | data/parsing | 新格式 | 6（0） | 1（是） | 备份/导出 JSON 按 org.json 或 Gson 库语义序列… |
| `lesson-2622bc32995ac62389c3` | data/parsing | 新格式 | 3（0） | 1（是） | 自写 fromJson 从宽类型输入取值时用 typeof/inst… |
| `lesson-5034b56be6fd828164c9` | data/parsing | 新格式 | 6（0） | 1（是） | 翻译源端 JSON 解析时按源解析器与取值 API 的语义定规则：o… |
| `lesson-871d3751cadde6dda1dc` | data/parsing | 新格式 | 3（0） | 1（是） | 显式 JSON 解码器按源解析器的接受范围和源数据的实际类型定规则：… |
| `lesson-5c101b4b3f08ab317202` | data/schema | 新格式 | 1（0） | 1（是） | 手写 relationalStore 插入语句时省略 Room au… |
| `lesson-65358a02b1bf9ef652d3` | data/schema | 新格式 | 5（0） | 1（是） | 用 relationalStore 重写 SQLiteOpenHel… |
| `lesson-a078efd3361b4abe58e3` | data/schema | 新格式 | 8（0） | 3（是） | relationalStore 事务体含 await 时用 crea… |
| `lesson-a6f300f9295ba538f23b` | data/schema | 新格式 | 4（0） | 1（是） | Room 数据库落成 relationalStore 时保留库名、s… |
| `lesson-c55c56444f5271471a64` | data/schema | 新格式 | 1（0） | 0 | 手写 relationalStore 建表 SQL 时给表名与列名统… |
| `lesson-488a3bd782acef92f5cf` | data/seeding | 新格式 | 1（0） | 1（是） | 源端在首次建库回调里播种时，目标把播种放进建表分支的同一事务并写入种… |
| `lesson-dc3f2589254d02893b0e` | data/seeding | 新格式 | 3（0） | 1（是） | 源端在应用启动时按标记首次播种、设置中可重置时，目标在启动路径落实际… |
| `lesson-1d3ab8b9d39bd8f6e24d` | data/sync | 新格式 | 1（0） | 0 | 源端不等待的落库改为异步写后，在落库完成后再广播触发重查的事件 |
| `lesson-32c7d4b2ada4b341778d` | data/sync | 新格式 | 4（0） | 1（是） | greenrobot EventBus 迁移先核投递契约：需同步按引… |
| `lesson-29744eb694376e8acaca` | process/build | 新格式 | 9（0） | 3（是） | 编译修复只改报错定位的行与符号，不以删掉功能或语义不同的替代换取通过… |
| `lesson-6dae0bf2657b0e339742` | process/build | 新格式 | 2（0） | 0 | 用 shell 一行命令或脚本改写含 $ 或反斜杠转义的 ArkTS… |
| `lesson-776ed5eb216833c6b002` | process/gates | 新格式 | 2（0） | 1（是） | 写文件以真实执行回执为准：只有文本形式的工具调用即未写入；覆盖模板入… |
| `lesson-8390913de64b0adc00fc` | process/gates | 新格式 | 0（0） | 0 | 处理孤儿检测报出的无调用方页面或弹窗时，已登记为范围内的产物不删除：… |
| `lesson-9147be4d87153de9c5b6` | process/gates | 新格式 | 0（0） | 1（是） | 功能对齐与验收结论逐项以代码落点为准：按规格验收项与导航出口检索实际… |
| `lesson-ad6f23b88f09b55dd92a` | process/gates | 新格式 | 2（0） | 0 | 用共享组件替换页面已实现片段前（关闭孤儿组件检查或按计划收口），完整… |
| `lesson-afae8d13e00941efe808` | process/gates | 新格式 | 3（0） | 1（是） | 交互问题先复现并分层定位、确认触摸可达再改约束；未经设备验证、被阻断… |
| `lesson-bdb97da6a6eb8d68435f` | process/gates | 新格式 | 5（0） | 0 | 运行会改写源码的自愈脚本后先审阅其改动；异常尺寸、与已有显式尺寸重复… |
| `lesson-f6b95d7d6d0159cb0436` | process/gates | 新格式 | 3（0） | 1（是） | 修复安全区等按关键字判定的结构检查时逐页落实实现，不用含检查关键字的… |
| `lesson-033b8254b5b6de0bd9e1` | process/input-loading | 新格式 | 22（0） | 5（是） | 页面、控件、算法或实体基类由二进制三方库承载时，按依赖坐标取库制品核… |
| `lesson-35f4f9b3cf566d33e79c` | process/input-loading | 新格式 | 0（0） | 0 | 依据另一文件的返回语义改写调用方前，重读该文件当前版本；编辑回执提示… |
| `lesson-6a3a7f46c8fec282affa` | process/input-loading | 新格式 | 0（0） | 0 | Windows PowerShell 5.1 读取 UTF-8 中文… |
| `lesson-b3f534eb740a768d95a6` | process/input-loading | 新格式 | 10（0） | 0 | 源端行为依赖的辅助方法、谓词、getter 与框架约定，要读到定义再… |
| `lesson-3348c580951ef82a9737` | process/scope | 新格式 | 9（0） | 1（是） | 写应用壳契约与实施计划时枚举源导航模块的全部入口能力（含深链解析与 … |
| `lesson-7827e0707780cb7546ee` | process/scope | 新格式 | 5（0） | 1（是） | 落盘差异决策时，以成本、复杂度或“首版不做”为理由的降级按范围裁剪处… |
| `lesson-35b9cdfd5d22ce53465e` | process/task-handoff | 新格式 | 0（0） | 0 | 规格把实现路径写成“由后续决策轮裁决”时，后续决策轮逐条出题或关闭；… |
| `lesson-447ba5818e4e203272e8` | process/task-handoff | 新格式 | 0（0） | 1（是） | 页面先于共享组件或共享工具实现时，页内等价实现登记为待收敛项；共享件… |
| `lesson-4f81eeea17b94190c2de` | process/task-handoff | 新格式 | 3（0） | 0 | 要靠其他文件或任务补实现的功能，登记成带负责方、验证方式和源端确定值… |
| `lesson-5754b7be28238f1bdf57` | process/task-handoff | 新格式 | 5（0） | 0 | 编排者推进阶段、拆分重派或派发下游前，核对约定产物与放行门，把回报里… |
| `lesson-73a7dd4f78cb747f7e7e` | process/task-handoff | 新格式 | 1（0） | 0 | 派工转述规则或把某任务的局部做法推广为派工规则时，连同原文的替代写法… |
| `lesson-8a7d25959b954ffb9215` | process/task-handoff | 新格式 | 0（0） | 1（是） | 把 fragment 内容交给共享组件、宿主页另建容器时，fragm… |
| `lesson-a2f6a4ae9a72be740de6` | process/task-handoff | 新格式 | 8（0） | 1（是） | “不确定”“待补资源”“无等价”“延期”“契约未确认”这类占位只登记… |
| `lesson-ae78da6f1a3669f6ef59` | process/task-handoff | 新格式 | 0（0） | 0 | 子代理派发失败先按报错修正参数重试；确需改由主线程执行时，按 ski… |
| `lesson-eb4de4fd7452308a0483` | process/task-handoff | 新格式 | 1（0） | 1（是） | 解决前向占位时按登记的触发文本逐项兑现：只接一半、写成常量或删掉标记… |
| `lesson-5bc9af19bedaecaf627c` | process/testing | 新格式 | 1（0） | 1（是） | 为迁移代码定预期值或写验收样例时按源端实现逐步手算（源式含 floa… |
| `lesson-42364ad323112c3342ae` | process/visual-review | 新格式 | 6（0） | 2（是） | 按源端截图复刻控件尺寸时，先判断实测值是内容测量结果还是框架 min… |
| `lesson-aae5f345ed2ced099757` | process/visual-review | 新格式 | 0（0） | 1（是） | 为颜色差异立单时，用像素均值和源端算式给出期望值，再建议混合方式 |
| `lesson-5caf7eadb69e940926f9` | ui/accessibility | 新格式 | 4（0） | 1（是） | 转写 Compose 可点击行与卡片时一并落实无障碍语义：role … |
| `lesson-d80ced7be82765244889` | ui/accessibility | 新格式 | 2（0） | 1（是） | 图标无障碍文本按源 contentDescription 转写：nu… |
| `lesson-6d6ba721c81206d45fbe` | ui/animation | 新格式 | 6（0） | 2（是） | 帧时钟动画（Animatable、ValueAnimator）改自驱… |
| `lesson-a4e6bcfb28597691c028` | ui/animation | 新格式 | 6（0） | 2（是） | Compose 的显隐、内容切换、尺寸与条目位移动画（Animate… |
| `lesson-fef54f39225a043ac692` | ui/animation | 新格式 | 2（0） | 0 | 把 AnimatedVisibility 等条件块改成常驻折叠容器时… |
| `lesson-0a26e0cfc44a183d3a02` | ui/dialog | 新格式 | 8（0） | 0 | 用页内覆层承载 Activity 级 Dialog 时挂在覆盖整窗的… |
| `lesson-18fca50f9c801cb282ec` | ui/dialog | 新格式 | 9（0） | 1（是） | 源对话框带目标系统弹窗没有的槽位（setView 注入的复选框等自定… |
| `lesson-1c27b6c7cf05c05733d9` | ui/dialog | 新格式 | 2（0） | 1（是） | ComponentContent 构造即执行 builder：构造后… |
| `lesson-1f366fe4ccdc917ce0fc` | ui/dialog | 新格式 | 8（0） | 1（是） | 源弹窗按它实际加载的布局 XML、函数全文或依赖库模板逐控件还原并接… |
| `lesson-21db515a505be4845497` | ui/dialog | 新格式 | 10（0） | 1（是） | 按源弹层类型逐个选呈现形态：居中 CustomDialog/Aler… |
| `lesson-29f62d177a17d08b4e4f` | ui/dialog | 新格式 | 6（0） | 0 | 依附式弹窗（AttachPopup）的宿主按锚点视图所在页面确定：提… |
| `lesson-368c4592e4c7075c1871` | ui/dialog | 新格式 | 19（0） | 4（是） | 源端 XPopup/DialogFragment 真弹窗（居中、锚点… |
| `lesson-3f3e1ff0a4d0e0299bda` | ui/dialog | 新格式 | 4（0） | 1（是） | @ComponentV2 页面的弹窗不用 CustomDialogC… |
| `lesson-5f8833721d3c4a11c60a` | ui/dialog | 新格式 | 0（0） | 0 | 源端弹窗展开后才加载数据时，先打开弹层再在弹层内异步加载，带加载中与… |
| `lesson-666a746081ba1e447322` | ui/dialog | 新格式 | 14（0） | 2（是） | 锚定弹出的下拉（PopupWindow showAsDropDown… |
| `lesson-6d3ac9a5c0382377b91e` | ui/dialog | 新格式 | 0（0） | 1（是） | 源端把入口委托给跨页面共享组件（详情弹窗、公共分享弹层）时，目标检索… |
| `lesson-96eea0feeae116ef9262` | ui/dialog | 新格式 | 1（0） | 0 | 页内遮罩承载源端对话框时，显示期间把背景内容移出无障碍树：acces… |
| `lesson-a3ac761b0d52a6bccb9f` | ui/dialog | 新格式 | 2（0） | 0 | 从组件外的共享函数打开自定义弹窗时，用 wrapBuilder + … |
| `lesson-b366cf7ae68525577f57` | ui/dialog | 新格式 | 1（0） | 0 | 源端应用内分享面板按交互形态复用目标的应用内分享弹层，并逐渠道映射（… |
| `lesson-39077e6612d5f97b0731` | ui/dialog/appearance | 新格式 | 8（0） | 2（是） | MaterialAlertDialog 卡片外观按源主题代际取值，每… |
| `lesson-9c4de55af3c1ecd8eaa4` | ui/dialog/appearance | 新格式 | 24（0） | 3（是） | 只靠平台默认外观的 AlertDialog（含 DialogPref… |
| `lesson-009212ca2c691b97d76c` | ui/dialog/sheets | 新格式 | 6（0） | 0 | 从 bindSheet 半模态里打开的弹窗必须叠在 sheet 之上… |
| `lesson-97bf3cf56f55715f7e42` | ui/dialog/sheets | 新格式 | 6（0） | 1（是） | 会从半模态内压入 Navigation 页的弹层用 SheetMod… |
| `lesson-b661a3a6a4c0a1e2a3c9` | ui/dialog/sheets | 新格式 | 1（0） | 0 | 多个相互独立的底部弹层不在同一组件上链式 bindSheet：分别挂… |
| `lesson-df1f691759f84ba9e688` | ui/dialog/sheets | 新格式 | 8（0） | 1（是） | BottomSheetDialogFragment 或 Compos… |
| `lesson-1a66114fb7523a1f9af1` | ui/effects | 新格式 | 13（0） | 1（是） | 位图着色（ColorFilter.tint、setColorFilt… |
| `lesson-4ce3a1c186651285f362` | ui/effects | 新格式 | 5（0） | 1（是） | Compose 渐变按端点几何换算成 ArkUI linearGra… |
| `lesson-d0aad947e26220fb43fa` | ui/effects | 新格式 | 11（0） | 1（是） | elevation 投影写入 ShadowOptions 时按 px… |
| `lesson-187c725b1bb9d8d1bf4d` | ui/feedback | 新格式 | 4（0） | 2（是） | 源端单一提示宿主（SnackbarHost、三方提示条库的全局队列）… |
| `lesson-8335bc404934f58c6f31` | ui/feedback | 新格式 | 6（0） | 3（是） | 公共 Toast 封装把时长做成每次调用的参数，逐调用点映射源端 L… |
| `lesson-a7f81d00f3aefd7cc618` | ui/feedback | 新格式 | 8（0） | 0 | Compose M3 不传 progress 的进度指示器与 Pul… |
| `lesson-ac7a2e17b8d88c3cee7b` | ui/feedback | 新格式 | 6（0） | 0 | 迁移源端异步结果回调时，按成功、失败分支（含失败类型）列出全部副作用… |
| `lesson-7708f650eb4b55dce045` | ui/graphics | 新格式 | 11（0） | 1（是） | android:background 的整屏背景位图按拉伸铺满映射，… |
| `lesson-943544ce27bf04f9faf8` | ui/graphics | 新格式 | 14（0） | 2（是） | 图标按源端原始资源落实：缺失时从 Android 密度目录、SDK … |
| `lesson-bdc493f5950835f9bfcc` | ui/graphics | 新格式 | 24（0） | 1（是） | 图标按资源固有 dp 显示、触摸盒放在外层：centerInside… |
| `lesson-e6b1f9094ec3b905cab5` | ui/graphics | 新格式 | 6（0） | 0 | AnimatedImageVector/animated-vecto… |
| `lesson-f395cbdf6742a7f4c761` | ui/graphics | 新格式 | 0（0） | 0 | 移植自适应尺寸公式时把参照基数（如按 6 周计算的参考格高）写成独立… |
| `lesson-046c8bbb304684669060` | ui/graphics/canvas | 新格式 | 7（0） | 0 | 把预烘焙位图改为每帧矢量绘制前，保留位图隐含的取值时机与缩放语义：烘… |
| `lesson-27d9e16a099c2fb437eb` | ui/graphics/canvas | 新格式 | 7（0） | 0 | View.invalidate 迁成唯一的“请求下一帧绘制一次”入口… |
| `lesson-351ce34d3ebe51b8ff8e` | ui/graphics/canvas | 新格式 | 3（0） | 0 | ArkUI Canvas 的内容跨帧保留：把 onDraw 移植为反… |
| `lesson-4da9eabca745b3b2be91` | ui/graphics/canvas | 新格式 | 13（0） | 2（是） | SurfaceView 自建线程的 lockCanvas 循环按线程… |
| `lesson-68717b80482f4bd12825` | ui/graphics/canvas | 新格式 | 4（0） | 0 | Canvas.drawText 移植为 fillText 时按每串首… |
| `lesson-7083c6ad69ab19ad17dd` | ui/graphics/canvas | 新格式 | 16（0） | 1（是） | 按 Android px 公式移植自绘 View 时先定画布上下文单… |
| `lesson-74295d12b4edc025569f` | ui/graphics/canvas | 新格式 | 5（0） | 1（是） | Canvas 字体串按注册字族名原样引用、不加源端没有的 bold；… |
| `lesson-c3bd9c8b2f24c209a659` | ui/graphics/canvas | 新格式 | 11（0） | 0 | 源端位图按密度解码、createScaledBitmap 预缩放后原… |
| `lesson-f876887b216b6caf9f39` | ui/graphics/canvas | 新格式 | 8（0） | 0 | 移植 Paint 文字度量前先按源 API 分层：getTextBo… |
| `lesson-0457a04c31208e1fb916` | ui/input | 新格式 | 14（0） | 3（是） | EditText 的 inputType 键盘与候选提示和内容约束分… |
| `lesson-1150c0c721e6dc0dede4` | ui/input | 新格式 | 10（0） | 2（是） | 按 EditText 对齐 TextInput 时，未声明 back… |
| `lesson-5d1c2c78b5c27d9c5e97` | ui/input | 新格式 | 10（0） | 2（是） | EditText.setError 迁为尾部错误图标加仅聚焦时显示的… |
| `lesson-617ffbd840398cf95efc` | ui/input | 新格式 | 5（0） | 2（是） | 源端受控输入框的拒绝条件要阻止文本显示：长度上限用 TextInpu… |
| `lesson-a5aeed3d4c376cd085d1` | ui/input | 新格式 | 3（0） | 2（是） | 金额类输入可含小数时不用 InputType.Number：按源端解… |
| `lesson-bc79621b279ff82517ab` | ui/input | 新格式 | 1（0） | 1（是） | 受控值含文本与选区（TextFieldValue）时，选区经 Tex… |
| `lesson-c3a3797da8b412c31aa7` | ui/input | 新格式 | 3（0） | 1（是） | Compose Switch 的 thumbContent（如选中时… |
| `lesson-d53223f43ad454261f26` | ui/input | 新格式 | 1（0） | 1（是） | 源码用 selectable 行加条件尾部勾选表示选中时按同一结构实… |
| `lesson-d715fa78ada2e79a5fd2` | ui/input | 新格式 | 3（0） | 1（是） | Compose Slider 的 steps 是两端之间的离散值个数… |
| `lesson-edc9465d3902807c386b` | ui/input | 新格式 | 10（0） | 2（是） | 菜单 SearchView 迁成自绘搜索栏时把展开、焦点、提交、收起… |
| `lesson-ef93bb2086aef9604aa1` | ui/input | 新格式 | 4（0） | 0 | 源端同一控件既可编辑又分段着色（EditText + Spannab… |
| `lesson-9d42548ee3c075de3330` | ui/input/focus-ime | 新格式 | 2（0） | 1（是） | 首屏输入框按源端平台缺省获焦时，在窗口获焦后再 requestFoc… |
| `lesson-edae4e2795ec169255bb` | ui/input/focus-ime | 新格式 | 5（0） | 1（是） | 只收键盘不清焦点用 hideTextInput：show/hideS… |
| `lesson-4a4f8d845a204ffa244b` | ui/interaction | 新格式 | 13（0） | 1（是） | Stack 上层全尺寸容器和页面级遮罩会参与命中测试：不处理点击的覆… |
| `lesson-68023ac5f088c72a775a` | ui/interaction | 新格式 | 14（0） | 0 | 源端 onTouch 自己按未掩码 getAction 只跟随首指时… |
| `lesson-7389433391eddbaea827` | ui/interaction | 新格式 | 7（0） | 1（是） | Image 承载点击/长按按钮或自绘拖拽柄时设 draggable(… |
| `lesson-7f5eba1b969bddfb34dc` | ui/interaction | 新格式 | 3（0） | 0 | SwipeToDismissBox 的滑删方向按物理手势和 offs… |
| `lesson-80e1d2c095a3698a7156` | ui/interaction | 新格式 | 6（0） | 1（是） | Activity 级 onKeyDown 映射到页面根节点（NavD… |
| `lesson-8a752faf9f5dff52e3ff` | ui/interaction | 新格式 | 2（0） | 1（是） | Compose combinedClickable 的长按自带系统触… |
| `lesson-99080bd3bfc1bcbb9c5f` | ui/interaction | 新格式 | 7（0） | 0 | 源端禁用态只靠代码换背景、文字色固定时，不用 ArkUI .enab… |
| `lesson-cf018b76af68b4c00895` | ui/interaction | 新格式 | 5（0） | 1（是） | 弹窗防穿透的 Block 只放在无子控件的遮罩层，内容面板与根容器保… |
| `lesson-ed5556325b6d8f510e2f` | ui/interaction | 新格式 | 0（0） | 0 | Button 内按状态切换图标时写成一个 if/else 或单个 I… |
| `lesson-f122d4c4d386c60fd8d5` | ui/interaction | 新格式 | 4（0） | 1（是） | 行组件内挂了 onClick 时外层 ListItem 的 onCl… |
| `lesson-f3e614f295aa409485fd` | ui/interaction | 新格式 | 1（0） | 1（是） | 源端监听回调体被注释时按无响应控件迁移；审计不因“已裁定/集成点”注… |
| `lesson-fd3add7128663eb9998f` | ui/interaction | 新格式 | 5（0） | 1（是） | 点击事件挂在源端真正持有点击的节点上：源端只绑整栏就挂外层，只绑行内… |
| `lesson-fde79829831c2269e925` | ui/interaction | 新格式 | 17（0） | 2（是） | 源端可点击容器自带的按压反馈（Compose clickable、C… |
| `lesson-148a3e67bd557bafd722` | ui/layout | 新格式 | 5（0） | 1（是） | 源 manifest 未声明 android:supportsRtl… |
| `lesson-51bf52bc666b921ef2e9` | ui/layout | 新格式 | 7（0） | 0 | values-sw<N>dp(-land) 覆盖按设备屏幕短边 mi… |
| `lesson-786a04847bf10d364d9d` | ui/layout | 新格式 | 7（0） | 0 | 源应用声明 supportsRtl=true 时保留逻辑方向：sta… |
| `lesson-a6121cc7eaf207b702f7` | ui/layout | 新格式 | 21（0） | 3（是） | 导航图标与菜单分区按实际生效者实现：DrawerToggle 画汉堡… |
| `lesson-c8e645a542254d96997e` | ui/layout | 新格式 | 7（0） | 0 | 源布局（含 include 引入的布局）有 layout-land、… |
| `lesson-f1a98587fe72ff68c5a8` | ui/layout | 新格式 | 2（0） | 1（是） | 页面转换逐项落实源 XML 的 gone 节点（代码只绑点击、没有设… |
| `lesson-08b9064f678f1635e647` | ui/layout/constraints | 新格式 | 18（0） | 3（是） | 源端默认起始对齐和贴顶要显式写出：Android 与 Compose… |
| `lesson-92aee54a305ea0bde363` | ui/layout/constraints | 新格式 | 14（0） | 1（是） | Stack 中内容尺寸的子项按 alignContent 定位：子项… |
| `lesson-29b42ac7502c0f284b9a` | ui/layout/scrolling | 新格式 | 2（0） | 1（是） | Compose LazyColumn 默认无滚动条：ArkUI Li… |
| `lesson-4030f978a230df37de2b` | ui/layout/scrolling | 新格式 | 3（0） | 1（是） | LazyRow/LazyColumn 的 contentPaddin… |
| `lesson-420023d472f48bed8ef9` | ui/layout/scrolling | 新格式 | 2（0） | 0 | heightIn(max) 紧接 verticalScroll 的卡… |
| `lesson-46a0d7f239efac925d33` | ui/layout/scrolling | 新格式 | 3（0） | 0 | 转换滚动区时只把源滚动容器内的子节点放进 Scroll/List，固… |
| `lesson-67ab02abe6ec76f4129e` | ui/layout/scrolling | 新格式 | 3（0） | 0 | 源端 exitUntilCollapsed 连续折叠顶栏按滚动偏移算… |
| `lesson-80dd4e626e1c207028e6` | ui/layout/scrolling | 新格式 | 14（0） | 2（是） | ScrollView 未写 overScrollMode、Compo… |
| `lesson-caa043fb95ff63e321e2` | ui/layout/scrolling | 新格式 | 4（0） | 1（是） | LazyRow 摘要行转成可横滑容器，不降成普通 Row：少量固定项… |
| `lesson-f0a40d990c62738fc04e` | ui/layout/scrolling | 新格式 | 3（0） | 0 | LazyListState.scrollToItem/animate… |
| `lesson-0ef2cd00e1a91491b350` | ui/layout/sizing | 新格式 | 11（0） | 1（是） | 源端在整数 px 上取整的布局公式：规格写明运算域，实现在 px 域… |
| `lesson-5c6217b05bb4c266f254` | ui/layout/sizing | 新格式 | 5（0） | 1（是） | Compose Modifier 链里位于背景之前的内距与 inse… |
| `lesson-624248be2c5f81082268` | ui/layout/sizing | 新格式 | 5（0） | 1（是） | 将图片内容缩放与组件尺寸约束分别落实：wrap_content + … |
| `lesson-75f4743dff663f50966b` | ui/layout/sizing | 新格式 | 20（0） | 5（是） | “父尺寸减边距”或“扣除兄弟后的剩余空间”不写成 '100%'：ma… |
| `lesson-a58ebfe7a4c55b041b14` | ui/layout/sizing | 新格式 | 24（0） | 2（是） | 由内容定尺寸的父级（列表行、wrap_content 头部、FIT_… |
| `lesson-adad817f2c3c8f1eaa09` | ui/layout/sizing | 新格式 | 11（0） | 2（是） | LinearLayout 的 weightSum 与子权重之和不等，… |
| `lesson-b73a1ac8908f74856a02` | ui/layout/sizing | 新格式 | 2（0） | 0 | 区分 Material 按钮的布局占位、背景实绘与触控范围：不只凭调… |
| `lesson-e3077bf60cfc3f34d0a2` | ui/layout/sizing | 新格式 | 3（0） | 1（是） | layout_marginStart/End 写成 margin 的… |
| `lesson-09a0bceae55d05616ecc` | ui/list | 新格式 | 2（0） | 0 | 会换位或增删的列表，位置相关值（首尾标记、序号、上移/下移可用态、首… |
| `lesson-e01c6f821d631fad5383` | ui/list | 新格式 | 1（0） | 1（是） | ExpandableListView 未设组点击监听时组头仍按默认切… |
| `lesson-e17b45a28a8d92ecbd01` | ui/list | 新格式 | 2（0） | 0 | 多类型 Adapter 承载的页面按全部 item 布局和 hand… |
| `lesson-396d54479492828eeea3` | ui/navigation/back-stack | 新格式 | 14（0） | 4（是） | 源端对话框、底部弹层或下拉菜单改成页内覆盖层后，在宿主 onBack… |
| `lesson-39f137ee173e50363f79` | ui/navigation/back-stack | 新格式 | 9（0） | 0 | 底部 tab 的 popUpTo(start){saveState}… |
| `lesson-69229aa8c7b051229f26` | ui/navigation/back-stack | 新格式 | 1（0） | 1（是） | 源端用 NavController.handleDeepLink 处… |
| `lesson-803ba029eea852122e77` | ui/navigation/back-stack | 新格式 | 7（0） | 1（是） | 被 @Entry 页直接组合、未进入 Navigation 栈的子组… |
| `lesson-96c890012b26b5cb32cd` | ui/navigation/back-stack | 新格式 | 2（0） | 0 | 源端 popUpTo(根){inclusive=true} 加 na… |
| `lesson-efff93743d668b55b55a` | ui/navigation/back-stack | 新格式 | 8（0） | 0 | 唯一页面被压在空的 Navigation 首页之上时，由栈底 Nav… |
| `lesson-f19632971e470d55c543` | ui/navigation/back-stack | 新格式 | 1（0） | 0 | 源端返回按钮与 onBackPressed 执行同一逻辑时共用同一处… |
| `lesson-0b72c197ea20fbe6f277` | ui/navigation/hosts | 新格式 | 2（0） | 1（是） | 一进入就无条件跳转并 finish 的 Activity 是路由跳板… |
| `lesson-19dd006e049c3f9d7563` | ui/navigation/hosts | 新格式 | 6（0） | 1（是） | 源端在导航目的地内用 LocalLifecycleOwner 观察 … |
| `lesson-1cebb531c991239d2691` | ui/navigation/hosts | 新格式 | 3（0） | 1（是） | 嵌在 Swiper/Tabs 里的页面组件只用 @Consumer … |
| `lesson-2ed8c21943925bf0ae9a` | ui/navigation/hosts | 新格式 | 2（0） | 1（是） | 源端一个 Composable 内多屏共享的清理，拆成多页面后归属外… |
| `lesson-69e07207a06a8a8a7ba9` | ui/navigation/hosts | 新格式 | 4（0） | 1（是） | 根 Navigation 只作路由容器时显式隐藏默认标题栏和工具栏 |
| `lesson-6c474c15ac28fca733a1` | ui/navigation/hosts | 新格式 | 2（0） | 1（是） | 路由表只注册以 NavDestination 为根的组件：Tab 内… |
| `lesson-8953e390416a80d7dd8c` | ui/navigation/hosts | 新格式 | 6（0） | 0 | 入口页 Navigation 宿主：NavDestination 首… |
| `lesson-9886f489045488c8b454` | ui/navigation/hosts | 新格式 | 8（0） | 1（是） | 源 Activity 或其基类 onCreate 调 overrid… |
| `lesson-9de3322165e533d6b790` | ui/navigation/hosts | 新格式 | 2（0） | 0 | NavHost 的 enter/exit/popEnter/popE… |
| `lesson-c4a6eaaf6a22c0b8823f` | ui/navigation/hosts | 新格式 | 4（0） | 1（是） | main_pages.json 只登记经 router 进入或由 l… |
| `lesson-0d7d6e7302f8c8c77c66` | ui/navigation/parameters | 新格式 | 2（0） | 1（是） | 经 router.pushUrl 进入的 @Entry 页在 abo… |
| `lesson-14509c64bd43100ce443` | ui/navigation/parameters | 新格式 | 2（0） | 2（是） | 源端带结果回调的选择器（show(..., 当前值) { resul… |
| `lesson-300200dd52892e9dadd2` | ui/navigation/parameters | 新格式 | 1（0） | 1（是） | Compose 带参路由迁到 NavPathStack 时，目的地名… |
| `lesson-32af50a1dfb0c1c254af` | ui/navigation/parameters | 新格式 | 3（0） | 0 | 源页面由点击回调经 ViewModel 副作用导航时，逐个导航出口在… |
| `lesson-4a7c04b864ef635c87b6` | ui/navigation/parameters | 新格式 | 2（0） | 1（是） | 路由参数以接收端契约为准：接收方不读取或写死的 extra 不透传，… |
| `lesson-953309e05bc1cd36c0d1` | ui/navigation/parameters | 新格式 | 1（0） | 1（是） | 同一目标页有多个启动入口时，按全部源端入口的 Intent extr… |
| `lesson-b714378f18d168bce81c` | ui/navigation/parameters | 新格式 | 6（0） | 1（是） | pushPathByName 传参用目标页 instanceof 的… |
| `lesson-dfcdbb19cd93d29159b2` | ui/navigation/parameters | 新格式 | 0（0） | 0 | 源端跳转前写入的共享状态（如播放队列）是跳转契约的一部分，按原顺序迁… |
| `lesson-ccccf83dc93ae809ccfb` | ui/pager | 新格式 | 3（0） | 1（是） | 分页容器的初始页用 Swiper.index 状态绑定，不在 onR… |
| `lesson-0e1c846868f2683cc280` | ui/safearea | 新格式 | 24（0） | 1（是） | 仅当源窗口内容延伸到系统栏下，或窗口背景是按窗口尺寸拉伸或定位的位图… |
| `lesson-2cf2614847a8dba832b3` | ui/safearea | 新格式 | 3（0） | 1（是） | 向子页或页内浮层下发状态栏高度参数时写明消费方式，挂在同一 Stac… |
| `lesson-824031d5fddf81036b54` | ui/safearea | 新格式 | 6（0） | 2（是） | 系统栏图标深浅按源端浅色状态栏标志推导：未设标志时安卓图标为白色，不… |
| `lesson-8bc258c2833be65f4fcd` | ui/safearea | 新格式 | 4（0） | 1（是） | 源端只在三键导航时给导航栏着色：以 TYPE_SYSTEM 底部避让… |
| `lesson-8e0e9fe5373a2bbe47af` | ui/safearea | 新格式 | 5（0） | 2（是） | 页面级安全区订阅从承载页面的主窗口取窗口对象：复用工程主窗口入口或入… |
| `lesson-a8452bfea5d42d3dcae3` | ui/safearea | 新格式 | 15（0） | 1（是） | 开启全屏布局前逐边核对源端系统栏：只沉浸状态栏（透明状态栏、未设 n… |
| `lesson-c7ee1769ca29abd236d3` | ui/safearea | 新格式 | 6（0） | 2（是） | 全屏窗口下先确认路由页的内容原点：已在状态栏 inset 之下就只补… |
| `lesson-cde4120ab9ad7412b1da` | ui/safearea | 新格式 | 11（0） | 0 | 自绘标题栏接入顶部安全区前先判定源端由谁避让：根 fitsSyste… |
| `lesson-cf111aadb8804649b578` | ui/safearea | 新格式 | 8（0） | 2（是） | getWindowAvoidArea 与 windowRect 的数… |
| `lesson-f64afc22d41b130f1628` | ui/safearea | 新格式 | 3（0） | 1（是） | Compose Scaffold 无 topBar 时 innerP… |
| `lesson-f86b02e97cc77e31d51a` | ui/safearea | 新格式 | 6（0） | 1（是） | 源窗口按 adjustResize 避让软键盘（声明 adjustR… |
| `lesson-fe10bd2491ca4ba82cb5` | ui/safearea | 新格式 | 1（0） | 1（是） | 状态栏实色避让带挂在只承担避让的外层 Column：宿主是 Tabs… |
| `lesson-08c38f950b69e991607d` | ui/state | 新格式 | 12（0） | 1（是） | 页面直接读共享 @ObservedV2 模型的 @Trace 字段，… |
| `lesson-0cc7ae4eec0a59086202` | ui/state | 新格式 | 2（0） | 3（是） | 用 @Monitor 监听数组路径代替 collect 时，生产方按… |
| `lesson-14b7f4090b7b83873b22` | ui/state | 新格式 | 3（0） | 1（是） | 页面向单例仓库或偏好注册监听时，把回调或句柄存成字段，在 about… |
| `lesson-1f6e36f8e8bf9df951da` | ui/state | 新格式 | 2（0） | 1（是） | 翻译“离开组合即销毁”的状态复位时，同时列出目标框架会替用户恢复的界… |
| `lesson-1fa08bf929cfced0ff34` | ui/state | 新格式 | 0（0） | 0 | 源端用带兜底的访问器取显示值时，目标调用已移植的等价访问器，不改读原… |
| `lesson-2e636699fa65aefd63f0` | ui/state | 新格式 | 15（0） | 1（是） | 列表条目以新对象替换或整表重建时，ForEach/Repeat 键要… |
| `lesson-3117bc9457610b1c2671` | ui/state | 新格式 | 2（0） | 0 | 源端 data class copy/replaceAll 更新译为… |
| `lesson-3b4a96141329db62a6af` | ui/state | 新格式 | 2（0） | 1（是） | 迁移 Compose remember 状态时按源端的求值与重建时机… |
| `lesson-40fc63b124b4a44e7a9f` | ui/state | 新格式 | 2（0） | 1（是） | 复用开关组件的变更事件给出目标值时，把它原样写入该开关的 sette… |
| `lesson-43a9050245b1afa165bf` | ui/state | 新格式 | 2（0） | 1（是） | 迁移按状态切换的显示时同时迁移 setVisibility 分支：该… |
| `lesson-4d1c980bbbd20275f5c3` | ui/state | 新格式 | 1（0） | 0 | 判定模型字段不需要可观察之前，先读修改它的方法和显示它的界面 |
| `lesson-5d6e099ff0c8965f2b3c` | ui/state | 新格式 | 2（0） | 2（是） | 源端以引用比较判断“有未保存改动”时，先确认未改动时两侧是同一对象；… |
| `lesson-5e235f283f120703784e` | ui/state | 新格式 | 3（0） | 0 | 把 @Monitor 改成生产方显式回调时，保留“被监听字段变化才执… |
| `lesson-7508ddc52eaf816887f0` | ui/state | 新格式 | 5（0） | 1（是） | AppStorageV2/PersistenceV2 的 key 只… |
| `lesson-8d2979542fa2cd65150c` | ui/state | 新格式 | 13（0） | 2（是） | 随状态变化的控件参数不作 @Builder 值参，改为内联读取状态或… |
| `lesson-b3bb0bc33f4caded78a2` | ui/state | 新格式 | 14（0） | 2（是） | 源页面在每次可见时、或由事件订阅与结果回调触发的重新加载，要迁成可见… |
| `lesson-c883a0ff96c32dfbd9ba` | ui/state | 新格式 | 2（0） | 1（是） | 共享单例 ViewModel 按规格的键丢弃过期响应，页面各加载入口… |
| `lesson-d7c148c4a233c59ff151` | ui/state | 新格式 | 2（0） | 0 | 把源界面的生命周期回调迁入 ViewModel 刷新方法时逐条迁移全… |
| `lesson-d9143de006714935afe2` | ui/state | 新格式 | 0（0） | 0 | 源端 Activity 实例字段承载的会话态映射为页面实例作用域：服… |
| `lesson-22432022455bff6f849b` | ui/text | 新格式 | 6（0） | 2（是） | resourceManager 代码内取值（字符串、数组、复数、颜色… |
| `lesson-2a2924aaebbfbea80780` | ui/text | 新格式 | 7（0） | 1（是） | 分开单行文本盒与多行行距，不把 Compose lineHeight… |
| `lesson-31ab9f59945e5f0259ea` | ui/text | 新格式 | 0（0） | 1（是） | Tab 标签、页面标题与设置行等可见文案沿资源引用链取源端 stri… |
| `lesson-4567f9f77f4280ec1747` | ui/text | 新格式 | 1（0） | 1（是） | 可见文案改为资源引用时值取自源端原文：目标字符串表缺键就新建专属键并… |
| `lesson-57a52be767730880cbba` | ui/text | 新格式 | 5（0） | 1（是） | 移植文本组件时先确认显示的是原始字符串还是加工后的富文本（Compo… |
| `lesson-605038b091e03c26c005` | ui/text | 新格式 | 3（0） | 1（是） | Compose FontWeight 按数值字重写入 ArkUI：S… |
| `lesson-836a5414b52f0e062f1f` | ui/text | 新格式 | 12（0） | 2（是） | maxLines + Ellipsis 两端截断粒度不同：单行补 w… |
| `lesson-b58df29f032cc6a8c9d6` | ui/text | 新格式 | 3（0） | 0 | 字符串语言目录与键集按源端实际存在的 values-<语言>（含依赖… |
| `lesson-c61ac79c7db81729a544` | ui/text | 新格式 | 7（0） | 1（是） | Compose 可折叠正文（onTextLayout 的 didOv… |
| `lesson-cce58a1538fedfda3695` | ui/text | 新格式 | 9（0） | 1（是） | 源端 textAllCaps（含 Material、AppCompa… |
| `lesson-cf670f808b1a42227083` | ui/text | 新格式 | 5（0） | 0 | 带参 $r 的 %s/%1$s 占位只传字符串：数值先 toStri… |
| `lesson-d442eb6e9aab4d77db18` | ui/text | 新格式 | 5（0） | 1（是） | 源端在代码里格式化的含固定措辞文案（SimpleDateFormat… |
| `lesson-ff19b09146b57d0f91a8` | ui/text | 新格式 | 5（0） | 1（是） | 源端文案来自框架（android.R.string.*，或偏好对话框… |
| `lesson-1856958fc6d369f0e2bb` | ui/theme | 新格式 | 9（0） | 2（是） | 主题提供的颜色按各主题与深浅两态取值导出成对 base/dark 键… |
| `lesson-1e972af4bc7e27b23d9c` | ui/theme | 新格式 | 2（0） | 1（是） | 追加主题颜色资源时同一次写深色限定目录的同名键，已存在的资源文件只追… |
| `lesson-2e4279c4b82f06af64fd` | ui/theme | 新格式 | 4（0） | 0 | “页面零硬编码色值”只禁止字面色值，不禁止用 $r 引用语义色 |
| `lesson-47785524c7f132ea7efe` | ui/theme | 新格式 | 24（0） | 1（是） | 把主题、控件默认样式或依赖库隐式提供的外观写成目标显式样式：按“控件… |
| `lesson-4e9507a2a793c5583aa8` | ui/theme | 新格式 | 9（0） | 1（是） | 按源端实际色值与字号在资源里反查同值键：主题语义色、排版样式先解析到… |
| `lesson-5a82d62ff7e087616968` | ui/theme | 新格式 | 24（0） | 5（是） | 委托 Material/AppCompat 库或平台框架（Theme… |
| `lesson-771d1ba1a032b769097a` | ui/theme | 新格式 | 19（0） | 4（是） | 布局引用的 @drawable（progressDrawable、背… |
| `lesson-7b19b801e0f21481d1d6` | ui/theme | 新格式 | 5（0） | 1（是） | 深浅主题与应用内色板状态放在可观察对象里并由入口同步，组件在渲染期从… |
| `lesson-8b7c4ece5e5bf7704a44` | ui/theme | 新格式 | 2（0） | 0 | 同时需要圆角与描边时把 radius 写进 .border() |
| `lesson-b742fb724345e4cfeb50` | ui/theme | 新格式 | 2（0） | 1（是） | 颜色插值或混合按 ARGB 四通道拆分并输出同一格式：#AARRGG… |
| `lesson-bc5b8558ab086168b462` | ui/theme | 新格式 | 16（0） | 1（是） | 引用 style 或抽成共享 @Builder 的控件：先展开共享默… |
| `lesson-f1069f514c0eb98702fb` | ui/theme | 新格式 | 4（0） | 2（是） | 应用内主题切换不只依赖 setColorMode：命令式取色、系统栏… |
| `lesson-42cf412cacabb3c8c281` | ui/web | 新格式 | 5（0） | 2（是） | 源 WebView 未设 WebViewClient 时链接按 An… |

退役经验的知识文件（不渲染）：

| id | 主题 | 规则 | 条目（带成立范围） | 改句（已进正文） | 标题 |
|---|---|---|---:|---:|---|
| `lesson-6e558834938be19c04e2` | arkts/api-signatures | 第三版 | 19（0） | 5（否，经验已退役） | 写 SDK 调用前按本地 .d.ts 核对成员名、所属类型、调用链每… |
| `lesson-25bc0b7518d335a947d6` | process/build | 第三版 | 10（0） | 2（否，经验已退役） | 交付前要编译：项目根没有 hvigorw 时改用 DevEco 或命… |
| `lesson-42df1ac4d4030421da34` | process/input-loading | 第三版 | 0（0） | 0 | 写码前要读全必读 skill、规格、参考文档与源布局/源码：批量读取… |
| `lesson-0c9e222422d81871b464` | process/spec-handoff | 第三版 | 6（0） | 1（否，经验已退役） | 源码或布局引用的资源值（getColor/getDimension(… |

## 两版规则各做了哪些

- **第三版规则（早先那版，4 条）**：条目多（共 35 条）、没有 `scope`，kind 里有「卡里验证」；不是按 `RULES.md` 做的。文件：`0c9e2224`、`25bc0b75`、`42df1ac4`、`6e558834`。
- **第七版规则（1 条）**：按 `RULES.md` 做，每条事实写了成立范围；写完由另一个人逐条独立复核了成立范围（建分支时那批 22 个文件 124 条，复核改了约三成，多数是漏了例外；之后各批见「并入记录」）。文件：`f88b9c82`。

核实时用的版本：鸿蒙 API 23（SDK 6.1.0.105）和 OpenHarmony 中文文档；安卓源码 android-36.1，平台资源 android-30 至 36；依赖库版本写在各文件的 `sdk` 和条目出处里。

## 怎么渲染

```
python knowledge/render.py                 # 渲染全部，写到 knowledge/rendered/（每次重写）
python knowledge/render.py lesson-<id>     # 一条打印到标准输出
python knowledge/render.py --check         # 只核对，不写
```

交给模型的那一段 = 经验正文（`memory/<主题>/lesson-<id>.lesson.md` 去掉 ID 行和「[本主题](index.md)」，截到「## 来源」之前，「来源支持：…」一行保留）；知识文件有条目时，空一行接「已核实的平台事实（核实时用的是 …；安卓 …。…）：」一段，每条「- 〔step〕fact」，有成立范围的再接「〔成立范围：scope〕」；不带出处和写法。和影子提示词生成器里的经验块是同一种写法：本分支建好后拿一套此前用 main 正文加这些知识文件生成的影子提示词核过，其中 27 条经验（32 个经验块，12 条的改句现在已在正文里）和 `render.py` 的输出逐字相同。

新格式的文件（`sdk` 里有 `docs_date` 或 `docs_commit`）知识段照写知识时用的渲染脚本：段头写成「核实时用的是 <harmony>；OpenHarmony 文档 master <docs_date>（提交 <docs_commit 前 8 位>）；安卓 …」，每条只有「- 〔step〕fact」，没有成立范围；同一个文件、同一份正文，和那个脚本的输出逐字节相同。旧格式的渲染不变。

知识文件里的改句：已在正文里的只核对；还没进正文的（新写的知识文件），原句在正文里恰好对上一处时当场套上并报出处数，对不上就报错。

## 怎么检查

```
python knowledge/check.py knowledge/lessons --legacy-ok [--app-name <留作评测的应用名> …]
python knowledge/check.py knowledge/lessons --only <id 前 8 位,…>     # 配知识的人查自己的（新格式，不加 --legacy-ok）
```

查：json 能解析、`lesson` 和文件名一致、经验在 `memory/` 里（store 里已退役的只列出）；条目六栏非空、kind 三选一、最多 6 条；source / fact / scope / code 没有本机路径和「文件:行号」；fact / scope 没有被迁移应用的名字（留作评测的应用名不写在仓库里，用 `--app-name` 传）；改句已在正文里（新句在、原句在新句之外不再出现），还没进正文的要能唯一定位。旧格式文件加 `--legacy-ok` 时，`id` 键、没有 scope、超过 6 条、kind「卡里验证」只列出。

新格式的文件（没有 `lesson` 键、`sdk` 里有 `verified_on` / `docs_commit` / `docs_date`）按写知识时的检查规则查，`--legacy-ok` 对它不起作用：顶层键齐全、`id` 和文件名一致；`sdk` 的核实日期、文档日期写成 YYYY-MM-DD，文档提交号是十六进制，`harmony` 写明 API 几；条目五栏非空，kind 四选一（含「卡里验证」）、origin 二选一、step 是正文的部分名，条数不设上限；卡里验证的事实不写返修怎么改，事实不带返修经过和做法建议的尾巴；文档出处写成文档仓库 master 的链接，网址只认一手来源，fact / after / note 里不放链接；没有本机路径、行号写法和应用名；改句已在正文里的同上，没进正文的按顺序要套得上。默认值缺「应用没有另设」一类限定、提到高于本机 SDK 的 API、新句提到设备或截图的只列出，给人看。出处和本机 SDK、文档的逐条核对不在这里做。

本分支的结果：319 个文件 0 处错误（加 `--legacy-ok`，只列出 55 处 = 旧格式 12 处 + 新格式 39 处（要人看的）+ 4 个退役经验）；第七版的 1 个文件、新格式的 314 个文件不加 `--legacy-ok` 也是 0 处错误。

效果数据见 `shadow/README.md`。
