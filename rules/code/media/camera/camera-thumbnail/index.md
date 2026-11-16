# 拍照和停录后的缩略图

agent 会看到什么：读到源端 updateThumbnail(thumbnail, isVideo, wantAnimation) 同时更新画廊按钮和预览覆盖层、停录后 MediaMetadataRetriever.getFrameAtTime 取帧再 createScaledBitmap；产物里只写共享状态的画廊字段、void 掉参数、用 PixelMapParams 的固定宽高取帧

## 规矩

- rule-8dd10c0ba48b｜源端 updateThumbnail 同时更新画廊和覆盖层时，目标两路都送达，不 void 丢参数后标为已解除｜读到：源端 updateThumbnail(thumbnail, isVideo, wantAnimation) 同时更新画廊按钮和预览覆盖层的缩略图动画，规格或占位登记要求接这条 seam；写错：回调只把位图赋给共享状态的画廊字段，写 void isVideo / void wantAnimation 丢掉参数，占位登记按已解除处理；或覆盖层门面里没有 updateThumbnail
- rule-53eb39fcae7a｜停录视频缩略图取末帧后按实测画廊按钮宽等比缩放，不借用媒体库缩略图的固定尺寸｜写错：停录缩略图用 PixelMapParams { width: 512, height: 384 } 这类媒体库缩略图常量取帧，并直接写共享状态里的画廊位图，绕过画廊服务和覆盖层
