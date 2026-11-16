# 映射 MediaPlayer→AVPlayer 时，映射行写明源端不抢音频焦点、播放中 start() 无效

审的是：规格
触发（任一种）：
- 读到：源端 MediaPlayer.create(context, R.raw.x) 后 start()，没有 AudioAttributes 或 requestAudioFocus；写错的样子：规格映射行写「AVPlayer + rawfile/…，play() 重置重播」，没写与其他音频混播、播放中再触发不重启
适用范围：规格把源端短提示音 MediaPlayer 映射到 AVPlayer 时
做法：
- 映射行写明两条隐式语义：源端未申请音频焦点（与其他音频混播，目标用 AudioSession concurrencyMode = CONCURRENCY_MIX_WITH_OTHERS 并设 audioRendererInfo）；start() 在播放中调用无效（目标播放中不重启）
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Calling start() has no effect on a MediaPlayer object that is already in the Started state：源端播放中再 start() 不会重播（出处：android.media.MediaPlayer（类注释的状态说明））
- CONCURRENCY_MIX_WITH_OTHERS：和其他音频流并发，需在音频流启动前激活 AudioSession：对应源端不抢焦点（出处：audio-session-management.md，音频会话策略）
来源：1 张卡，1 个应用
- case-e332c2cc4929f36c08c7（Cofi）：做法第 1 步 ← 建议 6、诊断
