# 源端动画终点取目标控件实际边界时，目标用 onAreaChange 实测边界注入 Canvas，不用布局常量

审的是：代码
触发（任一种）：
- 读到：源端动画终点用 findViewById(...) 的 getLeft() / getTop() / getWidth() / getHeight() 取目标控件实际位置和尺寸；写错的样子：覆盖层按布局规格推导终点中心、写死尺寸常量，不读目标控件 onAreaChange 的实测边界；不同布局模式下终点和控件对不上
适用范围：在 Canvas 覆盖层上复刻飞向某个控件的动画时
做法：
- 在目标控件上写 .onAreaChange((oldValue, newValue) => …)，把 newValue 的位置和宽高记成边界，注入 Canvas 覆盖层作为动画终点
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onAreaChange(event: (oldValue: Area, newValue: Area) => void): T：组件尺寸或位置变化完成时回调，newValue 给出实测宽高和位置（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.onAreaChange）
- 终点改读 onAreaChange 实测的画廊控件边界后，不同布局模式下动画都落在控件上：返修的落法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-d5c3514ada560cb5134d（opencamera-hmos）：做法第 1 步 ← 建议 6、诊断；取值 2 ← 诊断
