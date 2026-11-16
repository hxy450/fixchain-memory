# 源端的 URL 解析和链接截取

agent 会看到什么：读到源码用 java.net.URL(url).host、URL(base, path)、try { URL(link) } catch (MalformedURLException)、io.ktor.http.Url，或 substringBefore('#') / substringAfterLast('/') 这类 helper 解析链接；产物里是 url.URL.parseURL、靠 new url.URL 抛错判合法，或正则、lastIndexOf 手写截取

## 通用查法

### 源端用 java.net.URL、ktor Url 解析链接时，先对照两端语义，对不上就按源端语义手写

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

## 规矩

- rule-dad4df84f478｜源端靠 java.net.URL 抛错判绝对性或合法性时，目标先用 scheme 正则判定，不靠 url.URL 抛错｜读到：源码 try { URL(link) } catch (MalformedURLException) 后补 http:// 或改用 URL(base, link) 按 base 拼接；或以是否抛 MalformedURLException 判断链接合法、过滤失败项（…OrThrow）；写错：目标写成 try { new url.URL(trimmed) } catch { … } 来判断「已是绝对 URL / 合法」，无 scheme、相对或非法串原样放行
- rule-4662dc07e191｜java.net.URL(url).host 移植时取不带 userinfo 和端口的主机名，解析失败返回 null｜读到：源码 URL(url).host（java.net.URL），catch MalformedURLException 返回 null；写错：目标用 `^scheme://([^/?#]+)` 一类 RegExp 取 authority：结果带 userinfo 和端口，任意协议都接受
- rule-3c6456d62536｜源码用 URL(base, 绝对路径) 取 scheme 和 authority 时，目标按字符串截取保留显式端口｜读到：源码 URL(remoteUrl, "/api/…/") 取 base 地址（如 Retrofit 的 baseUrl(URL(…, "/path/"))），默认地址带显式端口（:443）；写错：目标写成 parsed.protocol + '//' + parsed.host + '/path/'，catch 才回退默认；默认地址丢了 :443，非法串得到 ///path/
- rule-37432a3d6cf0｜从 URL 取最后路径段或扩展名时，先去掉 #fragment 和 ?query 再取｜读到：源码对链接调用同文件的私有或扩展 helper 取路径段，helper 定义里是 `substringBefore('#')`、`substringBefore('?')`、`substringAfterLast('/')`；读到的片段可能只有调用、没有定义；写错：目标端直接在整串 URL 上 `lastIndexOf('/')` 取段再取扩展名，没先去掉 `?query` 和 `#fragment`（带参数的链接得到 `mp3?x=1` 这样的扩展名）
- rule-dfd85e489d2a｜源端用 io.ktor.http.Url 解析时，不直接换成 @ohos.url URL，先拿源仓库单测逐条核对｜读到：源码 import io.ktor.http.Url、runCatching { Url(url) }，用 segments、encodedPath、parameters["…"]；源仓库 src/test 下有对应单测；写错：目标改用 url.URL.parseURL 配 pathname、searchParams、decodeURIComponent 容错，并以「边缘情况可接受」跳过核对
