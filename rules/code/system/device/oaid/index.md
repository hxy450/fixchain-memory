# OAID 设备标识的采集

agent 会看到什么：读到源端用 MSA 的 MiitHelper、OAIDHelper.getOAID 等在隐私同意后采集 OAID 并写进网络公参，产物里是 identifier.getOAID 的调用、APP_TRACKING_CONSENT 权限申请，或只有「无对等 API」注释、只读偏好键不写入的取值

## 规矩

- rule-8b1629cd05c3｜源端采集 OAID 且规格要求承接时，目标用 identifier.getOAID 真实采集，不写「无对等 API」｜读到：源端用 MSA 的 MiitHelper 或厂商通道采集 OAID，写缓存、上送接口并发布就绪事件；规格验收要求承接，裁剪项里没有 OAID；写错：目标取 OAID 的方法在缓存未命中分支只有注释「HMOS 侧无对等 API」「待平台标识域 API 核验后接通」，没有调 identifier.getOAID()，不上送、不发事件
- rule-675e93b78dbf｜调 getOAID 前在隐私协议同意之后检查并申请 APP_TRACKING_CONSENT，全零串按未授权处理｜读到：目标要调用 identifier.getOAID()；规格接口表写 OAID 拒绝授权时返回全 0；写错：直接调 getOAID()，前面没有 checkAccessToken / requestPermissionsFromUser，或不在隐私协议同意之后；把 00000000-0000-0000-0000-000000000000 当成有效 OAID 上送，或去掉了超时兜底
- rule-a5732a0df4a0｜拦截器读取的公参键在工程里没有写入点时，按源端来源补生产者｜读到：源端隐私同意后的 initSdk 序列里有 OAIDHelper.getOAID 等获取设备标识的步骤，网络公参取的就是这些值；写错：目标的公参 provider / Interceptor 只从偏好键读 oaid 这类字段，工程里没有任何代码写这个键；隐私后初始化链里没有 OAID 步骤
