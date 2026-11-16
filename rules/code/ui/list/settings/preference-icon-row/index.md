# 带 android:icon 的 Preference 行

agent 会看到什么：读到 res/xml 里 <Preference android:icon="@drawable/…">，没有任何箭头元素，派工或转换表却写「箭头行」；产物里行尾加了 Text('›') 或 chevron 箭头 Image，图标按 24vp 画

## 规矩

- rule-df609570126f｜带 android:icon 的 Preference 写成 48dp 图标框加标题，不加源端没有的尾部箭头｜读到：res/xml 里 <Preference android:icon="@drawable/…">，没有任何箭头元素；派工或转换表写「箭头行」；写错：行尾加了 Text('›') 或 chevron 箭头 Image；图标按 24vp 画
