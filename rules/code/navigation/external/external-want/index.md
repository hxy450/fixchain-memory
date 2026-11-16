# 拉起浏览器和系统设置的 Want

agent 会看到什么：读到源端 new Intent(Intent.ACTION_VIEW, Uri.parse(url))、Settings.ACTION_APPLICATION_DETAILS_SETTINGS 一类 Intent 交给外部应用打开；产物里 startAbility 的 Want 的 action、entities、bundleName / abilityName

## 规矩

- rule-645830a28e44｜ACTION_VIEW 打开网址时，Want 要带 entity.system.browsable｜读到：`new Intent(Intent.ACTION_VIEW, Uri.parse(url))` 后 `startActivity`，交外部浏览器打开网址；写错：`Want` 只有 `action: 'ohos.want.action.viewData'` 和 `uri`，没有 `entities: ['entity.system.browsable']`；常见于照搬别处已有的外链打开函数
- rule-ad6f936bc91e｜打开系统设置的 Want 写 com.huawei.settings 时，NEXT 上改为 hmos 包名｜读到：源端用 Settings.ACTION_APPLICATION_DETAILS_SETTINGS、Settings.ACTION_MANAGE_APP_ALL_FILES_ACCESS_PERMISSION 等 Intent 跳系统设置；参考文档给出硬编码的设置包名并标「已验证」；写错：Want 里写 bundleName: 'com.huawei.settings'、abilityName: 'com.huawei.settings.MainAbility'，startAbility 失败只在 catch 里 hilog.warn
- rule-af2b2bb9097f｜取自身包名用 BundleInfo.name，不按安卓命名写 bundleName / packageName｜读到：派工或源端要按自身包名拉起应用市场详情（packageName）；写错：代码里写 info.bundleName（info 来自 getBundleInfoForSelf / getBundleInfoForSelfSync），编译报 Property 'bundleName' does not exist on type 'BundleInfo'
- rule-b2115167bd4d｜把媒体 URI 交给其他应用查看或分享时，Want 加 FLAG_AUTH_READ_URI_PERMISSION｜读到：源端 Intent.ACTION_SEND 带 Intent.EXTRA_STREAM（系统迁入 ClipData 并隐式附读授权），或 ACTION_VIEW 打开 content:// 媒体 URI；写错：Want 里有 uri（或分享用的 sendData）却没有 flags
- rule-4c499c3d1d60｜隐式拉起外部应用前先 canOpenLink 预检，无接收者走源端回退或提示，不靠抛错｜读到：源端用 Intent(ACTION_VIEW / ACTION_SENDTO, Uri) 拉起外部应用，先查可用性，没有接收者就回退（如改开网页地图 URL）或提示没有应用；写错：直接 startAbility(...) 或 openLink(...)，把 catch 当没有接收者；或 openLink('mailto:…') 不带 ://，被按后缀推断成别的类型
- rule-fda919b51007｜源端分 CustomTabs 和 ACTION_VIEW 两条通道打开链接时，目标保留两通道并透传私密参数｜读到：源码按开关分 CustomTabsIntent 与 Intent.ACTION_VIEW 两条通道，私密浏览时加 incognito / private_browsing 一类 extras，startActivity 失败时 Toast；写错：目标只发一个 viewData want，注释写这些参数「仅保留签名兼容」，失败只 console.error
- rule-a362cd7d13de｜补齐缺失服务时先读 spec 的 AC 和源码锚点，不按调用点补 void 加静默 catch 的空壳｜读到：检查器报切片自有服务缺失或未实例化（如「does not instantiate」），手里只有调用点名如 X.open(url)；源端打开链接的工具里 startActivity 捕获 ActivityNotFoundException、mailto 走邮件、custom tab 分支；写错：补出的 open(context, url): void 把 startAbility 失败静默 catch，没有空串和 # 守卫、mailto 分支、返回值、失败提示和异常分类，注释却写「与 Android 的 ActivityNotFound 兜底一致」
- rule-93e76b32d5b9｜拉起外部查看器时 Want.type 按这条媒体取精确 MIME，不写 image/* 通配｜读到：源端 new Intent(Intent.ACTION_VIEW)（或 REVIEW）用 MediaStore URI 打开最新照片或视频，不调 setType；写错：startAbility 的 Want 写死 type: 'image/*'；网关只收 URI，媒体查询结果里的 isVideo / photoType 没传进去
- rule-47ec5313df6f｜外部查看入口沿委托链迁每个分支，无 URI 时回落，不在注释里断言源端直接 return｜读到：源端点击处理委托给工具方法，后者 uri 为空时用 MediaStore.Images 的 EXTERNAL_CONTENT_URI 打开图库，另有 RAW 分支；写错：目标网关 `if (!uri) return`，注释写「无 uri 时不操作（源 … return）」，没有 startAbility 之外的回落入口
