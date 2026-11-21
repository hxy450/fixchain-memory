# Android Activity 级 NFC 前台派发迁到 HarmonyOS 时按 UIAbility 前后台注册，再用可见顶页登记表仿真页面级开关与默认新标签处理

## 何时使用

NFC 引擎与基类行为迁移阶段，把基类 onResume/onPause 的前台派发开关、onNewIntent 统一处理与“当前标签”判定分配给服务、页面与全局状态时

## 适用情境

Android 多数页面继承基类：onResume 设置待处理组件并 enableForegroundDispatch，onPause 关闭，onNewIntent 统一处理新标签，卡或设备不支持时跳转信息页；全局保存任意技术的 Tag。目标 tag.registerForegroundDispatch 按 UIAbility 注册，页面用 Navigation/NavDestination 组织，服务切片不能改页面。

## 原因

派发开关在 Android 随 Activity 可见性启停，在目标随 UIAbility 生效：让某一页的隐藏注销整个能力级派发，其他页就收不到卡；把订阅挂在 aboutToAppear/aboutToDisappear，被覆盖的页面仍在收卡；把全局 Tag 收窄为某一技术类型，非该技术的卡被判为不在场。来源中服务切片只写了注册与注销并把页面接线推给消费切片，消费切片又推回，最终只有主菜单注册、且在其隐藏时注销全应用派发；三个页面把订阅挂在组件生命周期；全局 Tag 被定义为单一技术类型。

## 做法

1. 在 EntryAbility 的 onForeground/onBackground 注册、注销能力级前台派发；服务维护可见页登记表（pageShown/pageHidden），把标签投递给最上层可见页，仿真 onPause → onNewIntent → onResume；各页在 onShown/onHidden 登记，不在 aboutToAppear/aboutToDisappear 订阅。
2. 不让单个页面的隐藏注销应用级派发，也不把“设置待处理页面”合并进通用注册函数；默认的新标签处理（不支持时跳信息页）放在服务提供的入口里。
3. 全局“当前标签”保存任意技术的标签信息，在场判定按它判断，不收窄为单一技术类型。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；安卓 Android SDK 源码 android-36.1。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 1 步〕鸿蒙 tag.registerForegroundDispatch 按 elementName（至少含 bundleName、abilityName）注册，即按 UIAbility 而不是按页面生效；应用必须在前台才能调用，要与 unregisterForegroundDispatch 成对使用，在退出前台或销毁前取消注册；官方指南的示例在 UIAbility 的 onForeground 注册、onBackground 取消前台读卡。〔成立范围：对 @ohos.nfc.tag 的前台派发（需 ohos.permission.NFC_TAG，SDK 权限定义里为 system_grant、normal）；同一 UIAbility 下的所有页面共用这一个注册；最常见的不成立情形：某一页在自己隐藏时调用 unregister，同一 UIAbility 的其他页也一起收不到卡。〕
- 〔做法第 1 步〕NavDestination 的 onHidden 在被新页覆盖、出栈和应用切后台时都会触发，onShown 在显示、上层页出栈露出和应用回前台时触发；aboutToAppear / aboutToDisappear 只在组件创建 / 销毁时调用，页面被覆盖时不会走 aboutToDisappear。〔成立范围：对 NavDestination 页面；Navigation 首页（NavBar）不在栈中、没有 onShown / onHidden；被 NavDestinationMode.DIALOG 页覆盖或该页出栈时，下层页不触发 onHidden / onShown（只触发 onInactive / onActive，API 17 起）；最常见的不成立情形：把收卡订阅挂在 aboutToAppear / aboutToDisappear 上，被覆盖的页面仍在订阅中。〕
- 〔做法第 1 步〕安卓 Activity 在 resumed 状态下不会收到新 Intent：若正处于 resumed，系统先 onPause，再 onNewIntent，之后 onResume；此后 getIntent() 仍返回原来的 Intent，除非调用 setIntent()。〔成立范围：对 singleTop 启动模式或以 FLAG_ACTIVITY_SINGLE_TOP 重新拉起时复用的 Activity 实例；pause → onNewIntent → resume 的时序依据是 javadoc（暂停由系统服务调度，SDK 客户端代码里看不到）；最常见的不成立情形：Activity 不在 resumed 状态时新 Intent 直接投递，onResume 要等它重新变为活动时才调用。〕
- 〔做法第 3 步〕安卓 enableForegroundDispatch 的 filters 与 techLists 都传 null 时是通配，前台 Activity 经 ACTION_TAG_DISCOVERED 收到所有标签（techLists 第二层取「与」、第一层取「或」）；鸿蒙 registerForegroundDispatch 的 discTech 不能为空、至少指定一种，用来设置 NFC 读卡轮询的标签技术类型，文档写明取值为 NFC_A、NFC_B、NFC_F、NFC_V 中的一种或多种。〔成立范围：对两端前台派发的技术过滤参数；鸿蒙 SDK d.ts 的参数注释写的是 NFC_A 到 MIFARE_ULTRALIGHT，比文档宽；最常见的不成立情形：只传某一种轮询技术时，其他轮询技术的卡不会被发现，等于把安卓的通配收窄。〕
- 〔原因〕安卓 NfcAdapter.enableForegroundDispatch 的 javadoc 要求按 Activity 开启：只在主线程、且该 Activity 处于前台（resumed）时调用，并在该 Activity 的 onPause 完成前调用 disableForegroundDispatch；javadoc 标了 @throws IllegalStateException（Activity 不在前台时），但 android-36.1 的客户端实现只检查 NFC 特性和空参数，不检查 resumed。〔成立范围：对 android.nfc.NfcAdapter 的前台派发；时序要求的依据是 javadoc；最常见的不成立情形：在 android-36.1 上于 onCreate 或 onStart（尚未 resumed）里调用不会因未 resumed 抛异常，更早版本的实现本机核不到。〕
