# 源组件的无障碍语义（contentDescription、role、合并朗读）

agent 会看到什么：读到源端 android:contentDescription 初值取字符串资源、运行时改成拼出的字符串，或 Compose 的 Modifier.clickable(role = Role.Button, enabled = …)、整卡合并的点击区、独立 IconButton、Dialog；规格把喂给 .accessibilityText() 的状态写成 string | Resource，或组件验收条目没写按钮角色、enabled 条件、合并朗读和对话框模态

## 规矩

- rule-67e42c3f5098｜派生状态要喂给 accessibilityText 这类分开声明重载的属性时，规格里状态类型只写 string｜读到：源端 android:contentDescription="@string/…" 初值取字符串资源，代码里 contentDescription = … 改成运行时拼出的字符串；写错：状态接口表把喂给 .accessibilityText() 的派生状态（@Computed）类型写成 string | Resource，转换决策没写资源串怎么取成字符串
- rule-5628eddc118b｜规格把源组件的语义属性写进组件验收条目：role、enabled、合并或独立按钮、对话框模态｜读到：源端组件 Modifier.clickable(role = Role.Button, enabled = …)、整卡合并的点击区、独立 IconButton、Dialog 独立窗口；写错：组件验收条目只写结构、样式与回调，没写按钮角色、enabled 条件、合并朗读与独立按钮、对话框模态
