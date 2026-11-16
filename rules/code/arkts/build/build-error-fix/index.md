# 为修编译错误改过的文件

agent 会看到什么：读过的构建日志只报 import / export、@Entry 或某个符号未导出（has no exported member、not exported）；交回的修复改动超出报错处：整文件重写换掉了没报错的组件写法，或删掉了整块功能

## 规矩

- rule-1d76f5066a19｜为修某条编译错误整文件重写时，没报错的组件用法原样保留｜读到：构建错误只指向导入/导出或 @Entry 一类问题（如 declares 'X' locally, but it is not exported）；写错：整文件重写后的版本里，未被报错的组件用法换了写法（如删掉 @Builder 页签方法、把 .tabBar(this.…) 改成对象字面量）
- rule-65d6db9352bc｜编译报 @kit.ArkUI 未导出 CanvasRenderingContext2D 时只删 import，不删图表｜读到：编译日志只报 import { CanvasRenderingContext2D, RenderingContextSettings } from '@kit.ArkUI' 的符号未导出；写错：修复把整个 Canvas 图表（trendContext、绘制函数、Canvas 调用）删掉，换成文字点列之类的占位来通过编译
