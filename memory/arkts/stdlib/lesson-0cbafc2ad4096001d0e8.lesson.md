# Java/ICU 正则、String/List 方法与 Android 工具类不按形似 JS 内建改写：先列语义差异，不等价就按源实现移植

ID：`lesson-0cbafc2ad4096001d0e8` · 版本：1

[本主题](index.md)

## 何时使用

服务层、模型层与页面逻辑实现阶段，把源码直接调用的 Java 正则、String/List 方法或 Android 平台工具类翻译成 ArkTS 表达式时；规格提取阶段为这些调用写契约时

## 适用情境

源方法体调用的是平台库而不是应用自身代码：Pattern/matches/replaceAll（\s、\p{L}、Pattern.quote 交替）、String.split("")、compareToIgnoreCase、List.remove(Object)、android.util.Base64.decode、Uri.parse(path).getPath()、ContentResolver.getType；目标只有 JS RegExp/String/Array 与内建解码可用，写者准备在注释里写“等价/直迁”。

## 例外与边界

- 规格或差异决策已明确接受对应差异，并写明受影响的输入

## 原因

这些调用与 JS 内建形似而语义不同：Android 的 java.util.regex 由 ICU 实现，\s 匹配 Unicode 空白而不只 ASCII 空白，\p{L} 不含组合标记 \p{M}；Pattern.quote 交替的 replaceAll 单遍扫描，拆成多遍 split/join 会重复替换；split("") 按码点切分而 JS 字符串按 UTF-16 单元；compareToIgnoreCase 逐字符先比大写再比小写，不等于整串小写比较；List.remove(Object) 原地移除首个相等元素，filter 新建数组并删掉全部；Base64.decode(DEFAULT) 跳过字母表外字符并按状态机处理“=”；Uri.parse(path).getPath() 剥离 scheme/authority 并做百分号解码；ContentResolver.getType 对未知扩展名常返回 application/octet-stream（例：FileProvider）。近似实现加“等价”注释收口后，编译与常规样例都通过，只在边界输入上偏离。

## 做法

1. 写“等价/直迁”前逐项列出所用调用的源端语义与 JS 内建的差异：正则字符类所属引擎、替换是否单遍、切分单位、比较规则、原地修改还是新建、解码容错、URI 解析与解码、未知值的平台默认；对不上的按源实现逐分支移植成共享函数，各调用点复用。
2. 常用对照：\s、\p{L} 按 ICU 字符集写成显式 Unicode 类并用 u 标志；Pattern.quote 交替的 replaceAll 写成一个交替正则单遍替换；split("") 用 Array.from 按码点切；compareToIgnoreCase 逐字符先比 toUpperCase 再比 toLowerCase；List.remove(Object) 用 indexOf + splice 原地移除首个；Base64.decode(DEFAULT) 移植 android.util.Base64 的解码状态机；Uri.parse(path).getPath() 先解析 scheme/authority 再百分号解码；getType 未知扩展名回退 application/octet-stream 后再走源端归类。
3. 规格提取写这类契约时写语义点（切分与截断规则、正则引擎、舍入、解码容错、未知值默认）并标“需逐语义移植”，不用“非空白字符数”“拒绝某前缀”一类口语描述。

## 可选检查

- 对“等价”有疑问时，用边界输入与源端对照：emoji 与组合字符、全角空格、大小写变体、尾随分隔符、含空白或非法字符的 Base64、带 scheme 与百分号编码的路径、未知扩展名

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-e9189514e875ef00f96f](../../../store/cases/case-e9189514e875ef00f96f/70962a835201462f5cdf9dc9d03b341d51dc0e830922cf32d7761f935762ea1b.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:4
  卡片版本：`70962a835201462f5cdf9dc9d03b341d51dc0e830922cf32d7761f935762ea1b`
