# 源端 updateThumbnail 同时更新画廊和覆盖层时，目标两路都送达，不 void 丢参数后标为已解除

审的是：代码
触发（任一种）：
- 读到：源端 updateThumbnail(thumbnail, isVideo, wantAnimation) 同时更新画廊按钮和预览覆盖层的缩略图动画，规格或占位登记要求接这条 seam；写错的样子：回调只把位图赋给共享状态的画廊字段，写 void isVideo / void wantAnimation 丢掉参数，占位登记按已解除处理；或覆盖层门面里没有 updateThumbnail
适用范围：页面接线和收口阶段接拍照、保存后的缩略图回调时
做法：
- 回调同时送两路：画廊服务更新画廊图标（带 thumbnail、isVideo、wantAnimation），覆盖层 updateThumbnail(thumbnail, isVideo, wantAnimation)；暂停预览时触发显示最后一张
- 覆盖层还没就绪时保留 FWD-REF 记号，或在门面接口先预留 updateThumbnail，覆盖层重建时补送；不能 void 参数后把登记项标为已解除
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 缩略图经画廊服务下发、覆盖层绑定重建时补送、暂停回看时显示最后一张后，暂停回看能显示刚拍的照片：两路接通的落法（出处：卡里修好并验证过）
针对本应用要查的：
- 源端这个回调送到哪几处：源工程里 updateThumbnail 的实现，以及规格里成功保存后要更新哪些控件的那条验收；列出每个接收方和它用到的参数，目标逐个接上
未核实：卡里环境是 API 24
来源：1 张卡，1 个应用
- case-d5c3514ada560cb5134d（opencamera-hmos）：做法第 1 步 ← 建议 4、诊断；做法第 2 步 ← 建议 4、诊断；取值 1 ← 诊断
