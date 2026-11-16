# 重构计划的跨业务依赖

agent 会看到什么：重构计划里的跨业务依赖模拟：是手写的依赖骨架，还是当前代码里页面、ViewModel、Service 之间真实的 import 和路由跳转

## 规矩

- rule-7fb6e0eaaf9d｜跨业务依赖模拟用手写骨架时，改用当前代码真实的 import 和路由关系｜读到：目标工程当前代码里页面、ViewModel、Service 之间的 import 和路由跳转；写错：重构计划的跨业务依赖模拟只建了手写的依赖骨架文件，没有列出当前代码谁 import 谁、谁跳到谁
