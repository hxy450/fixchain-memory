# 容器背景加嵌套 ImageView 的元素

agent 会看到什么：读到源布局里一个元素由容器的 android:background 位图加嵌套 ImageView 的 android:src 图标组成；规格的元素→资源表只列了背景图

## 规矩

- rule-532f41a280f8｜规格的资源清单要覆盖容器背景和嵌套 ImageView 的 src，按元素写出对应｜读到：源布局里一个元素由容器 android:background 位图加嵌套 ImageView 的 android:src 图标组成（如悬浮入口）；写错：规格的元素→资源表只列了背景图，漏了嵌套 ImageView 的图标
