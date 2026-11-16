# 录像的视频档、帧率和录像会话

agent 会看到什么：读到源端打开相机后按 CamcorderProfile 建视频质量表、按尺寸和 videoFrameRate / setCaptureRate 选档，MediaRecorder 的 surface 进相机会话；产物里当前档的索引由谁赋值、VideoSession 的 NORMAL_VIDEO 能力面、videoProfiles 的帧率匹配和 VideoOutput 的配置与启动

## 规矩

- rule-f9f0d558ae1e｜承接的状态容器里当前索引只有 setter 没调用方时，按源端时机补建表和选档｜读到：源端在打开或切换相机后的初始化里建视频质量表、选当前档并写回 SharedPreferences；写错：目标状态容器的当前索引一直是 `-1`，只有 setter 没有调用方；消费方遇到 `-1` 返回 dummy 配置；建表只在表为空时懒加载
- rule-37496ea21545｜录像会话的预览和视频档取 NORMAL_VIDEO 能力面按尺寸加帧率匹配，并启动 videoOutput｜读到：源端录像按尺寸和帧率选档（视频档含 videoFrameRate 和捕获率），MediaRecorder 的 surface 进会话；写错：预览档沿用 NORMAL_PHOTO 能力面；视频档只比尺寸、没匹配就回落 profiles[0]、不看 frameRateRange；commitConfig 后只有 session.start()，没有 videoOutput.start()
- rule-5a0b924b77ff｜跨文件接线时把视频档的尺寸和帧率、捕获率一路传到配置 VideoOutput 的地方｜读到：上游接口收到整份视频档（含 videoFrameWidth、videoFrameHeight、videoFrameRate 和捕获率）；写错：中间层挂视频输出的接口只收 surfaceId 和宽高，binder 只传 videoFrameWidth / videoFrameHeight，帧率在中间层被丢掉
