# 降采样与 EXIF 方向迁到 ImageSource：用 desiredSize 而非 sampleSize，ORIENTATION 的描述字符串映射成角度

ID：`lesson-108eabea8042e1daf064` · 版本：1

[本主题](index.md)

## 何时使用

图片解码与缩略图实现阶段，把 Android inSampleSize 降采样与 ExifInterface 整数方向读取翻译为 image.ImageSource 的 createPixelMap 与 getImageProperty 时

## 适用情境

源端按 inSampleSize 算法降采样解码，并以整数读取 EXIF 方向后旋转；目标准备把 sampleSize 直接填进 DecodingOptions，把 getImageProperty(ORIENTATION) 的返回值 Number() 成角度。

## 原因

d.ts 对 DecodingOptions.sampleSize 只写“Sampling ratio”，在已观察的 API 24 设备上非 1 值（如 8）使解码失败；ORIENTATION 按 d.ts 返回 'Top-left'、'Right-top' 一类描述字符串，Number() 得到 NaN，旋转被跳过。凭 Android 记忆断言“直接支持”、不读 d.ts，这两处都会出错。

## 做法

1. 按源端算法得到 sampleSize 后，用 getImageInfo 取原尺寸，以 desiredSize = 原宽高 ÷ sampleSize 传给 createPixelMap，不填 sampleSize；ImageSource 用完 release。
2. ORIENTATION 读出后按描述值映射：Top-left→0、Right-top→90、Bottom-right→180、Left-bottom→270，并兼容返回数字串的情况。

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-d5c3514ada560cb5134d](../../../store/cases/case-d5c3514ada560cb5134d/f08e3534f55b8cc6ebd570ff39c426fb4462edec6d303e3d2574fe5789a9b67f.json) · 结论：diagnosis, recommendation:3
  卡片版本：`f08e3534f55b8cc6ebd570ff39c426fb4462edec6d303e3d2574fe5789a9b67f`
