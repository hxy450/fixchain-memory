# 字符串

源端有 res/values*/strings.xml、arrays.xml 和 values-* 语言目录，或控件、代码引用的 @string、@android:string、android.R.string 文案；目标端有 string.json、strarray.json 和语言限定词目录时

## 触发族

- [values-* 语言目录对应的限定词目录](locale-dirs/index.md)（8 条）：源 res/ 下有 values-zh、values-zh-rTW、values-es 等语言目录，或只有默认 values/；目标 resources/ 下的限定词目录和源端对不上（少语言、values-zh 收窄成 zh_CN、合成了源端没有的 zh_CN），或限定词目录的键集比源端该语言多
- [strings.xml、arrays.xml 的值转写成 element JSON](string-value-conversion/index.md)（10 条）：源 strings.xml / arrays.xml 的值跨行书写、带 \n \' \" 转义或未转义双引号、含 <p> <a> <b> 子元素，或是 <string-array> 的项；产物 string.json / strarray.json 的 value 残留转义和缩进、为空、数组项是纯字符串、@string/ 引用没改写
- [string.json 条目的文案来源](string-text-source/index.md)（11 条）：源控件的 android:text 引用 @string/…、写死字面量、走平台 @android:string/cancel，或代码格式化出标题和数量；产物 string.json 里的值是自拟、概括或按键名猜的，缺源端有的文案或格式串，建了源端没有的条目，或只写了 base 一种语言
