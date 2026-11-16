# 主题与深浅色

计划或决策写主题「深浅双主题跟随系统」、源端按 isSystemInDarkTheme() 选套，派工要拆主题令牌任务时

## 触发族

- [深浅主题跟随系统的任务拆分](follow-system-theme/index.md)（4 条）：计划或决策写主题「深浅双主题跟随系统」、源端按 isSystemInDarkTheme() 选套，主题令牌任务的派工限定「纯常量文件」，没写深浅状态可观察、入口由谁读 colorMode
- [应用内主题切换和页面里的 $r 取色点](in-app-theme-color-refs/index.md)（3 条）：规格或主题层写主题由应用内设置、调色板驱动，页面渲染期读主题对象令牌、不走 $r，而已生成的页面和组件里有 $r('app.color.…')、getColorSync 取色；占位登记、移交项、「全局主题」占位的关闭或主题合流的派工没有按文件覆盖这些取色点
