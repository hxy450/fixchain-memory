# 手写 getString/String.format 的位置参数插入时，不把用户数据作为 String.replace 的替换串：用 split/join 或替换回调字面插入

## 何时使用

实现阶段，把 Android getString(resId, args) 或 String.format 的 %1$s、%s 位置参数改写为 ArkTS 字符串拼装（自写 formatRes 一类 helper）时

## 适用情境

源端 getString(R.string.x, name) 把用户输入的名称、标题插入格式串（如克隆名后缀）；目标取到格式串后准备用 s.replace('%1$s', arg) 替换占位，或复用兄弟页面已有的同类 helper。

## 原因

JS 的 String.replace 会解释替换串里的 $$、$&、$`、$' 等模式，参数含这些字符时插入结果与原文不同；Android 的格式化按字面插入参数。

## 做法

1. 字面插入：s.split('%1$s').join(arg)，或 s.replace('%1$s', () => arg)（回调返回值不做模式解释）；格式串有多个占位时按序号逐个处理。若本地 SDK 声明提供带格式化参数的取串接口（如 resourceManager.getStringSync(resId, ...args)），可直接用它。
2. 复用工程已有的格式化 helper 前，核对它是否把参数当替换串插入，是就一并改正。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因〕Resources.getString(id, formatArgs) 先取出资源串，再以当前配置的首选 Locale 调 String.format 代入参数；%s、%1$s 这类格式符把参数的字符串形式直接插入，不解释其中的 $ 等字符
- 〔做法第 1 步〕String.prototype.replace 的回调重载（第二个参数是函数）用回调的返回值作为替换文本
- 〔做法第 1 步〕resourceManager 的 getStringSync(resId, ...args)（API 10 起）按 %d、%f、%s、%%、%数字$d、%数字$f、%数字$s 格式化资源串：%1$s 取 args[0]，依此类推；%% 转义为 %
