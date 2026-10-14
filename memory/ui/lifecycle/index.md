# ui/lifecycle

组件实例与重建：条件渲染换出实例、转屏存档恢复与重画

[上一级](../index.md)

## 本级经验

- [条件渲染换出自绘组件时，按身份解除绑定，并在新实例挂上后重画](lesson-5191382cc4af6a6f15d0.lesson.md)
  - 时机：规格提取与界面实现阶段，把安卓转屏重建（横竖屏双布局加onPause存档、onResume恢复）映射为ArkUI按方向if/else切换布局，并为分支内的自绘组件设计控制器与重画时机时
  - 情境：源Activity未声明configChanges，竖横屏各一套布局，转屏时Fragment经存档→恢复向新视图重新绘制；目标在build中按方向if/else切换两套布局，每套挂一个Canvas自绘组件，共用宿主持有的控制器。
