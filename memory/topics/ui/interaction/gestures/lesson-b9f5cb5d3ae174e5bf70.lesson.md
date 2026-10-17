# 源端自写触摸状态机或用框架手势类时，按源阈值、跟手与取消逐项复刻，不以 onClick/SwipeGesture/PinchGesture 识别器代替

ID：`lesson-b9f5cb5d3ae174e5bf70` · 版本：4 · 阶段：spec/execute · 主题：[ui/interaction/gestures](index.md)

概要：自写触摸状态机按源阈值复刻，不换识别器

信号：`onTouch`, `dispatchTouchEvent`, `ItemTouchHelper`, `ScaleGestureDetector`, `SwipeGesture`, `PinchGesture`, `PanGesture`, `getSwipeThreshold`, `item_touch_helper_swipe_escape_velocity`, `MotionEvent`

## 何时使用

规格提取阶段把源端 MotionEvent 处理或手势类翻成交互契约时；界面实现阶段为列表项滑动、画廊点击与缩放选择 onClick、SwipeGesture、PanGesture 还是 onTouch 时

## 适用情境

源端 onTouch/dispatchTouchEvent 自写 DOWN 记点、MOVE 超阈值取消点击、UP 判定点击；或用 ItemTouchHelper 滑删、ScaleGestureDetector 或三方缩放控件；映射参考写“ItemTouchHelper Swipe → SwipeGesture”“ScaleGestureDetector → PinchGesture 直接映射”，或规格写“目标点击与滑动天然分离，无需迁移”。

## 例外与边界

- 源端本身就是识别器回调（setOnClickListener、onLongClick）且没有自定义阈值时，直接用对应识别器

## 原因

识别器在识别成功时一次性回调：SwipeGesture 识别即触发，只有速度阈值（默认 100vp/s），没有跟手位移、位移阈值与回弹，与 PanGesture（默认 5vp 距离）以默认方式或互斥方式同绑时先达条件者触发（HarmonyOS 文档 arkts-gesture-events-single-gesture，访问于 2026-10-17）；onClick 不含源端“移动超过阈值取消点击”的规则，也不保证与 Swiper 拖动互斥。映射表只给组件候选，阈值与时序在源方法体和框架默认参数里。

## 做法

1. 先读源方法体及其所用框架类的默认参数，列出跟手位移、触发阈值、速度阈值、取消条件与回弹或落定，并为每项在目标代码中指出承接的位置。
2. 源端自写 DOWN/MOVE/UP 状态机时用 onTouch 逐事件移植，阈值按源端单位换算；与 Swiper、List 的拖动联动取消点击（如 Swiper 开始拖动时清除按下状态）。
3. ItemTouchHelper 滑删用 PanGesture 或 onTouch 跟手平移，松手按源 Callback 判定滑出或回弹；未覆写时取库默认值：getSwipeThreshold 为 0.5 个条目宽，甩动速度阈值为 item_touch_helper_swipe_escape_velocity（androidx recyclerview 资源，120dp/s）。
4. 缩放、双击类三方控件仓内无源码时，从依赖缓存或 AAR 取出 class 反编译（javap 等）核对缩放、双击与拦截行为；仍无法确认就在规格登记行为缺口，不静默降级为无缩放。
5. 规格阶段把源端显式状态机写成带阈值边界的行为验收条目；只有核实了目标事件模型，才可登记“目标内建，无需迁移”。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [规格与源码冲突按源实现，例外只认决策 ID](../../../process/secondary-over-source/lesson-7a065e8fe384b8c462cc.lesson.md)（共享 1 张卡）

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-1a09dd649093f650a6fc](../../../../../store/cases/case-1a09dd649093f650a6fc/da04b374b7092b19b66477caa7b72bf7555cde232a69d7d65bab1fe080a2a458.json) · 结论：diagnosis, rec-f5f5202f69, rec-395e87c63e, rec-d06426ccbe, rec-5181317241
  卡片版本：`da04b374b7092b19b66477caa7b72bf7555cde232a69d7d65bab1fe080a2a458`
