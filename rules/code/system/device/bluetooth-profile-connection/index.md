# 蓝牙 A2DP、HFP 的连接状态

agent 会看到什么：读到源端走 BluetoothDevice 的 ACTION_ACL_CONNECTED / ACTION_ACL_DISCONNECTED 设备级广播；交回的 a2dp 或 hfp 任一 profile 的 connectionStateChange 收到 STATE_DISCONNECTED 就判设备断开

## 规矩

- rule-2b8913679630｜A2DP/HFP 分协议连接回调按设备聚合，所有协议都断开才算断开｜读到：源端连接/断开走 BluetoothDevice 的 ACL 设备级广播（ACTION_ACL_CONNECTED / ACTION_ACL_DISCONNECTED）；写错：a2dp 或 hfp 任一 profile 的 on('connectionStateChange') 收到 STATE_DISCONNECTED 就上报设备断开；待断开设备收到首个协议的断开即判定断开成功
