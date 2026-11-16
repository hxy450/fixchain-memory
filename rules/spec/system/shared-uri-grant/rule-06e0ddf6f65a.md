# 源端用 FileProvider 给剪贴板传 URI 时，规格写明跨应用授权语义和鸿蒙侧可读的写法

审的是：规格
触发（任一种）：
- 读到：源端经 FileProvider 生成 URI 放进剪贴板或分享，接收方凭跨应用授权读取；写错的样子：规格的剪贴板契约只写「图片 URI 写入」，没写 FileProvider 的跨应用授权语义，也没写鸿蒙侧改写成接收方可读的数据（PixelMap）和成功提示
适用范围：规格里写复制图片到剪贴板、分享图片的契约时
做法：
- 契约里写明：源端 URI 靠 FileProvider 跨应用授权才可读；鸿蒙侧不写应用沙箱 file URI，改写 PixelMap（pasteboard.MIMETYPE_PIXELMAP）等接收方可读的数据，成功后补 Toast
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- const MIMETYPE_PIXELMAP = 'pixelMap'：剪贴板写图片用的 MIME 类型（出处：鸿蒙 SDK 的 ets/api/@ohos.pasteboard.d.ts，pasteboard.MIMETYPE_PIXELMAP）
未核实：规格作者如何形成「图片 URI 写入」这条契约没有追溯
来源：1 张卡，1 个应用
- case-149fd657e7134bf86261（jerboa）：做法第 1 步 ← 建议 4
