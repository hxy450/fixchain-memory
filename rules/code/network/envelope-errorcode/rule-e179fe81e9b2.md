# 修补回调分支的文案或常量前，按源端完整判别路径逐层对照分支结构

审的是：代码
触发（任一种）：
- 读到：源端网络回调先按信封 isSuccess 分流，成功分支里再按 dataObj.has("…") 分流，错误码和附带标志用 data 层的 optInt("errorCode") / optBoolean(…) 读，位于成功分支的 else 里；写错的样子：目标把同名错误码判断放在 if (report.success) {…; return} 之后（成功分支之外），修补时只改了文案或常量，结构没动
适用范围：对齐复核或修补阶段，对照源端网络回调改某个分支的文案、常量或参数时
做法：
- 先写出源端到达该分支的完整判别路径（信封成功 → data 里某键是否存在 → data 层错误码），和目标代码逐层对照；层级或判别键不同就一并修正结构，不只替换字符串
- 按源端结构写：错误码分支放进「信封成功且 data 无该键」的路径，错误码和标志从 data 层读，信封失败分支只做源端那几步（提示 msg、停计时等）
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- JSONObject#has(name)：有这个键的映射就返回 true（值可以是 NULL）：源端按键存在性分流，目标要用同样的键存在性判断，不是按值真假（出处：org.json.JSONObject#has）
- JSONObject#optInt(name) 缺键或不能转成 int 时返回 0；optBoolean(name) 返回 false：源端从 data 层读错误码和标志时的缺省值（出处：org.json.JSONObject#optInt、#optBoolean）
- 上限弹窗移进成功分支的无该键路径，成功判定取 root 层，errorCode / 标志取 data 层：返修后的分支结构（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-5b91aeeca2e493368af0（企业安全培训）：做法第 1 步 ← 建议 1；做法第 2 步 ← 诊断；取值 3 ← 诊断
