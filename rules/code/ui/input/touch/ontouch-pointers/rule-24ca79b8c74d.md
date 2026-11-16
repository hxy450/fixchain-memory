# 三方手势控件没源码时，代码按 AAR 还原缩放双击，还原不了在回执登记缺口

审的是：代码
触发（任一种）：
- 读到：源布局用三方库的缩放图片或画廊控件（如 `TouchImageView`、自定义 `ViewPager`）；写错的样子：代码头注释写三方库无源码，画廊写成 `Swiper` + `Image`，没有任何缩放、双击实现，回执里也没登记缺口
适用范围：实现阶段迁移依赖库提供的交互控件时
做法：
- 从 Gradle 缓存取出该库的 classes，用 javap 还原缩放、双击、拦截行为后实现（缩放按 ScaleGestureDetector 逐事件移植）
- 还原不了时在回执里登记「缩放/双击行为缺口」，不静默降级
针对本应用要查的：
- 三方控件的交互行为：Gradle 缓存 modules-2/files-2.1/<group>/<artifact>/<version>/ 下的 aar 或 jar（按应用依赖的版本）；解出 classes.jar，用 javap -c -p 看 onTouchEvent、onScale、onDoubleTap 等方法
来源：1 张卡，1 个应用
- case-1a09dd649093f650a6fc（omni-notes-hmos）：做法第 1 步 ← 建议 4、诊断；做法第 2 步 ← 建议 4
