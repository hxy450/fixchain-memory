# 移植 getString 的 %1$s 位置参数时用 split/join 字面插入，不当 replace 替换串

审的是：代码
触发（任一种）：
- 读到：`getString(R.string.…, name)` 或 String.format 带 %1$s 等位置参数，参数是用户数据；写错的样子：目标格式化写成 s.replace('%1$s', arg)（或从兄弟页沿用的同类 helper），名称含 $$、$& 时被当作替换模式
适用范围：把 Android 带格式参数的字符串资源迁成 ArkTS 字符串拼接时
做法：
- 字面插入：s.split('%1$s').join(arg)，或 s.replace('%1$s', () => arg) 用回调；复用兄弟页的格式化 helper 前先按本页源语义核对
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Resources.getString(id, formatArgs) 按 Formatter / String.format 代入参数：源端是格式化后的字面插入（出处：android.content.res.Resources#getString）
- replace(searchValue: string | RegExp, replacer: (substring: string, ...args: any[]) => string): string：回调重载：返回值按字面插入（出处：鸿蒙 SDK 的 ets/build-tools/ets-loader 内 typescript/lib/lib.es5.d.ts，String.replace）
- 改成 split/join 后名称里的 $ 字符原样保留：卡里的修法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-3b8b620c1c7fa2848a34（Cofi）：做法第 1 步 ← 建议 2、诊断；取值 3 ← 诊断
