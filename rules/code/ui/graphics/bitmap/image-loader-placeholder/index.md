# 图片加载库的占位图、错误图和淡入

agent 会看到什么：读到 Coil 的 ImageLoader.Builder / ImageRequest.Builder、AsyncImage 上的 .placeholder(...)、.error(...)、.crossfade(true)；产物里 Image 的 .alt(...)、加载中的占位和 .contentTransition(...)

## 规矩

- rule-ed75a3c03d5f｜Coil 有占位、错误图和 crossfade 时，Image 写 alt 加 contentTransition｜读到：默认 ImageLoader.Builder 或 ImageRequest.Builder 上有 .placeholder(...)、.error(...)、.crossfade(true)；写错：目标 Image 只写 .alt(错误图)，加载中没有占位；或把 crossfade 说成 Image 的默认过渡，没写 .contentTransition(...)
