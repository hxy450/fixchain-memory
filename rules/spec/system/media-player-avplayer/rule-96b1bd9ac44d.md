# 台账以「会新增播控卡片」为由把后台续播记成平台差异时，改记缺失功能并接入

审的是：规格
触发（任一种）：
- 读到：安卓 MediaPlayer 播放在宿主 onPause/onStop 后继续，退后台播到结束；写错的样子：决策台账或平台差异登记里写「接入 AVSession 会新增控制中心播控卡片」，据此不接 AVSession、不做后台续播
适用范围：源端退后台继续播放、目标端未做后台播放，台账里把它登成平台差异时
做法：
- 撤销这条平台差异，改记为缺失功能：源端继续播放而目标端被系统静音，按 AVSession + AUDIO_PLAYBACK 长时任务 + backgroundModes/KEEP_BACKGROUND_RUNNING 接入
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 从 API version 20 开始，接入 AVSession 后后台任务模块不发通知栏通知，由 AVSession 发通知：播控卡片是后台播放本来就有的系统表现，不是接入带来的额外差异（出处：continuous-task.md，使用场景（关于AUDIO_PLAYBACK（音视频播放）说明））
- 未接入时退后台被系统静音暂停，接入 createAVSession + startBackgroundRunning(AUDIO_PLAYBACK) 后与源端一致，平台差异撤销：这是缺失功能，不是平台不可行（出处：卡里修好并验证过）
未核实：卡里上机对照出自 HarmonyOS 6.1.1(24)，本机文档副本按 API 23 核对
来源：1 张卡，1 个应用
- case-1dee716aadc97af875f2（omni-notes-hmos）：做法第 1 步 ← 建议 4、诊断；取值 2 ← 诊断
