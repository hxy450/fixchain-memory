# 平台库调用不以形似 JS 内建加“等价”注释收口：ICU 正则字符类、码点切分、List.remove、Base64/Uri 逐项按源语义移植

ID：`lesson-5e3ba83ebfe5bbdf9278` · 版本：2

[本主题](index.md)

## 何时使用

实现阶段把 Java/Android 平台库调用（正则、字符串切分与比较、集合删除、Base64、Uri、MIME 查询）替换为 JS 内建或自写简化函数，准备在注释里写“等价/直迁”时；规格提取阶段描述这类调用的契约时

## 适用情境

源码调用 Pattern/String.matches/replaceAll（Android 上由 ICU 执行）、split("")、compareToIgnoreCase、List.remove(Object)、android.util.Base64.decode、Uri.parse(path).getPath()、ContentResolver.getType；目标准备用 JS RegExp 字符类或手写 ASCII 空白集、charCodeAt 逐单元计数、整串 toLowerCase 比较、filter、自写宽松解码、对原始串直接处理或静态扩展名表替代；规格对这些调用只有口语描述（如“非空白字符数”“拒绝 /data 前缀”）。

## 例外与边界

- 决策记录明确批准某项语义差异，并写明用户可见影响

## 原因

形似 API 的边界语义不同：Android 正则由 ICU 执行，\s 是 Unicode White_Space、\p{L} 不含组合符 \p{M}，与 JS 的 \s 集合不完全相同，手写 ASCII 空白集更窄；Java split("") 按码点切分，charCodeAt 按 UTF-16 单元，emoji 计为 2；compareToIgnoreCase 逐字符先 toUpperCase 再 toLowerCase 后比较，与整串 toLowerCase 的排序可能不同；List.remove(Object) 原地删除首个相等元素，filter 新建数组并删除全部；Base64.decode(DEFAULT) 有自己的跳过字符与 “=” 处理状态机；Uri.parse(path).getPath() 会剥离 scheme/authority 并做百分号解码；FileProvider 类的 getType 对未知扩展名返回 application/octet-stream。注释自称“等价”后，这些差异不再被复核。

## 做法

1. 写替换前把每个源调用的语义点列成对照（字符单位、空白与字母字符集所属引擎、大小写折叠方式、删除首个还是全部、解码容错、路径解析、未知值默认），逐项决定按源算法移植或登记差异；Java 文本读行与 split/trim、集合迭代序、float 运算按对应经验处理。
2. 常用写法：ICU 字符类用 u 标志与 Unicode 属性写全（\s → \p{White_Space}，\p{L} 不并入 \p{M}）；split("") 与字符计数用 Array.from 或 for…of 按码点；compareToIgnoreCase 逐码点 toUpperCase 再 toLowerCase 后比较；List.remove(Object) 用 indexOf + splice(i, 1)；Base64.decode 与 Uri.parse().getPath() 按 AOSP 源码逐状态移植；getType 未知扩展名回落 application/octet-stream 再按源端归类。
3. 注释写“等价/直迁”前，用一组边界输入对照源端结果（emoji、全角空格、大小写变体、尾随分隔符、含非法字符的 Base64、file:// 或含百分号的路径、未知扩展名），对不上就按源算法移植，不以近似实现加注释收口。目标侧结果在设备的 ArkTS 运行时上取，不只按 ECMAScript 规范推断：运行时正则的 \b 会把部分非 ASCII 字符当作 ASCII 处理，/ui 对非 BMP 字符的大小写折叠也与预期不一致（HarmonyOS 文档 arkts-runtime-faq，访问于 2026-10-17）。
4. 源码依赖的三方库源文件不在工程内时，按依赖坐标取发布版源码，从真实正则与常量移植，不从单元测试用例反推契约。

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-e9189514e875ef00f96f](../../../store/cases/case-e9189514e875ef00f96f/70962a835201462f5cdf9dc9d03b341d51dc0e830922cf32d7761f935762ea1b.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`70962a835201462f5cdf9dc9d03b341d51dc0e830922cf32d7761f935762ea1b`
