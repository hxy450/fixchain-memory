# 源端靠 java.net.URL 抛错判绝对性或合法性时，目标先用 scheme 正则判定，不靠 url.URL 抛错

审的是：代码
触发（任一种）：
- 读到：源码 try { URL(link) } catch (MalformedURLException) 后补 http:// 或改用 URL(base, link) 按 base 拼接；或以是否抛 MalformedURLException 判断链接合法、过滤失败项（…OrThrow）；写错的样子：目标写成 try { new url.URL(trimmed) } catch { … } 来判断「已是绝对 URL / 合法」，无 scheme、相对或非法串原样放行
适用范围：把依赖 java.net.URL 抛错的分支（补 scheme、相对链接按 base 拼接、合法性校验）改写成 ArkTS 时
做法：
- 先用 scheme 正则判断是否带 scheme：/^[a-zA-Z][a-zA-Z0-9+.-]*:/；带 scheme 再解析校验，无 scheme 才补 http://，非绝对才按 base 解析，空 link 返回 base
- 源端 OrThrow 语义的调用点（如候选链接列表）对失败项过滤掉，不原样保留；合法性校验要求带 scheme 且可解析
- 写分支前把规格判例（无 scheme 补 http://、/path 按 base 拼接、非法串跳过或回退）逐条对照所选目标 API 的声明抛错条件
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- constructor(url: string, base?: string | URL)：@deprecated since 9，@useinstead ohos.url.URL.parseURL：带参构造已废弃，声明里不写抛错；不能假定它对无 scheme、相对、非法串抛错（出处：鸿蒙 SDK 的 ets/api/@ohos.url.d.ts，URL.constructor）
- static parseURL(url: string, base?: string | URL): URL，@throws 10200002 - Invalid url string：声明了非法串抛错的是 parseURL（出处：鸿蒙 SDK 的 ets/api/@ohos.url.d.ts，URL.parseURL）
- 无 scheme 时 throw new MalformedURLException("no protocol: " + original)：源端「先 URL(link)、抛错再补 http:// 或按 base 拼接」依赖的就是这个抛错（出处：java.net.URL#URL(URL, String, URLStreamHandler)）
- 按 scheme 判绝对性、无 scheme 才补 http://、相对按 base、空 link 回 base、OrThrow 调用点过滤失败项：修好后判例全过的写法（出处：卡里修好并验证过）
未核实：ArkTS 构造器对 'not a url' 等串得到的各字段值卡里没有直接打印；卡里环境同时记了 target_sdk 23 和 26.0.0，本机按 API 23 核对声明
来源：1 张卡，1 个应用
- case-bb79a6275f14f9eb5438（com.nononsenseapps.feeder）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2、诊断；做法第 3 步 ← 建议 4、建议 1；取值 4 ← 诊断
