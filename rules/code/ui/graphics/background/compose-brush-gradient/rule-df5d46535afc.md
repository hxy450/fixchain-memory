# Compose 默认对角渐变在宽高不等的组件上，angle 取 90+atan2(h,w)，不写 RightBottom

审的是：代码
触发（任一种）：
- 读到：Compose 源码 Brush.linearGradient(colors) 没写 start / end（默认沿组件自身 (0,0) → (w,h)），用在宽高不等的胶囊、卡片上；写错的样子：目标写 direction: GradientDirection.RightBottom 或 angle: 135，宽胶囊上渐变变成上下走向（上青下紫之类）
适用范围：把 Compose 默认对角线性渐变翻译成 ArkUI linearGradient 时
不适用的情形：圆形、正方形（宽高相等）上两者等价，可以保留 GradientDirection.RightBottom
做法：
- 用 .onAreaChange((o, n) => { 记下 n.width、n.height }) 取实测宽高存进状态
- 写 .linearGradient({ angle: 90 + Math.atan2(h, w) * 180 / Math.PI, colors: … })，不设 direction
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- angle：0 度时从下往上，顺时针为正；默认 180：90 是从左往右，90 + atan2(h, w) 就是沿 (0,0) → (w,h) 的方向（出处：ts-universal-attributes-gradient-color.md，linearGradient 的 angle）
- direction 在 angle 设为非 undefined 后不生效；默认 GradientDirection.Bottom：用 angle 时不要再依赖 direction（出处：ts-universal-attributes-gradient-color.md，linearGradient 的 direction；鸿蒙 SDK 的 ets/component/common.d.ts，LinearGradientOptions）
- onAreaChange(event: (oldValue: Area, newValue: Area) => void): T：组件尺寸变化时拿到新的 width、height（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.onAreaChange）
- RightBottom 在宽胶囊上呈上下走向的渐变；按实测宽高取 angle = 90 + atan2(h, w) 后与源一致：RightBottom 的行为和修法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-40c445e1fb0a99ce0a72（Jetsnack）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3、诊断；例外 1 ← 建议 3；取值 4 ← 诊断
