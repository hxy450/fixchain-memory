# 组件上的 .accessibilityText

agent 会看到什么：读到源端的 android:contentDescription、Icon 的 contentDescription = null，或规格里 string | Resource 的文案字段，交回的代码给组件写了 .accessibilityText(...)：传的值是什么类型、文案从哪来

## 规矩

- rule-c2169106007b｜联合类型的值传给组件属性方法前查重载，没有接受整个联合的就归成单一类型再传｜读到：源端控件写了 android:contentDescription（映射参考只给 String → String）；写错：字段声明为 ResourceStr、赋 $r(...) 后传给 .accessibilityText(...)，联合类型匹配不上任何一个重载
- rule-0132484f610a｜accessibilityText 不传 string 与 $r 混合的三元，先统一成 string｜读到：派工要求文案经 $r 资源绑定；已有页面的 accessibilityText 有的传 string、有的传 $r(...)；写错：写成 .accessibilityText(<条件> ? <字符串> : $r('app.string.…')) 这种一支 string、一支 Resource 的三元
- rule-e674fc37eef2｜源图标 contentDescription 为 null 或空串时，不臆造无障碍文本，确需时用 $r 资源｜读到：源端 Icon(…, contentDescription = null) 或 contentDescription = ""；写错：目标给对应图标写死单一语言的 .accessibilityText('返回') 一类字面量，工程却是多语言资源
