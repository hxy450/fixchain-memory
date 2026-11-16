# 规划切片时列出继承源端基类的全部 Activity，把前台注册、注销和默认 onNewIntent 写进页面切片清单

审的是：计划与派工
触发（任一种）：
- 读到：源端多数 Activity 继承同一个基类，基类在 onResume / onPause / onNewIntent 里有统一行为；写错的样子：切片计划里页面切片的 wires 或 closer 清单没有前台注册、注销和默认 onNewIntent 这一边；writeback 只拿服务文件给页面级验收条目交账，条目声明的锚点并不存在
适用范围：生成切片计划和收口 writeback 时，源端基类行为要落到每个页面上
做法：
- 从源码列出全部继承该基类的 Activity，把前台注册、注销和默认 onNewIntent 写进对应页面切片的 wires 或 closer 清单
- writeback 交账前核对验收条目声明的目标锚点（Mixin 或页面）确实存在
来源：1 张卡，1 个应用
- case-3735da03c6e544339df6（MifareClassicTool）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2
