# 编译报 @kit.ArkUI 未导出 CanvasRenderingContext2D 时只删 import，不删图表

审的是：代码
触发（任一种）：
- 读到：编译日志只报 import { CanvasRenderingContext2D, RenderingContextSettings } from '@kit.ArkUI' 的符号未导出；写错的样子：修复把整个 Canvas 图表（trendContext、绘制函数、Canvas 调用）删掉，换成文字点列之类的占位来通过编译
适用范围：编译修复阶段处理 ArkUI 内置类型的 import 报错时
做法：
- 删掉这条 import，直接用全局声明的 CanvasRenderingContext2D 和 RenderingContextSettings（new CanvasRenderingContext2D(new RenderingContextSettings(true))），其余绘制代码不动
- 只修报错的符号；确需降级时回写规格、把该项保持为未完成，不用文字占位替换规格要求的图表
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- declare class CanvasRenderingContext2D extends CanvasRenderer；declare class RenderingContextSettings：两者都是 ets/component 下的全局声明，不从 '@kit.ArkUI' 导入（出处：鸿蒙 SDK 的 ets/component/canvas.d.ts，CanvasRenderingContext2D、RenderingContextSettings）
- @kit.ArkUI 的导出里没有 CanvasRenderingContext2D 和 RenderingContextSettings：从它导入就报未导出（出处：鸿蒙 SDK 的 ets/kits/@kit.ArkUI.d.ts（全文搜这两个名字 0 处））
来源：1 张卡，1 个应用
- case-9d7fa754a567e2ecec7e（android-train-ticket-vest7）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2
