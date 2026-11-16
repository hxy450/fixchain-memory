# 音视频与媒体选取

源端有 VideoView、MediaPlayer、ExoPlayer / PlayerView、SoundPool、MediaController、选图和选文件的 Intent，目标端有 Video、AVPlayer、SoundPool、XComponent、PhotoViewPicker、SaveButton 时

## 子主题

- [相机、录像与录音](camera/index.md)（47 条）：源端有 Camera / Camera2 的 CameraDevice、预览和拍照会话、CaptureRequest / CaptureResult / CameraCharacteristics 的参数键、快门点击和长按连拍、MediaRecorder 录像、CamcorderProfile 选档、AudioRecord 采集，目标端有 cameraManager、CameraInput、PhotoSession / VideoSession、PhotoOutput.capture、VideoOutput、ManualExposure / ManualFocus / ManualIso、AVRecorder 或 AudioCapturer 时

## 触发族

- [Video 的 src 里的本地文件地址](video-local-src/index.md)（2 条）：读到源端把本地缓存文件路径经 Intent 交给 VideoView.setVideoPath 或播放器 setUrl，交回的代码把缓存、预载接口的输出或路由参数原样传进 Video({ src: … })
- [AVPlayer 的状态机和异步播控](avplayer-state/index.md)（5 条）：源端 MediaPlayer / ExoPlayer 的装载（stop → setDataSource → prepare）、播控和错误回调，对应目标 AVPlayer 的设源、prepare / play / stop 的 Promise 和 on('error') / stateChange
- [音效和播放器的封装](audio-playback/index.md)（6 条）：源端 SoundPool / MediaPlayer 播放短音效或 assets 音频、重载前 release；产物里 createSoundPool 还是每次 createAVPlayer、usage 和 loadComplete，以及播放封装类的 release 和短路分支
- [系统选择器和相册保存控件](system-picker-save-button/index.md)（11 条）：读到源端用 Intent（ACTION_OPEN_DOCUMENT、EXTRA_ALLOW_MULTIPLE）、自建相册页或 MediaStore 选取和保存图片、音频、文件，产物里是 PhotoViewPicker、AudioViewPicker、DocumentViewPicker、photoAccessHelper 和 SaveButton 的写法
- [Flutter 选图插件的兼容层（AssetPicker.pickAssets / AssetEntity）](flutter-asset-picker-compat/index.md)（4 条）：读到 Flutter 业务调 wechat_assets_picker 的 AssetPicker.pickAssets、拿 AssetEntity 的宽高和原图做处理，产物里是 OHOS 下替代插件的本地兼容层（走系统选择器、填 AssetEntity 宽高、交出前缩放）
- [播放器的播放、暂停和切集状态转移](player-state-transition/index.md)（3 条）：读过的源码或规格里有 playPause 的谓词分派、PLAYING / PAUSED 转移表、seekToNextMediaItem 切下一集和「同一媒体且 PLAYING 即忽略」的入口守卫；交回的代码里切换方法按哪个状态分派、切集时先改了哪个字段
- [播放器视图的尺寸和层级](player-view-layout/index.md)（2 条）：读到布局里 match_parent 的 PlayerView（没写 app:resize_mode），或播放时 addView(播放器 View, 0) 挂到 item 根布局的最底层；产物里 XComponent / Video 直接写 100% 宽高被拉伸，或放进封面区、没铺满 item
- [UI 侧播放控制器的取媒体和挂视频面](media-controller-binding/index.md)（2 条）：读到源端 UI 侧播放控制器的取媒体方法在成员为空时懒加载（从偏好里存的媒体 ID 读库）、MediaController.buildAsync 成功回调里直接 setPlayer；产物里目标控制器同步的 seekTo / getPosition 只读服务实例，或挂视频面以 getStatus() === PLAYING 为前提
- [媒体库的查询和删除（photoAccessHelper.getAssets、MediaAssetChangeRequest.deleteAssets）](media-library-query-delete/index.md)（4 条）：读到源端用 MediaStore 经 ContentResolver.query 查最近媒体、经 contentResolver.delete 删自有条目；产物里 photoAccessHelper.getAssets、MediaAssetChangeRequest.deleteAssets 调用前的 READ_IMAGEVIDEO / WRITE_IMAGEVIDEO 核对、有没有 await、catch 里按 err.code（201、'user deny'）分的提示，以及删除取消的测试替身
- [MediaRecorder 录像迁成 AVRecorder 的配置、上限和错误](mediarecorder-avrecorder/index.md)（5 条）：读到源端 MediaRecorder 的 setOutputFile、setVideoEncoder、setMaxFileSize / setMaxDuration、onInfo 和 OnErrorListener；产物里 AVRecorderConfig / AVRecorderProfile 的 fileGenerationMode、url、videoCodec，替代上限的文件大小轮询和 setTimeout，以及 on('error') 里按什么分档
- [MediaRecorder 迁成 AVRecorder 的录制控制](avrecorder-control/index.md)（4 条）：读到源端 MediaRecorder 的 prepare / start / stop（stop 后立即置 null、抛 RuntimeException 时删坏片）、依赖同步时序的重复录制计数，或带当次录制档位对象的错误上报；产物里 AVRecorder 的 Promise 链、停录的并发守卫和取消检查、失败分支的标志复位和回传，以及上报传的是不是档位对象
- [跨卡片、跨退后台存活的播放器](player-lifetime/index.md)（2 条）：读到源端 ExoPlayer / MediaPlayer 是全局懒创建、多张卡共用的单例，或 stop / release 只在显式退出时调、宿主 onPause / onStop 不碰播放器；产物里播放器句柄放在哪、无可见项时 stop 还是靠卸载，有没有 AVSession 和 AUDIO_PLAYBACK 长时任务
- [选图后上传并回填文本的链路](pick-upload-fill/index.md)（2 条）：读到源 @Composable 共享组件带账号参数、rememberLauncherForActivityResult 的选图回调里完成匿名判断、上传、上传中状态、按选图时的文本回填和各自的失败 Toast；产物里共享组件只剩 PhotoViewPicker、选到的图经必传 @Event 抛给宿主页，或宿主页的上传回调少了这些步骤
- [SAF 新建文档和 DocumentViewPicker 保存](document-save-picker/index.md)（1 条）：读到源端用 SAF 的 CreateDocument / ACTION_CREATE_DOCUMENT 按 MIME 让用户选导出位置；产物里 DocumentViewPicker.save 的 DocumentSaveOptions（newFileNames、fileSuffixChoices）
- [相机的多帧拍照（连拍、HDR、包围曝光）](camera-burst-capture/index.md)（1 条）：读到源端按 burst 类型（HDR、包围曝光、降噪、快速连拍）定一次快门的帧数、结果经整组回调交付；产物里拍照处 PhotoOutput.capture() 调了几次、保存请求的 images 列表放了几帧
