# Coil 全局 ImageLoader 的图片管线

agent 会看到什么：读到源码用 ImageLoaderFactory.newImageLoader 或 Coil.setImageLoader 建全局 ImageLoader.Builder（placeholder、error、crossfade，components 里只加了部分解码器、另有带 GIF 解码器的 loader 由设置位切换）；规格的图片管线 AC 只写 crossfade，或写「GIF 按帧动画播放，与 Android 一致」

## 规矩

- rule-860256c4a15a｜图片经 Coil 全局 ImageLoader 加载时，规格的图片管线写明默认占位、错误图、过渡和动图行为｜读到：源码里 ImageLoaderFactory.newImageLoader 或 Coil.setImageLoader 建的默认 ImageLoader.Builder 设了 placeholder(...)、error(...)、crossfade(...)，components 里只 add 了部分解码器（没有 GifDecoder / ImageDecoderDecoder），另有带 GIF 解码器的 ImageLoader 由设置位切换；写错：规格的图片管线 AC 只写了 crossfade，没写默认占位图和错误图；或者写成「GIF 按帧动画播放，与 Android 一致」，没写默认 loader 只出首帧、也没写切换 loader 的设置位
