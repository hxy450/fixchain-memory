# 拍照 profile 的格式和取字节通路（photoProfiles、CameraFormat）

agent 会看到什么：读到 getSupportedOutputCapability 返回的 photoProfiles、camera.CameraFormat 的 JPEG / RGBA_8888 / DNG 等格式，和 photoAvailable 里 getComponent(image.ComponentType.JPEG) 取字节；产物里选 profile 和能力枚举只认 CAMERA_FORMAT_JPEG、没有 JPEG 就 throw、按 DNG 判 RAW，或非 JPEG profile 没有取数据通路

## 规矩

- rule-6d65a86bf156｜选拍照 profile 时不把 JPEG 当打开相机的硬门槛，JPEG 优先、RGBA_8888 兜底｜读到：getSupportedOutputCapability 返回的 capability.photoProfiles；拍照字节通路按 getComponent(image.ComponentType.JPEG) 取数据；写错：photoProfiles.filter(...) 只留 CAMERA_FORMAT_JPEG，没有 JPEG 时在打开相机、能力探测会话或建会话时 throw（如 'no JPEG photo profile'）
- rule-74fd47c28782｜拍照能力枚举只排除处理不了的格式并按尺寸去重，不只认 JPEG，DNG 不算 RAW｜读到：camera.CameraFormat 枚举里有 RGBA_8888、YUV、JPEG 等多种格式，photoProfiles 里各格式的 size；写错：能力枚举（拍照尺寸列表、拍照录像能否同时进行）只认 CAMERA_FORMAT_JPEG，没有 JPEG 就 throw（如 'no JPEG picture sizes'）；或因有 DNG 格式 profile 就把 RAW 支持置为 true
- rule-d06795dfe162｜拍照字节只按 JPEG 组件取时，为非 JPEG profile 接上 photoAssetAvailable 通路｜读到：拍照回调 on('photoAvailable') 里用 photo.main.getComponent(image.ComponentType.JPEG) 取字节；写错：选出的拍照 profile 可能是 CAMERA_FORMAT_RGBA_8888，代码却只有 getComponent(ComponentType.JPEG) 这一条取数据通路，没有非 JPEG 的处理
