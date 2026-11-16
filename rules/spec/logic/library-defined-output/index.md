# 源码交给依赖库算出的结果（RRULE 序列化、相对时间、URL 解析）

agent 会看到什么：读到源码把常量或输入交给依赖库求值：ical4j 的 RRule.toString()、PrettyTime.format()，或靠 java.net.URL、Patterns.WEB_URL 语义的工具函数；规格的 algo-io、映射行或 AC 只登记原始常量、写「自研」「intl 相对时间」或只给标准样例，没写库输出的字面格式和边界样例

## 通用查法

### 源码把值交给依赖库算出要存、要显示或要判定的结果时，规格照库的真实输出写契约

审的是：规格
触发（任一种）：
- 读到：源码把常量或输入交给依赖库求值：ical4j 的 RRule.toString()、PrettyTime.format()，或 java.net.URL、Patterns.WEB_URL、String.replaceFirst 这类库语义的工具函数；写错的样子：规格的映射行、algo-io 或 AC 只写替代方向（「自研」「intl 相对时间」）、只登记原始常量或只给标准样例，没有库输出的字面格式和边界样例
适用范围：规格提取阶段，给结果由依赖库决定的算法和工具函数写映射行、algo-io 和验收判据时
做法：
- 按源工程的依赖坐标和版本取到这个库，用源码里的实参跑出真实输出；库语义的工具函数再读源仓库里对应的单测，拿到输入和期望输出
- 把输出逐字写成契约字段（时区形态、分隔符、结尾、文案模板），AC 写这些字面串和边界样例；取不到真值或决定不移植时登记 PD-* 交用户改判
针对本应用要查的：
- 库的版本和代表输入下的真实输出：源工程模块构建脚本里的依赖坐标和版本；本机 Gradle 缓存 modules-2/files-2.1/<group>/<artifact>/<version>/ 下的 jar；用 JDK 小程序以源码里的实参调用库函数，把输出逐字写进契约。例：卡里用 jar 对拍，ical4j 的 RRule.toString() 输出的 UNTIL 是设备时区浮动时间 yyyyMMddTHHmmss、末尾带 CRLF
- 库语义工具函数的单测用例：源仓库 src/test 下按被测类名加 Test 找到的单测文件；把其中的输入和期望输出抄进 AC，作为 unit 判据
来源：2 张卡，2 个应用
- case-4b8ebe5007982e666e18（jerboa）：做法第 1 步 ← 建议 5
- case-d23537ecc4c87801075a（omni-notes-hmos）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1、建议 2

## 规矩

- rule-87c4ef542964｜产出持久化或展示字符串的算法库，映射行写库输出的字面契约或登记 PD-*｜读到：源工程依赖里有 RRULE 解析与序列化、重复文案、相对时间、日期格式这类算法库（如 org.mnode.ical4j:ical4j、org.ocpsoft.prettytime:prettytime），源码用 RRule.toString()、PrettyTime.format() 产出要存库或显示的串；写错：跨栈映射行只写「自研 / tiny RRULE 解析（RFC5545 子集）」「@ohos.i18n intl 相对时间或自研」并标 Auto / Semi-Auto，没写库输出的字面格式，标了 Manual 也没转成 PD-*
- rule-6b194f8ba55f｜功能 spec 的 algo-io 登记常量时，一并登记它经库序列化后的字符串形态｜读到：源码把常量交给库序列化，如 new RRule(new Recur(freq, new DateTime(<毫秒常量>))).toString()；写错：algo-io 只登记毫秒常量，验收条目写「输出含 UNTIL=<毫秒数>」，没写序列化后的串是 UTC Z 还是设备时区浮动时间
- rule-8cb7c6d21805｜依赖库语义的工具函数，规格 AC 写入边界样例并引用源仓库单测｜读到：源码工具函数依赖库语义（String.replaceFirst、java.net.URL.host、Patterns.WEB_URL.matcher().matches()、io.ktor.http.Url），源仓库 src/test 下有对应单测；写错：AC 只有标准绝对 URL 的样例，没有无 scheme、带端口或 userinfo、句中含 URL、畸形转义这些边界样例，也没引用源仓库单测
