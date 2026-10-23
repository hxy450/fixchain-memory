# app/camera/recording

录像会话与 AVRecorder：profile 与帧率、启停串行、编码选项映射与应用层限额

[上一级](../index.md)

## 本级经验

- [AVRecorder 启停串行：共享停止任务、启动可取消](lesson-d41878bcc79f7e356a54.lesson.md) · 阶段：spec/execute · 信号：MediaRecorder.prepare, MediaRecorder.stop, MediaRecorder.release, AVRecorder.prepare
- [应用层录像限额按已录时长计，保留停止分支](lesson-1957f0e6ad83f19258e8.lesson.md) · 阶段：spec/execute · 信号：setMaxDuration, setMaxFileSize, OnInfoListener, MEDIA_RECORDER_INFO_MAX_DURATION_REACHED
- [录像档取 NORMAL_VIDEO 按帧率匹配，先启输出再录](lesson-793682615c640e55d88a.lesson.md) · 阶段：execute · 信号：CamcorderProfile, MediaRecorder, NORMAL_VIDEO, VideoProfile
- [录像选项按 AVRecorder 枚举映射，缺能力就报错](lesson-9826c047e0381581db09.lesson.md) · 阶段：spec/execute · 信号：setVideoEncoder, setOutputFormat, setAudioSource, setCaptureRate
