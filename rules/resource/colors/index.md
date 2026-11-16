# 颜色

源端有 colors.xml、values-night、布局和 Compose 里的色值，或颜色来自 ?attr 主题属性、控件默认样式、@android:color 和 Material 等库主题；目标端有 color.json 和 dark 目录时

## 触发族

- [主题、平台或库提供的颜色和外观值](theme-resolved-colors/index.md)（17 条）：源端颜色或外观不是自己写的值，而来自主题属性（?attr、?android:attr）、控件默认（没写 android:textColor）、平台 @android: 资源或依赖库主题（AppCompat、Material3、Holo、GlanceTheme）；color.json 等里是凭记忆的近似值、模板值，base 和 dark 同值或缺 dark 键
- [源端写明的颜色值转 color.json](color-literals/index.md)（7 条）：源端自己写明了颜色：colors.xml 与 values-night、布局里的字面色值、Compose 的 Color(0x…) 和深浅两套、数据源里的色值；color.json 里原样写了 @color / ?attr 引用，字节序或值和源不一致，dark 从 base 派生，漏了某个色、改了共享 token，或追加了按截图估的色
- [dark 目录 color.json 对页面色键的覆盖](dark-key-coverage/index.md)（1 条）：验收要求页面配色随深浅资源限定符切换，页面和共享常量引用 $r('app.color.…')；dark/element/color.json 的键少于 base 里页面用到的 app.color 键（自检输出 base N / dark M），交付说明写「无差异」、decision_gaps 为空
