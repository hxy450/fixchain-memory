# 源端用 io.ktor.http.Url 解析时，不直接换成 @ohos.url URL，先拿源仓库单测逐条核对

审的是：代码
触发（任一种）：
- 读到：源码 import io.ktor.http.Url、runCatching { Url(url) }，用 segments、encodedPath、parameters["…"]；源仓库 src/test 下有对应单测；写错的样子：目标改用 url.URL.parseURL 配 pathname、searchParams、decodeURIComponent 容错，并以「边缘情况可接受」跳过核对
适用范围：把依赖 ktor Url 解析语义的函数移植成 ArkTS 时
做法：
- 先读源仓库对应单测，把用例当行为样例；ktor Url 接受无 scheme 的相对路径（如 "test.jpg"），转义畸形时解析失败
- @ohos.url 的 URL 是 WHATWG 语义，相对路径要给 base、转义处理也不同；用单测逐条核对，对不上就写 ktor 兼容的解析函数
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- static parseURL(url: string, base?: string | URL): URL；相对 URL 必须给 base，非法时抛 10200002 Invalid url string：不给 base 时相对路径解析失败，和 ktor 不同（出处：鸿蒙 SDK 的 ets/api/@ohos.url.d.ts，URL.parseURL）
- 修好后自写了 ktor 兼容的解析函数：无 scheme 的文件名不再判为链接，畸形转义按解析失败处理（出处：卡里修好并验证过）
针对本应用要查的：
- 源端解析函数的期望行为：源仓库 src/test 下测试这个函数的单测文件（按被测类名加 Test 找）；把每个用例的输入和期望输出列成目标端的自测样例
未核实：ktor Url 的宽松解析和转义报错行为出自卡，依赖库源码本机没有
来源：1 张卡，1 个应用
- case-4b8ebe5007982e666e18（jerboa）：做法第 1 步 ← 建议 2、建议 1；做法第 2 步 ← 建议 2、诊断；取值 2 ← 诊断
