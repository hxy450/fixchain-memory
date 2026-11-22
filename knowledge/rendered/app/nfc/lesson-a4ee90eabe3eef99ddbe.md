# Android Activity 级 NFC 前台派发迁到 HarmonyOS 时按 UIAbility 前后台注册，再用可见顶页登记表仿真页面级开关与默认新标签处理

## 何时使用

NFC 引擎与基类行为迁移阶段，把基类 onResume/onPause 的前台派发开关、onNewIntent 统一处理与“当前标签”判定分配给服务、页面与全局状态时

## 适用情境

Android 多数页面继承基类：onResume 设置待处理组件并 enableForegroundDispatch，onPause 关闭，onNewIntent 统一处理新标签，卡或设备不支持时跳转信息页；全局保存任意技术的 Tag。目标 tag.registerForegroundDispatch 按 UIAbility 注册，页面用 Navigation/NavDestination 组织，服务切片不能改页面。源端不继承该基类、自己也不开前台派发的页面不登记：它在最上层时源端前台派发是关的，目标的登记表此时也不把标签投给压在下面的已登记页。

## 原因

派发开关在 Android 随 Activity 可见性启停，在目标随 UIAbility 生效：让某一页的隐藏注销整个能力级派发，其他页就收不到卡；把订阅挂在 aboutToAppear/aboutToDisappear，被覆盖的页面仍在收卡；把全局 Tag 收窄为某一技术类型，非该技术的卡被判为不在场。来源中服务切片只写了注册与注销并把页面接线推给消费切片，消费切片又推回，最终只有主菜单注册、且在其隐藏时注销全应用派发；三个页面把订阅挂在组件生命周期；全局 Tag 被定义为单一技术类型。

## 做法

1. 在 EntryAbility 的 onForeground/onBackground 注册、注销能力级前台派发；服务维护可见页登记表（pageShown/pageHidden），把标签投递给最上层可见页，仿真 onPause → onNewIntent → onResume；各页在 onShown/onHidden 登记，不在 aboutToAppear/aboutToDisappear 订阅。
2. 不让单个页面的隐藏注销应用级派发，也不把“设置待处理页面”合并进通用注册函数；默认的新标签处理（不支持时跳信息页）放在服务提供的入口里。
3. 全局“当前标签”保存任意技术的标签信息，在场判定按它判断，不收窄为单一技术类型。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔适用情境 / 原因 / 做法第 1 步〕tag.registerForegroundDispatch 按 ElementName（必须含 bundleName 和 abilityName）注册，开关粒度是 UIAbility 而不是页面；应用必须在前台才能调用，须与 tag.unregisterForegroundDispatch（同一个 ElementName）成对使用，在退出前台或销毁前取消注册；读卡器模式 tag.on('readerMode') 同样按 ElementName 注册
- 〔做法第 1 步〕UIAbility.onForeground 在应用从后台转到前台时触发，onBackground 在应用从前台转到后台时触发，粒度是整个 UIAbility
- 〔原因 / 做法第 1 步〕NavDestination 的 onShown 在页面布局显示之后执行；onHidden 在页面隐藏后执行，触发场景包括有新页面 push 到它上面、栈顶页面被 pop、应用切到后台；而 aboutToAppear 在组件创建后、build 前执行，aboutToDisappear 在组件析构前执行，被上层页面覆盖的页面不会销毁，也就不会走 aboutToDisappear
- 〔原因〕设备上各页把 NFC 标签订阅放在 aboutToAppear、注销放在 aboutToDisappear 时，被新页面覆盖的页面仍然收到标签
- 〔适用情境 / 原因〕安卓 NfcAdapter.enableForegroundDispatch 只能在主线程、Activity 处于前台（resumed）时调用，Activity 必须在 onPause 返回前调用 disableForegroundDispatch，开关粒度是单个 Activity 的前后台
