# ui/navigation/parameters

路由参数契约：固定目的地名与 param、按接收端定义载荷、多入口共享载荷、缺失哨兵与有效性、语义冲突拆字段。

[上一级](../index.md)

## 本级经验

- [入参以 @Param 显式承接并由宿主真实传入](lesson-289cab2abd4268b26ce0.lesson.md) · 阶段：execute · 信号：@Param, @Event, newInstance, setCurrentCity
- [同一参数多语义时按源契约拆字段或入口解析](lesson-e202ff0d01ace7dee225.lesson.md) · 阶段：execute/repair · 信号：JSON.parse, pushPathByName, ViewModel, DTO
- [多入口目标页按全部 extras 定义共享路由载荷](lesson-953309e05bc1cd36c0d1.lesson.md) · 阶段：execute/repair · 信号：searchFromMap, locationType, searchText, setResult
- [带参路由目的地用固定名，参数只走 param](lesson-300200dd52892e9dadd2.lesson.md) · 阶段：execute · 信号：pushPathByName, pageMap, pathInfo.param, NavDestinationContext
- [路由入参在 aboutToAppear 读取并校验必填](lesson-0d7d6e7302f8c8c77c66.lesson.md) · 阶段：execute · 信号：router.getParams(), router.pushUrl, requireArguments, navArgs
- [路由参数以接收端为准，不读的 extra 不透传](lesson-4a7c04b864ef635c87b6.lesson.md) · 阶段：execute · 信号：putExtra, getXxxExtra, onReady, startActivity
- [路由参数缺失哨兵与有效性判定一致，错误态隐藏入口](lesson-c433adebb9d20f273b22.lesson.md) · 阶段：execute · 信号：pathInfo.param, Number.isInteger, NavPathStack, -1
