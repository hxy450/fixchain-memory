# 源 material3 Slider 迁移时自绘 M3 轨道和竖条 thumb，顶层透明 Slider 负责交互

审的是：代码
触发（任一种）：
- 读到：源端 material3 Slider，只用 SliderDefaults.colors 传部分颜色，thumb 和刻度取 M3 默认；写错的样子：目标用 Slider({ style: SliderStyle.OutSet }) 内置圆形 thumb，没有竖条 thumb、thumb 两侧留隙和刻度点
适用范围：要求一比一还原 material3 滑杆外观时
做法：
- 按 M3 几何自绘轨道、竖条 thumb、thumb 两侧留隙、刻度点和末端 stop indicator；上面叠一个透明的 Slider 负责交互，刻度恰在 thumb 加留隙的边界上时照画
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- SliderBlockType.DEFAULT = 0：Round slider：内置滑块是圆形（出处：鸿蒙 SDK 的 ets/component/slider.d.ts，SliderBlockType.DEFAULT）
- 自绘轨道加 4×44 竖条 thumb、留隙、刻度点和末端 stop indicator，顶层透明 Slider 交互：修复后外观与源端一致（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-7f41c5604c3a5213023b（Jetsnack）：做法第 1 步 ← 诊断；取值 2 ← 诊断
