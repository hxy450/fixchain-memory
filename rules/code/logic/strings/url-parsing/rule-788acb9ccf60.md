# 源端用 java.net.URL、ktor Url 解析链接时，先对照两端语义，对不上就按源端语义手写

审的是：代码
触发（任一种）：
- 读到：源码用 java.net.URL 的 host、URL(base, path)、catch (MalformedURLException)，或 io.ktor.http.Url 的 segments、parameters 取链接的某一部分；写错的样子：目标直接换成 url.URL.parseURL 的 host、pathname、searchParams，或靠 new url.URL 抛错判合法，没对照源端语义
适用范围：把依赖某个 URL 解析类语义的源端函数移植成 ArkTS 时
做法：
- 先读源端解析类在用到的属性上的语义：java.net.URL 看安卓框架源码里 getHost、getPort 和构造器的抛错条件；ktor Url 这类依赖库看源仓库的单测用例
- 再对照 @ohos.url 的 URL.parseURL 声明和 js-apis-url.md 的 URL 属性说明（相对 URL 要给 base、默认端口解析为空串、hostname 不带端口），把源端判例逐条对过
- 对不上的按源端语义写成显式的字符串处理（scheme 正则、按 # 和 ? 截断、截取 scheme://authority），不靠 url.URL 的字段或抛错
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- static parseURL(url: string, base?: string | URL): URL，@throws 10200002 - Invalid url string；相对 URL 必须给 base：目标端声明了抛错条件的解析入口（出处：鸿蒙 SDK 的 ets/api/@ohos.url.d.ts，URL.parseURL）
- 解析时 port 等于当前 protocol 的默认端口（https: 443、http: 80）就解析为空字符串：按 host、port 拼回去会丢掉源端写明的默认端口（出处：js-apis-url.md，URL 的属性说明）
针对本应用要查的：
- 源端解析函数在各类输入上的期望行为：源仓库 src/test 下测试这个函数的单测文件（按被测类名加 Test 找）；没有单测时用规格里的判例；把每个用例的输入和期望输出列成目标端的自测样例，逐条核对所选写法
来源：2 张卡，2 个应用
- case-4b8ebe5007982e666e18（jerboa）：做法第 1 步 ← 建议 1、建议 2；做法第 3 步 ← 诊断
- case-bb79a6275f14f9eb5438（com.nononsenseapps.feeder）：做法第 2 步 ← 建议 4、建议 1；做法第 3 步 ← 建议 2
