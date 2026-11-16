# 收口跑了会改写源码的自愈脚本后，回执要列出它的改动并做量级检查，不能只报 findings 计数

审的是：计划与派工
触发（任一种）：
- 读到：收口协议写明 pipeline 模式会自动运行 icon-sizing 图标尺寸自愈，它是唯一会改写源码的 detector，改动记录写在 icon-pipeline-iterN.json；写错的样子：收口回执只报 findings 计数和结果文件路径，没有列出脚本改了哪些文件哪些行，也没有对新增尺寸做量级检查就继续派修复
适用范围：结构收口阶段运行会改写 .ets 的自愈脚本、决定是否接受它的改动时
做法：
- 跑完自愈脚本先读它的改动记录（icon-pipeline-iterN.json）或 git diff，再看 detector 收敛结果
- 对新增尺寸做量级检查：数值远超屏幕尺寸（如上万 vp）或与同组件已有显式 width/height 重复的，回滚这处改动并在回执里上报
来源：1 张卡，1 个应用
- case-500cf2e63e19988f0420（android-panorama-map-vest7）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1、建议 2
