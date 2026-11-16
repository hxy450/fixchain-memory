# BitmapFactory 的解码选项（inSampleSize、inJustDecodeBounds）

agent 会看到什么：读到源端 BitmapFactory.Options 先 inJustDecodeBounds 取尺寸、再按 2 的幂设 inSampleSize 降采样解码；产物里 ImageSource.createPixelMap 的 DecodingOptions 写了 sampleSize 还是 desiredSize

## 规矩

- rule-9bb86548a68a｜inSampleSize 不直译成 DecodingOptions.sampleSize，改算 desiredSize｜读到：源端 BitmapFactory.Options 先 inJustDecodeBounds 取尺寸，再按 2 的幂设 inSampleSize 降采样解码；写错：目标 ImageSource.createPixelMap 的 DecodingOptions 里写 sampleSize: <源端的 inSampleSize>
