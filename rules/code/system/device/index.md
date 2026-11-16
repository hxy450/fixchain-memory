# 设备与连接

源端有 NfcAdapter、MifareClassic、BluetoothAdapter、ConnectivityManager、Vibrator、OAID，目标端有 nfc、bluetooth、connection、vibrator、identifier 这类系统接口时

## 触发族

- [NFC 前台派发（enableForegroundDispatch）的开关时机](nfc-foreground-dispatch/index.md)（3 条）：读过的源码里基类 Activity 在 onResume / onPause 里 enableForegroundDispatch / disableForegroundDispatch、onNewIntent 收标签，页面继承它；交回的 tag.registerForegroundDispatch、标签订阅挂在了页面的 aboutToAppear / onHidden 上，或回调里多了开关闸门
- [NfcAdapter 的可用性判断和贴卡入口](nfc-adapter/index.md)（3 条）：读到源端 NfcAdapter.getDefaultAdapter 判空、isEnabled() 判开关、清单 intent-filter 带 android.nfc.action.TECH_DISCOVERED；交回的只有一个 isAvailable 布尔门、降级标志在每种缺失下都置位，或 EntryAbility 不读 want 里的 TagInfo
- [ConnectivityManager 的网络类型和计费判断](connectivity-network-state/index.md)（2 条）：读到源端注册 CONNECTIVITY_ACTION 接收器、getActiveNetworkInfo 按 TYPE_WIFI / TYPE_MOBILE / TYPE_ETHERNET 分支，或 isActiveNetworkMetered；交回的没有 createNetConnection 监听，或计费只看 NET_CAPABILITY_NOT_METERED、不按 bearerTypes 区分
- [蓝牙 A2DP、HFP 的连接状态](bluetooth-profile-connection/index.md)（1 条）：读到源端走 BluetoothDevice 的 ACTION_ACL_CONNECTED / ACTION_ACL_DISCONNECTED 设备级广播；交回的 a2dp 或 hfp 任一 profile 的 connectionStateChange 收到 STATE_DISCONNECTED 就判设备断开
- [蓝牙开关、状态和扫描](bluetooth-state-scan/index.md)（8 条）：读到源端 BluetoothAdapter（isEnabled、enable / disable、ACTION_STATE_CHANGED、startDiscovery、BluetoothDevice.getName）；产物里 @ohos.bluetooth.access / ble / connection 的开关、stateChange 回调、扫描调用和失败处理
- [OAID 设备标识的采集](oaid/index.md)（3 条）：读到源端用 MSA 的 MiitHelper、OAIDHelper.getOAID 等在隐私同意后采集 OAID 并写进网络公参，产物里是 identifier.getOAID 的调用、APP_TRACKING_CONSENT 权限申请，或只有「无对等 API」注释、只读偏好键不写入的取值
- [Vibrator 振动和提示音](vibrator/index.md)（2 条）：读过的源码里调 Vibrator 的 cancel / vibrate、用 MediaPlayer 播提示音或 performHapticFeedback；交回的代码里 vibrator.startVibration / stopVibration 有没有写、先后是否串行
- [MIFARE Classic 标签接口](mifare-classic/index.md)（3 条）：读过的源码里用 android.nfc.Tag、MifareClassic 的 authenticateSectorWithKeyA/B（返回 boolean）；交回的代码里当前标签存成 TagInfo 还是 MifareClassicTag、authenticateSector 的 reject 和错误码怎么分流
- [系统省流量开关（Data Saver）和计费网络判定](data-saver-switch/index.md)（1 条）：读到源端经 ConnectivityManager 按系统 Data Saver 开关（RESTRICT_BACKGROUND_STATUS_ENABLED）判定的档位；产物里改成按 NET_CAPABILITY_NOT_METERED、getNetCapabilities 判计费网络
