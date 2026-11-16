# 同一组件链上出现第二组 .width/.height 且数值异常大时，删掉后加的那组，保留原尺寸

审的是：代码
触发（任一种）：
- 读到：源端 ImageView 给的是固定 dp（@dimen 引用）或 match_parent 尺寸；写错的样子：Image(...) 的链上已有 .width('18vp').height('18vp') 或 .width('100%').height('100%')，后面又追加了一组 .width(21845).height(1431000589) 这类远超屏幕的整数尺寸
适用范围：构建、验证或收口阶段读到同一组件有两组 width/height 修饰时
做法：
- 按后写生效核对最终尺寸：同一链上后加的那组覆盖前面的显式尺寸；数值远超屏幕（上万 vp）或与已有显式 width/height 重复的，当场删除这组，保留按源端写好的尺寸（如 '18vp'、'100%' 加 objectFit）
- 不能只改相邻属性就继续构建；删不掉或拿不准来源时上报
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 删除尾随的 .width(21845).height(1431000589)，保留 18vp 和 100%/Cover 后显示恢复：修好的写法；不删时整屏被图标铺满（出处：卡里修好并验证过）
- width(value: Length): T，传 number 时单位是 vp：.width(21845) 就是 21845vp，远超任何屏幕（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.width；ts-universal-attributes-size.md，width）
未核实：自愈脚本具体的解析缺陷和它读到的数值卡里没能核实
来源：1 张卡，1 个应用
- case-500cf2e63e19988f0420（android-panorama-map-vest7）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3；取值 1 ← 诊断
