# 占位改挂延后和延后项的归属

agent 会看到什么：收口或复审时把占位的 resolve_by 改成「集成期」、外部视觉核验（a2h-verify）或 deferred，或保持 registered 推给别人；页面报告里的延后项没有落到谁的任务

## 规矩

- rule-66877645a4e4｜收口裁决本组的占位时先回源确认依赖，能本地实现的就地兑现，不改成无人认领的集成期延迟｜读到：登记里某 FWD-REF 的 resolve_by 是某个 Slice，依赖的是仓内可实现的自有 HTTP 端点；账本里有「懒接入」「软前置」这类数据链措辞；写错：closer 把 resolve_by 改成「集成期：……落定」之类的外部延迟，债务闸据此判 EXTERNAL / PASS
- rule-41a6d2173bd5｜「鸿蒙无对等 API」类延迟占位要写明检索范围；复审时先查 SDK 声明复核前提｜读到：占位登记或移交项里有「鸿蒙无对等 API」「待平台 API 核验后接通」一类延迟条目；写错：条目没写检索过哪些 SDK 模块和结果；收尾或复审时只把 resolve_by 改成「集成期」或补一个兜底定时器，前提一直没复核
- rule-4e42d84d9e6e｜收口处理 forward-ref-uncertain 条目时先回看源码，能实现就当场实现，不改 deferred｜读到：收口或验收阶段手里有 forward-ref-uncertain（`UNC`）条目，条目指向的源码行为已写明；写错：条目被改成 deferred 或把 resolve_by 改成「verify visual tuning」，理由写「requires runtime scroll telemetry」之类，没有回看源码
- rule-09823038990a｜收尾遇到动画类待办时派给有写权的实现步骤，不只把 resolve_by 改成外部视觉核验｜读到：registry 里有动画类的登记项（如源端 AnimatedContent 切换被降级为直切），resolve_by 指向某个切片步骤；写错：收尾或编排把它的 resolve_by 统一改成外部视觉核验（如 a2h-verify），债务闸按外部延迟放行，源行为明确却没有实现步骤接手
- rule-4173d176a3aa｜派给本 Slice 的 forward-ref 点名了源端实现类时，判「规格没给端点」前先读该类｜读到：派工把某条 FWD-REF / 占位列为本 Slice 待接，登记行点名了源端实现类；写错：回执里以「功能规格 API 表没列端点，建未指定端点即发明」为由保持 registered，或把它改交 closer 的跨 Slice 草稿，而没读过登记点名的类
- rule-41060b7387cb｜主题切片禁碰 pages/ 时，把页面报告里的「深色未建」类延后项转成有归属的任务｜读到：页面转换报告写「深色配色未建」「端点由主题切片统一」一类延后项；写错：主题切片的派工写盘边界是「禁碰 pages/」，延后项没有转成任何人的任务；派工已告知共享顶栏、主题文件可引用，页面仍另写页内顶栏
- rule-eebf4cac38c6｜收口时把 FWD-REF 改挂为集成期延期前，先确认代码在缺口下 fail-closed｜读到：占位登记里有平台缺口的 FWD-REF（如 DNG 封装待 PD 决策），注释写「直写缓冲字节」；写错：收口时把这条 FWD-REF 的 resolve_by 改挂成「集成期 PD 决策」，对应代码仍在缺口下返回成功
- rule-ed8e3a7d853c｜上传服务已建成时，宿主和收尾者直接接通共享组件的上传占位，不改写成外部裁定｜读到：宿主切片或收尾者读到共享组件里的上传占位 marker，而上传服务已经存在；写错：占位登记和 marker 被改写成「决策缺口（外部裁定归属）」一类说法以过债务闸；或者宿主连同自己名下的上传占位和接线一起删掉，交代成「选图后无反应」
- rule-b8a0047f5285｜工程找不到数据源 getter 时，登记「平台缺口」前先查 SDK d.ts，理由写 d.ts 依据｜读到：占位登记写着要注入真实数据源（如 AVRecorder 振幅、拍照会话捕获结果的 ISO / 曝光时间），在工程的控制器或录像引擎里 grep 不到对应 getter；写错：占位登记或代码注释把该项 retag 为「集成期 PD（平台缺口）」，写「HMOS … 无 … 等价 API」「注入不可达」，理由里没有 d.ts 文件和符号
- rule-60c6673deb76｜packet 里的 AC 因写权不足做不了时按阻塞范围缺口上报，closer 派有写权的人修，不只记 deferred｜读到：slice 的返回信封里把本 packet 的 AC 判为「跨切面，交主题 slice / group-closer」，只列为风险；写错：closer 派工或迁移报告写「本组不做，记入 deferred」，该 AC 没有指派执行者，也没有补写权或补 packet
