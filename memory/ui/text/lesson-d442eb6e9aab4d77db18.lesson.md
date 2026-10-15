# 源端在代码里格式化的含固定措辞文案（SimpleDateFormat、String.format、拼接）也建参数化字符串资源并用 $r 传参，不写模板字符串

ID：`lesson-d442eb6e9aab4d77db18` · 版本：1

[本主题](index.md)

## 何时使用

界面转换阶段，为源端在代码里动态生成的可见文案（日历年月标题、带单位的数量等）选择文本来源并登记字符串资源时

## 适用情境

Android 源在 Kotlin/Java 里用 SimpleDateFormat、String.format 或拼接生成带中文单位或固定措辞的显示文本（如 yyyy年M月），不在 strings.xml 中；目标工程约定可见文案走 $r('app.string.*')，模块 string.json 已有 %s 参数化条目。

## 例外与边界

- 文本只由纯数字或数据值构成（如日期格子的 day.toString()）

## 原因

转换者容易只把 XML 里的静态文本当作要资源化的文案，代码里拼出的标题就留成模板字符串，绕过资源化约定与多语言替换；资源化自检通常也只对照 XML 来源的键。来源中转换者同一次追加了十余个静态文案键，唯独年月格式串写成了反引号模板。

## 做法

1. 源端代码生成的显示文本只要含固定措辞或单位，就建参数化字符串资源（如 %s年%s月），用 $r('app.string.<key>', 参数...) 传值；沿用本模块 string.json 已有的 %s/%d 写法与命名前缀，参数保持源格式的数值形态（如 M 不补零）。
2. 追加本页静态文案键时，把动态标题、数量、单位等格式串一并登记。

## 可选检查

- 有疑问时检索本页 Text()、accessibilityText() 实参中的反引号模板或 + 拼接，夹带非数字字面量的改为格式资源。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-c8f1e6989f066bb2f51a](../../../store/cases/case-c8f1e6989f066bb2f51a/379e0f87386f11ebb46f6831f460e384c959a9411825b37cb85d5be90a6e69ac.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`379e0f87386f11ebb46f6831f460e384c959a9411825b37cb85d5be90a6e69ac`
