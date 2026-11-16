# 播放器的播放、暂停和切集状态转移

agent 会看到什么：读过的源码或规格里有 playPause 的谓词分派、PLAYING / PAUSED 转移表、seekToNextMediaItem 切下一集和「同一媒体且 PLAYING 即忽略」的入口守卫；交回的代码里切换方法按哪个状态分派、切集时先改了哪个字段

## 规矩

- rule-493a53794dfc｜播放暂停切换方法按转移表逐态分派：只有 PLAYING 走 pause()，PAUSED 走 play()｜读到：源端 playPause 以辅助谓词分派：`谓词() ? pause() : play()`；规格转移表写 PAUSED 经 play() 或 playPause() 转 PLAYING，只有 PLAYING 经 pause() / playPause() 转 PAUSED；写错：目标写成 `if (state === PLAYING || state === PAUSED) this.pause() else this.play()`，把 pause() 允许的起始态套成切换的分派条件，PAUSED 永远走 pause()
- rule-f0e9f39deafe｜把一套实现的切换步骤接到另一套的入口时，由入口统一切换当前项，不先改写入口守卫读的状态｜读到：规格一条写启用实现的跳下一集（`seekToNextMediaItem` → 队列下一项）直接切换当前媒体，另一条写播放入口「同一媒体且 `PLAYING` 即忽略」的守卫；写错：目标代码先把当前媒体字段赋成下一项，再调用带「同一媒体且 `PLAYING` 即忽略」守卫的播放入口，守卫拿下一项和自己比较：在播中跳下一集被吞，旧音频位置记到下一集
- rule-3b6577c8aece｜页面只存当前媒体 id 折算行的在播态时，同时存播放态并在事件和 aboutToAppear 里一起重算｜读到：源列表项的次级按钮是否显示暂停、条目是否 `activated` 高亮，由「当前媒体匹配且服务在运行且状态为播放中」的谓词决定；写错：页面只保存当前播放媒体的 id，行组件 `@Param` 的在播标志写成 id 相等；状态事件处理和 `aboutToAppear` 只重查 id，不查播放状态
