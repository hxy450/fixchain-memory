# NFC 前台派发（enableForegroundDispatch）的开关时机

agent 会看到什么：读过的源码里基类 Activity 在 onResume / onPause 里 enableForegroundDispatch / disableForegroundDispatch、onNewIntent 收标签，页面继承它；交回的 tag.registerForegroundDispatch、标签订阅挂在了页面的 aboutToAppear / onHidden 上，或回调里多了开关闸门

## 规矩

- rule-d593827103bf｜源随 onResume/onPause 开关 NFC 前台派发时，目标改在 UIAbility 前后台开关｜读到：源端基类 Activity 的 onResume 里 NfcAdapter.enableForegroundDispatch、onPause 里 disableForegroundDispatch，onNewIntent 统一处理新标签，多数页面继承它；写错：目标在某个页面的 onHidden / aboutToDisappear 里调 tag.unregisterForegroundDispatch，注销整个应用的派发；或注册函数里顺带设置当前待处理页；收到标签广播给所有监听者
- rule-17e8b04680e4｜源页面继承开关前台派发的基类时，目标在 NavDestination 的 onShown/onHidden 里登记和注销｜读到：页面类 extends 一个在 onResume 开、onPause 关 NFC 前台派发的基类 Activity；或服务的订阅接口注释写明页面 onShow 期注册、onHide 期注销；写错：页面把标签订阅写在 aboutToAppear、注销写在 aboutToDisappear，被别的页面覆盖后仍收卡
- rule-8501754655b7｜源端前台派发无条件开启时，不在前台贴卡回调里按自启动开关加闸门｜读到：基类 onResume 无条件 enableForegroundDispatch，偏好开关只用于 setComponentEnabledSetting 启停 alias；写错：前台 tag 回调（tag.on('readerMode', …) / registerForegroundDispatch 的 callback）开头按偏好开关 return，开关关闭时前台贴卡不响应
