# 跨设备截图显得偏小时，尺寸类工单先把目标值和源布局 dp 对照，已一致就不写放大

审的是：计划与派工
触发（任一种）：
- 读到：双端截图来自不同设备，并排对比显示目标页主内容「偏小 / 上移」；目标页的固定高度和 marginTop 已是源布局的 dp 字面值；写错的样子：视觉工单写「主内容约缩小 10%–15%」「对齐固定高度、间距和图片尺寸」，源码缺口写成「…:unknown」，没有源布局值、目标当前值和截图折算值的对照
适用范围：视觉校验阶段根据双端截图差异撰写尺寸、间距类布局工单时
做法：
- 工单逐项列出源布局 dp 字面值、目标代码当前值、截图差异按各自设备密度或逻辑宽度折算后的 dp/vp，三方对照
- 目标值已等于源布局值时，不写「对齐固定高度」类修复建议；源码缺口写到具体的源布局文件和属性，不留 unknown
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- DENSITY_MEDIUM = 160（DENSITY_DEFAULT）、DENSITY_XHIGH = 320、DENSITY_XXHIGH = 480：dp = px × 160 / 设备密度；同一 dp 在不同密度设备上截图像素不同（出处：android.util.DisplayMetrics#DENSITY_MEDIUM、#DENSITY_XHIGH、#DENSITY_XXHIGH）
针对本应用要查的：
- 源布局里对应元素的 dp 值：源工程页面布局 XML 里该元素的 android:layout_height、android:layout_marginTop 等尺寸属性（含引用的 @dimen 资源）；读出 dp 值，和目标代码里对应的 .height / .margin 数值逐项比对
来源：1 张卡，1 个应用
- case-6a2ee155bd552b418d50（骑行记录）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1
