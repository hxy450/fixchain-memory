# 布局里 @drawable 引用的控件外观（progressDrawable、background）

agent 会看到什么：读到布局 XML 里 ProgressBar 的 android:progressDrawable="@drawable/…" 或控件 android:background 引用 @drawable/…；规格里这个控件只写了边距和初值，没有高度、圆角、轨道色和渐变

## 规矩

- rule-0519cc9472b6｜布局用 progressDrawable 等 @drawable 引用时，规格打开该文件写出高度、圆角、轨道色和渐变｜读到：布局 XML 里 ProgressBar 写 android:progressDrawable="@drawable/…"，或控件 android:background 引用 @drawable/…；写错：规格里这个进度条只写了边距和初值，没有高度、圆角、轨道色和进度色（渐变）
