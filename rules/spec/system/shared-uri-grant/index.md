# 交给别的应用读的 content URI（FileProvider、ACTION_SEND）

agent 会看到什么：读到源端经 FileProvider 生成 URI 放进剪贴板或分享，或 Intent.ACTION_SEND 带 EXTRA_STREAM、ACTION_VIEW 打开媒体 URI，没写显式授权标志；规格的剪贴板契约或映射行只写「图片 URI 写入」「startAbility sendData + EXTRA_STREAM uri」，没写接收方凭什么读

## 规矩

- rule-d5bdef94322c｜ACTION_SEND / ACTION_VIEW 的映射行写明源端隐式授予的 URI 读权限｜读到：源端 Intent.ACTION_SEND 带 EXTRA_STREAM，或 ACTION_VIEW 打开媒体 URI，没写显式授权标志；写错：映射行只写「startAbility sendData + image/jpeg + EXTRA_STREAM uri」，没写 URI 读授权
- rule-06e0ddf6f65a｜源端用 FileProvider 给剪贴板传 URI 时，规格写明跨应用授权语义和鸿蒙侧可读的写法｜读到：源端经 FileProvider 生成 URI 放进剪贴板或分享，接收方凭跨应用授权读取；写错：规格的剪贴板契约只写「图片 URI 写入」，没写 FileProvider 的跨应用授权语义，也没写鸿蒙侧改写成接收方可读的数据（PixelMap）和成功提示
