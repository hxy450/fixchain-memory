# 源端动效锚点是按钮里的子 View 时，目标取同一元素的中心，不取整颗按钮或整行

审的是：代码
触发（任一种）：
- 读到：源端传给动效的锚点是按钮或列表行里的某个子 View（如 ImageView 图标、勾选区），动效方法对它 getLocationInWindow 后取中心；写错的样子：目标把 onAreaChange 或位置读取挂在外层 Button / Row 上，用整颗按钮或整行的中心作起点
适用范围：迁移以被点元素为起点的一次性动效时，确定起点取哪个元素
做法：
- 看源端调用处实际传进动效的是哪个 View；目标把 onAreaChange 挂在对应的同一元素（如按钮内的 Image）上，中心取 globalPosition.x + width / 2、globalPosition.y + height / 2
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onAreaChange(event: (oldValue: Area, newValue: Area) => void): T：挂在哪个组件上就报哪个组件的宽高和位置（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.onAreaChange）
- Area.globalPosition：目标元素相对页面左上角的位置：中心 = globalPosition 加半宽半高（出处：ts-universal-component-area-change-event.md，onAreaChange 参数说明）
- getLocationInWindow(int[] outLocation)：源端读的是传进来的那个 View 自己的位置（出处：android.view.View#getLocationInWindow）
- 把位置读取从整颗按钮移到按钮内的完成图标后，起点和源端一致：整颗按钮的中心偏离源端的图标中心（出处：卡里修好并验证过）
针对本应用要查的：
- 源端动效实际用的锚点 View：源工程里调用动效方法的列表适配器或对话框代码，找传给它的参数；顺着参数找到它对应布局 XML 里的控件（ImageView、勾选区等），目标在同一个元素上取位置
来源：1 张卡，1 个应用
- case-51d51ad98738e338df19（记得日历）：做法第 1 步 ← 建议 3、诊断；取值 4 ← 诊断
