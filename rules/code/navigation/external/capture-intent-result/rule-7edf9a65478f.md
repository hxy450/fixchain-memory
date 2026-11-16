# 意图要 inline-data 位图而 want 带不了时，按 RESULT_CANCELED 结束，不报成功

审的是：代码
触发（任一种）：
- 读到：源码 ACTION_IMAGE_CAPTURE 没带 EXTRA_OUTPUT 时把小图 Bitmap 放进返回 Intent 的 data extra（inline-data）；写错的样子：目标注释写「terminateSelf 无 setResult 数据通道 → 平台缺口」，没有数据仍以成功结束，把请求报成成功
适用范围：接线阶段要声明「平台缺口」，或源端回传的数据在目标端带不过去时
做法：
- 声明平台缺口前先查目标 API（如 UIAbilityContext.terminateSelfWithResult），不以上游的临时实现为准
- 数据确实带不过去（want 带不了 inline 位图）时，释放位图后 terminateSelfWithResult({ resultCode: 0 })，按取消结束
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 没有 EXTRA_OUTPUT 时源端把小尺寸图片作为 Bitmap 放在 extra 里返回：inline-data 分支回传的是位图数据（出处：android.provider.MediaStore#ACTION_IMAGE_CAPTURE）
- terminateSelfWithResult(parameter: AbilityResult): Promise<void>：目标有回传结果码和数据的通道，不是平台缺口（出处：鸿蒙 SDK 的 ets/api/application/UIAbilityContext.d.ts，UIAbilityContext.terminateSelfWithResult）
- 修好后 inline 请求释放位图后按取消结束：修好后的做法（出处：卡里修好并验证过）
未核实：want 带不了 inline 位图出自卡，本机声明里没有查实
来源：1 张卡，1 个应用
- case-76fcde297f6a5406e58f（opencamera-hmos）：做法第 1 步 ← 建议 5；做法第 2 步 ← 建议 5、诊断；取值 3 ← 诊断
