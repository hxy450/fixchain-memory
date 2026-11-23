# 降采样与 EXIF 方向迁到 ImageSource：用 desiredSize 而非 sampleSize，ORIENTATION 的描述字符串映射成角度

## 何时使用

图片解码与缩略图实现阶段，把 Android inSampleSize 降采样与 ExifInterface 整数方向读取翻译为 image.ImageSource 的 createPixelMap 与 getImageProperty 时

## 适用情境

源端按 inSampleSize 算法降采样解码，并以整数读取 EXIF 方向后旋转；目标准备把 sampleSize 直接填进 DecodingOptions，把 getImageProperty(ORIENTATION) 的返回值 Number() 成角度。

## 例外与边界

- 源端算出的 inSampleSize 小于等于 1 时安卓按原图解码，目标这时不填 desiredSize（不写即按原图尺寸），不要为了统一写法硬算一个尺寸
- 方向映射以源端实际处理的取值为准：源端只处理 1、3、6、8 四个整数、其余按不旋转的，目标对带镜像的 "Left-top" 等描述值和 "Unknown Value <number>" 也按 0 处理；源端还处理镜像方向的，把镜像值一并映射，不要只留四个旋转角

## 原因

d.ts 对 DecodingOptions.sampleSize 只写“Sampling ratio”，文档写明默认 1、当前只能取 1，在已观察的 API 24 设备上非 1 值（如 8）使解码失败；ORIENTATION 按 d.ts 返回 'Top-left'、'Right-top' 一类描述字符串，Number() 得到 NaN，旋转被跳过。凭 Android 记忆断言“直接支持”、不读 d.ts，这两处都会出错。

## 做法

1. 按源端算法得到 sampleSize 后，用 getImageInfo 取原尺寸，以 desiredSize = 原宽高 ÷ sampleSize 传给 createPixelMap，不填 sampleSize（源端 sampleSize 不是 2 的幂时，安卓解码器按不大于它的最大 2 的幂取值，先折算再除；desiredSize 的宽高取正整数）；ImageSource 用完 release。
2. ORIENTATION 读出后按描述值映射：Top-left→0、Right-top→90、Bottom-right→180、Left-bottom→270，并兼容返回数字串的情况。

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1 步〕DecodingOptions.sampleSize 在声明里只注释为采样比；文档写明默认 1、当前只能取 1
- 〔原因〕设备上 DecodingOptions.sampleSize 传非 1 值（如 8）时解码失败（卡里设备为 API 24，超出本机 SDK 的 API 23）
- 〔做法第 1 步〕DecodingOptions.desiredSize 是期望输出尺寸，宽高须为正整数，比例和原图不一致时拉伸或缩放到指定尺寸；不写时按原图尺寸，(0, 0) 也表示按原图尺寸解码
- 〔做法第 1 步〕安卓 BitmapFactory.Options.inSampleSize 大于 1 时输出宽高为原图的 1/inSampleSize，小于等于 1 按 1；解码器按 2 的幂取最终值，其他值向下取到最近的 2 的幂
- 〔原因 / 做法第 2 步〕getImageProperty 读 PropertyKey.ORIENTATION 时以字符串返回描述值："Top-left" 不旋转、"Right-top" 顺时针 90°、"Bottom-right" 180°、"Left-bottom" 顺时针 270°，另有带镜像的 "Left-top" 等；读到未定义值时返回 "Unknown Value <number>"
- 〔做法第 2 步〕安卓 ExifInterface 的整数方向取值：ORIENTATION_NORMAL = 1、ORIENTATION_ROTATE_180 = 3、ORIENTATION_ROTATE_90 = 6、ORIENTATION_ROTATE_270 = 8
