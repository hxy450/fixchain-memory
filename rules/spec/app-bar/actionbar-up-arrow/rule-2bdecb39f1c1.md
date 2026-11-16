# 规格导航表里 Up 和系统返回各写一行，照源码各自的调用填

审的是：规格
触发（任一种）：
- 读到：源码 android.R.id.home 分支调 super.onBackPressed() 或 finish()，onBackPressed 覆写里另有回退分支；写错的样子：规格导航表把「ActionBar Up 尖角」和系统返回写成一行「与系统返回共用同一分支」，Up 也先走覆写里的回退
适用范围：规格提取阶段写导航表的 Up 行和系统返回行时
不适用的情形：home 分支调的是 this.onBackPressed()，两路本来同一逻辑，可以写成同一分支
做法：
- 导航表 Up 与系统返回各写一行，照源码各自的调用填写：Up 行写 home 分支的实际调用和效果（如 super.onBackPressed() → 退出本页），系统返回行写覆写里的分支
来源：1 张卡，1 个应用
- case-3d6b5f99f326a3e5e8e9（Sokoban）：做法第 1 步 ← 建议 3、诊断；例外 1 ← 建议 2
