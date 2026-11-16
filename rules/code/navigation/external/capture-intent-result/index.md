# 响应拍照、录像意图时的结果回传

agent 会看到什么：读到源端响应 MediaStore.ACTION_IMAGE_CAPTURE / ACTION_VIDEO_CAPTURE，读 EXTRA_OUTPUT 等意图参数，结束时 setResult(RESULT_OK / RESULT_CANCELED, data) 再 finish()；产物里 terminateSelf / terminateSelfWithResult 的调用次数、结果码和 uri，以及调用方 uri 有没有写入

## 规矩

- rule-39f91a2db14f｜setResult+finish() 移植成一次 terminateSelfWithResult，带回结果码和 uri｜读到：源码响应 MediaStore.ACTION_IMAGE_CAPTURE / ACTION_VIDEO_CAPTURE，结束时 setResult(RESULT_OK 或 RESULT_CANCELED, data) 再 finish()；写错：目标结果函数的成功和失败分支都只调 this.context.terminateSelf()，注释说调用方会读回 want，结果码和 uri 没进 AbilityResult
- rule-83e2796934af｜源端多处 setResult / finish，目标合并成唯一出口，空 uri 回 RESULT_CANCELED｜读到：源码同一流程里有多处 setResult(...) + finish()（如录像停止时先在广播函数里回传一次，停止回调末尾再按结果回传一次）；写错：目标把每处都接到一次性的终止回调上，terminateSelfWithResult 被调两次；uri 为空时先以成功结束
- rule-852211d70951｜意图带 EXTRA_OUTPUT 的保存分支，写入完成后也要走结果出口，并先等保存完成再结束｜读到：源码意图拍照保存到调用方 uri 后 setResult(RESULT_OK) 并 finish()，意图里带 MediaStore.EXTRA_OUTPUT；写错：目标的 uri 分支只 fileIo.writeSync 写进 uri 并记成功，没有 terminateSelfWithResult 出口；只有无 uri 的分支接了结果回调
- rule-60c40ce7b440｜意图带 EXTRA_OUTPUT 时，录像器打开调用方 uri 写入、按 URI 方式完成，不删调用方资产｜读到：源码录像意图读 MediaStore.EXTRA_OUTPUT、EXTRA_VIDEO_QUALITY、EXTRA_DURATION_LIMIT、EXTRA_SIZE_LIMIT；规格写「URI（第三方 intent 指定输出）→ setResult 回传」；写错：目标录像落盘固定 photoAccessHelper.createAsset 拿 fd，完成回调固定按媒体库方式，意图参数和调用方 uri 从没传到录像器
- rule-7edf9a65478f｜意图要 inline-data 位图而 want 带不了时，按 RESULT_CANCELED 结束，不报成功｜读到：源码 ACTION_IMAGE_CAPTURE 没带 EXTRA_OUTPUT 时把小图 Bitmap 放进返回 Intent 的 data extra（inline-data）；写错：目标注释写「terminateSelf 无 setResult 数据通道 → 平台缺口」，没有数据仍以成功结束，把请求报成成功
