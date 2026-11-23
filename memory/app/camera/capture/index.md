# app/camera/capture

拍照与录像产出链：拍照编排与图元的桥接回调和多帧/连拍、photoAvailable 字节的复制与释放、相机系统资产保存与媒体库写权限、录像时长与文件大小限额、目标确无能力的格式与选项的失败路径

[上一级](../index.md)

## 本级经验

- [录制器原生时长/文件大小上限改由应用层定时器或轮询承接时，按不含暂停的已录时长计时，并照源端 onInfo 各分支停止或续录](lesson-1ba734fe6ef196518f9c.lesson.md)
  - 时机：规格提取与录像功能实现阶段，用应用层定时器、文件大小轮询替代 MediaRecorder.setMaxDuration/setMaxFileSize 及其 onInfo 回调时
  - 情境：源端由录制器自行计时计量并回调 onInfo（MAX_DURATION_REACHED、MAX_FILESIZE_APPROACHING/REACHED、NEXT_OUTPUT_FILE_STARTED），pause/resume 只累计已录时长，按偏好决定到达上限后续录还是停止；目标 AVRecorder 启停为异步 Promise，上限改由 setTimeout 或 statSize 轮询合成事件。
  - 例外：源端把时长或文件大小上限设为 0 或负数（即关闭上限，常见于偏好里的“不限”）时，目标对应地不安排定时器、不做大小轮询，不要换成某个默认上限。
- [拍照编排与相机拍照图元之间的桥接要回传完成/失败并按模式交付整组多帧：不定义成无参即发即弃的单帧调用](lesson-df70c7f19f8652dbf36c.lesson.md)
  - 时机：拍照编排实现与跨切片接线阶段（源端拍照调用带完成与错误回调，并有多帧或连拍模式），设计编排器与相机拍照图元之间的桥接契约（完成/失败回调、单帧/多帧结果通道），实现 HDR、包围曝光、降噪、快速连拍与长按连拍，并接线快门点击、长按与按键拍照入口时
  - 情境：源端以带完成与错误回调的调用发起拍照（如 takePicture(pictureCallback, errorCallback)）：完成回调里复位拍照阶段与“相机操作中”标志、续拍剩余重复、按偏好暂停预览，错误回调恢复预览；多帧模式按 burst 类型决定帧数并整组交付；长按快门进入连续快拍，松手停止。目标把编排、相机控制器、保存与页面拆到不同文件或切片，经注入的桥接或通道相连；目标相机会话可能没有连续 burst 类型。
  - 例外：长按连拍照源端门控进入：源端在长按偏好关闭、录像模式、快速连拍模式、只存 RAW 等情形下不进入连拍的，目标保留这些门控，不让长按在这些情形下也开始连拍；源端没有长按连拍的，不新增。
- [目标确无对应能力的拍摄或录制选项（DNG 封装、容器、音源）在创建媒体资产前明确失败，不改写成相近选项或伪装成功](lesson-938301f1bd3b133b6af4.lesson.md)
  - 时机：拍照保存与录像配置实现阶段，源端格式或选项在目标缺少对应封装或枚举、要决定走失败路径还是降级时；收口阶段处理这类缺口的占位时
  - 情境：源端支持 RAW（DngCreator 写 DNG）、3GP/WebM 容器、特定录音音源或独立的采集帧率；目标缺 DNG 封装等价物，或 SDK 只提供部分 CodecMimeType、ContainerFormatType、AudioSourceType；规格把封装层列为平台缺口候选，实现者准备把原始缓冲直接按 .dng 写入媒体库并返回成功，或把不支持的选项映射为另一个可用值。
  - 例外：决策台账已批准该选项降级为某个具体替代，并写明用户可见差异；源端自己写了回落规则的（如某音源在低版本或不支持时回落到默认音源），目标照源端的回落规则实现，这不算静默替换；本做法只管源端没有回落、目标自行换值的情形。
- [相机 photoAvailable 回调的 JPEG 字节交给异步保存时，先复制 byteBuffer 再释放 Photo](lesson-376cb07bc6b225bfd396.lesson.md)
  - 时机：拍照接线与图像保存实现阶段，从 PhotoOutput 的 photoAvailable 回调取 component.byteBuffer、决定 Photo.release 时机时
  - 情境：源端 onImageAvailable 先把 JPEG 平面复制成 byte\[\] 再 image.close()；目标在 photo.main.getComponent(JPEG) 后拿到 byteBuffer，字节要交给排队的后台保存或其他异步消费者。
- [相机拍摄的照片与录像走相机系统资产保存，不默认用需受限写权限 WRITE_IMAGEVIDEO 的 createAsset 系列](lesson-262681f65adf4aeb0ce3.lesson.md)
  - 时机：相机拍照与录像的保存实现阶段，为相机产出的照片、视频选择媒体库写入接口与 PhotoOutput、AVRecorder 输出回调时（源端存进系统相册、目标没有 WRITE_IMAGEVIDEO 受限权限签名授权）；规格提取写 MediaStore → photoAccessHelper 映射行时
  - 情境：源端经 MediaStore insert（IS_PENDING 两段写）或 MediaRecorder 输出文件保存拍摄结果；目标是没有受限权限签名授权的普通应用，候选有 photoAccessHelper createAsset/createAssetRequest、PhotoOutput 的 photoAvailable/photoAssetAvailable、AVRecorderConfig.fileGenerationMode 的 APP_CREATE 与 AUTO_CREATE_CAMERA_SCENE。
  - 例外：工程已具备 ohos.permission.WRITE_IMAGEVIDEO 的受限权限签名授权，且当前决策要求应用自建资产；调用方（如外部拍照/录像请求）显式给出输出 URI 时，写入该 URI；源端把照片或录像只写在应用私有目录、不进系统相册的，目标照源端写应用沙箱（照片走 photoAvailable 取字节、录像用 APP_CREATE + 沙箱文件 fd），不改成相机系统资产：saveCameraPhoto 与 AUTO_CREATE_CAMERA_SCENE 会把文件存进相册。
