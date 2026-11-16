# 迁移 Bitmap.recycle 时给每个 PixelMap 定唯一所有者，只释放一次

审的是：代码
触发（任一种）：
- 读到：源端 bitmap = 后处理结果.bitmap 重新赋值，缩略图和末尾 bitmap.recycle() 都针对成品，调用方另外再 recycle()；写错的样子：后处理结果只放进局部变量，缩略图和末尾 release() 仍用入参 PixelMap；调用方在保存函数返回后又各自 release() 同一个 PixelMap
适用范围：把 Bitmap 的处理和回收链路迁成 PixelMap，后处理会替换输入并释放旧图时
做法：
- 后处理返回新图时用返回值覆盖同一个变量，编码、缩略图和末尾 release() 都针对这个成品
- 删掉调用方重复的 release()，每个 PixelMap 只由它的所有者释放一次；源端调用方的 recycle() 不逐行照搬
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- public void recycle() { if (!mRecycled) { nativeRecycle(mNativePtr); …：Java 的 recycle 可重复调用，第二次起不做事，源端调用方的 recycle 只是冗余（出处：android.graphics.Bitmap#recycle）
- PixelMap 释放后，任何访问其内部数据的方法调用都会失败：PixelMap.release 不能当成可重复的冗余调用（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.image.d.ts，PixelMap.release）
- 删除三处调用方 release，工作变量只承载最终位图并在末尾释放一次：返修后的写法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-b49b06a3f59e5828d836（opencamera-hmos）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2、诊断；取值 3 ← 诊断
