# 规格或壳注释点名的按钮要在 build 里实际渲染并按门控显隐，不只实现 handler

审的是：代码
触发（任一种）：
- 读到：派工的 cross_slice_edits 要求接通录像中拍照快照；壳页 handler 注释点名源端 ImageButton 控件，并带 FWD-REF 登记；写错的样子：只写了 handler 函数和能力门控，build() 里录制控件组没有调用它的 Button
适用范围：规格、派工或壳页注释点名了界面按钮的功能接线
做法：
- 在 build() 里渲染这个按钮（录像中显示），onClick 调用该 handler，显隐按能力位和会话里实际挂上的快照 PhotoOutput 判定
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 录像中按能力位和会话实际快照输出显示快照按钮：修复后的界面（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-7ef1335447ade047f4c7（opencamera-hmos）：做法第 1 步 ← 建议 4、诊断；取值 1 ← 诊断
