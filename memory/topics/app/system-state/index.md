# app/system-state

系统能力的异步状态真值：终态回读、分协议聚合、回调会话归属、同步抛错收敛、读后增量写回与返回值判定

[上一级](../index.md)

## 本级经验

- [三方授权回调先比对 state，不匹配即忽略](lesson-95314752073ab4760059.lesson.md) · 阶段：execute · 信号：requestId, authCode, errCode, SendAuth.Resp
- [分协议连接回调按设备聚合，全部断开才判断开](lesson-ecc67592eba3402c0a1f.lesson.md) · 阶段：execute · 信号：connectionStateChange, A2DP, HFP, ACL
- [声明 void 的同步接口查 @throws 并在服务层捕获](lesson-7ed00c55221c0f935d95.lesson.md) · 阶段：execute · 信号：startBLEScan, stopBLEScan, @ohos.bluetooth.ble, BusinessError
- [接 getOAID 需声明跟踪同意权限，全零串视为未授权](lesson-2b00c4ffaeb442d87e5e.lesson.md) · 阶段：execute · 信号：identifier.getOAID, ohos.permission.APP_TRACKING_CONSENT, requestPermissionsFromUser, checkAccessToken
- [蓝牙开关以 getState 回读终态为准，过渡态不写关闭](lesson-29922f57cc365ff3d638.lesson.md) · 阶段：execute · 信号：access.getState, access.on('stateChange'), STATE_ON, STATE_OFF
- [读基线写增量的亮度手势分映射读写两侧，就绪时预读](lesson-33791daf74fc4298779e.lesson.md) · 阶段：execute · 信号：setWindowBrightness, getWindowProperties().brightness, settings.display.SCREEN_BRIGHTNESS_STATUS, ACTION_DOWN
