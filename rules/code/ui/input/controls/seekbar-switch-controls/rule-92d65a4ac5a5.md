# SeekBar 拇指尺寸转 Slider 时，blockSize 传 { width, height }，不传数字

审的是：代码
触发（任一种）：
- 读到：SeekBar 有 android:thumb 或自定义拇指尺寸，规格要求转 Slider；写错的样子：.blockSize(<数字>) 直接传 number
适用范围：把 SeekBar 迁成 ArkUI Slider 并设置滑块大小时
做法：
- 写成 .blockSize({ width: <直径>, height: <直径> })，参数是 SizeOptions 对象
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- blockSize(value: SizeOptions): SliderAttribute：滑块尺寸，参数是带 width / height 的对象（出处：鸿蒙 SDK 的 ets/component/slider.d.ts，SliderAttribute.blockSize）
来源：1 张卡，1 个应用
- case-de8de9ff9274ca3ce884（AntennaPod）：做法第 1 步 ← 建议 1、诊断
