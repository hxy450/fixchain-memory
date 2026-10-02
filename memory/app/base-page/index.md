# app/base-page

Android 业务基类（BaseActivity、BaseBusinessActivity）横切行为迁到组合式 BasePage：生命周期埋点与返回归因、触摸分发与点外收键盘的逐方法映射与逐页接线

[上一级](../index.md)

## 本级经验

- [Android 业务基类的横切行为逐方法映射到组合式 BasePage，并逐页落地生命周期调用](lesson-2fcb6612ee4106b34e17.lesson.md)
  - 时机：公共基座实现与页面转换阶段，把 BaseActivity/BaseBusinessActivity 等业务基类的 onCreate、onDestroy、onBackPressed、dispatchTouchEvent 行为迁到 ArkUI 页面时
  - 情境：Android 页面统一继承业务基类，由基类自动完成页面展示/退出埋点（停留时长、返回键归因）、触摸计数与点外收键盘等；ArkUI @ComponentV2 struct 不能继承，目标改用需逐页调用的组合式 BasePage 或工具类，页面还可能先于公共基座生成。
