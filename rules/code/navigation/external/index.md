# 外部入口与深链

源端有 intent-filter 深链、onNewIntent、PendingIntent、TaskStackBuilder，或交给外部应用的 ACTION_VIEW / ACTION_SEND / Settings Intent，目标端有 EntryAbility 的 onNewWant、want.uri、startAbility 的 Want、WantAgent、systemShare 时

## 触发族

- [拉起浏览器和系统设置的 Want](external-want/index.md)（9 条）：读到源端 new Intent(Intent.ACTION_VIEW, Uri.parse(url))、Settings.ACTION_APPLICATION_DETAILS_SETTINGS 一类 Intent 交给外部应用打开；产物里 startAbility 的 Want 的 action、entities、bundleName / abilityName
- [onNewIntent 与外部深链的再次拉起](new-intent-deeplink/index.md)（4 条）：读过的源码里外部入口用带 FLAG_ACTIVITY_CLEAR_TOP 的 Intent、handleDeepLink 或 onNewIntent 再次拉起页面；交回的 onNewWant 没清 NavPathStack 就切 tab 或 push，或页面改在 onShown 里刷新
- [Intent 发起的外部入口、通知动作和分享](intent-entry-share/index.md)（8 条）：读到 Intent / PendingIntent 发起的动作：快捷方式和通知点进页面的 startActivity、通知按钮 PendingIntent.getBroadcast、isIntentAvailable 判断、ACTION_SEND 分享面板；产物里 EntryAbility 的 want 路由、WantAgent、导航守卫和 systemShare
- [TaskStackBuilder 父栈和路由栈的恢复与再次拉起](task-stack-restore/index.md)（4 条）：源端 TaskStackBuilder.addNextIntentWithParentStack、android:parentActivityName、LAUNCHER 跳板 Activity 的 FLAG_ACTIVITY_CLEAR_TOP，对应目标 NavPathStack 的入栈和整栈恢复、EntryAbility 的 onCreate(launchParam) 与 onNewWant
- [深链的 intent-filter、navDeepLink 和 want.uri 解析](deep-link/index.md)（9 条）：读到 AndroidManifest 里带 android.intent.action.VIEW / BROWSABLE 和 <data android:scheme> 的 intent-filter、navDeepLink 的 uriPattern 或源端深链路由器；产物里 EntryAbility 的 onCreate / onNewWant 读 want.uri、URI 解析函数和导航栈的深链入口
- [ShortcutManager 固定的桌面快捷方式](pin-shortcut/index.md)（1 条）：读到源端 ShortcutManager 的 isRequestPinShortcutSupported、requestPinShortcut、disableShortcuts 和 ShortcutInfo；产物里添加、移除快捷方式的入口是 productViewManager 的申请固定，还是只有日志、引导弹窗和 no-op
- [响应拍照、录像意图时的结果回传](capture-intent-result/index.md)（5 条）：读到源端响应 MediaStore.ACTION_IMAGE_CAPTURE / ACTION_VIDEO_CAPTURE，读 EXTRA_OUTPUT 等意图参数，结束时 setResult(RESULT_OK / RESULT_CANCELED, data) 再 finish()；产物里 terminateSelf / terminateSelfWithResult 的调用次数、结果码和 uri，以及调用方 uri 有没有写入
- [接收别的应用分享来的 ACTION_SEND](receive-share/index.md)（3 条）：读到源端入口 Activity 从 getIntent() 的 ACTION_SEND 读 EXTRA_TEXT、EXTRA_SUBJECT、EXTRA_STREAM 后打开页面，处理完 setResult + finish()；产物里 EntryAbility 或承接 Ability 的 onCreate / onNewWant 怎么取分享内容（systemShare.getSharedData、want.parameters 的键）、怎么传给页面、内容为空时开不开页、结束的是谁
- [指向应用自身的包名（getPackageName、APPLICATION_ID）](own-bundle-name/index.md)（1 条）：读到源端用 getPackageName()、BuildConfig.APPLICATION_ID 或 Intent 的 setPackage / ComponentName 指向应用自身；产物里 Want 的 bundleName 写成 'com.example.…' 字面量，或另起、跨文件复制包名常量
- [外部应用拉起时 Intent extras 里的协议键](external-intent-extras/index.md)（1 条）：读到源 Activity 在 onCreate 里从 getIntent() 读外部协议的 action 和 extras（IMAGE_CAPTURE、VIDEO_CAPTURE、CAMERA_FACING 一类），规格 AC 或映射列了键名、取值域和优先级；产物里 want.parameters 的解析代码多了源码没有的键、漏键，或类型、取值域和短路顺序不符
