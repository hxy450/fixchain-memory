# 动效起点的锚点窗口位置

agent 会看到什么：读到源端动效触发时对锚点 View（可能是按钮或列表行里的子 View）调 getLocationInWindow 再加半宽半高求起点；产物里点击时拿 onAreaChange 缓存的 globalPosition 当起点，或量的是外层 Button / Row

## 规矩

- rule-6e7351f56703｜源端触发时才读锚点窗口位置，目标取本次手势坐标，onAreaChange 缓存只兜底｜读到：源端在动效触发时对锚点 View 调 getLocationInWindow，再加 getWidth() / 2、getHeight() / 2 求起点；写错：目标在 onAreaChange 里缓存 newValue.globalPosition 加半宽半高，点击（TapGesture / onClick）时直接拿缓存值当起点
- rule-6fb4f8cd81d7｜源端动效锚点是按钮里的子 View 时，目标取同一元素的中心，不取整颗按钮或整行｜读到：源端传给动效的锚点是按钮或列表行里的某个子 View（如 ImageView 图标、勾选区），动效方法对它 getLocationInWindow 后取中心；写错：目标把 onAreaChange 或位置读取挂在外层 Button / Row 上，用整颗按钮或整行的中心作起点
- rule-ba8e6f93c87d｜源端动画终点取目标控件实际边界时，目标用 onAreaChange 实测边界注入 Canvas，不用布局常量｜读到：源端动画终点用 findViewById(...) 的 getLeft() / getTop() / getWidth() / getHeight() 取目标控件实际位置和尺寸；写错：覆盖层按布局规格推导终点中心、写死尺寸常量，不读目标控件 onAreaChange 的实测边界；不同布局模式下终点和控件对不上
