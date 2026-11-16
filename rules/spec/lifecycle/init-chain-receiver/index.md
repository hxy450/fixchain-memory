# Application 初始化链里注册的 BroadcastReceiver

agent 会看到什么：读到 Application 初始化链里 registerReceiver 注册 BroadcastReceiver（如 CONNECTIVITY_ACTION），或上游契约点名某接收器触发业务；feature 规格的锚点、数据流和 AC 里没有这个触发入口

## 规矩

- rule-16ecba3edc00｜Application 初始化链注册的广播接收器调业务时，规格要把它作锚点并写明触发条件和目标 API｜读到：源端 Application 初始化链里调用 register*Receiver 注册 BroadcastReceiver（如 CONNECTIVITY_ACTION），或上游契约文档点名某个接收器会触发业务检测、上报；写错：feature 规格的 android_source_anchors 没有这个接收器，数据流、服务层承接方法和 AC 里都没有这个触发入口，也没有迁移或裁剪决定
