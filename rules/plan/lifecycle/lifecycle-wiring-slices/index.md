# 源端基类与跨切片的生命周期接线

agent 会看到什么：源端多数 Activity 继承的基类在 onResume / onPause / onNewIntent 里的统一行为、前一切片引擎代码留给后续切片调用的 onStop / onResume 接线入口，在切片计划、派工、占位登记里有没有落点

## 规矩

- rule-9d7773ab3d3b｜规划切片时列出继承源端基类的全部 Activity，把前台注册、注销和默认 onNewIntent 写进页面切片清单｜读到：源端多数 Activity 继承同一个基类，基类在 onResume / onPause / onNewIntent 里有统一行为；写错：切片计划里页面切片的 wires 或 closer 清单没有前台注册、注销和默认 onNewIntent 这一边；writeback 只拿服务文件给页面级验收条目交账，条目声明的锚点并不存在
- rule-0a9449d340ed｜服务切片不能改页面、AC 锚点的基类等价物不存在时，逐页登记 handoff，不以「归消费切片」交账｜读到：规格验收条目的目标锚点是一个基类等价物（Mixin 之类），工程里不存在；派工禁止本切片改页面；写错：source-notes 只写页面调用「归各消费切片」，回执却称无新增 placeholder 需登记、integration_points 全部就绪
- rule-b9209041a269｜跨 slice 的生命周期接线在派工里列成接线项并登记占位，不只留在代码注释｜读到：前一 slice 交回的引擎代码注释写「页面退后台接线入口（由后面的 slice 调用）」，派工的 engine_api 列出 onStop()/onResume()；写错：slice 计划和派工里没有生命周期接线项，跨 slice 的占位登记里也没有这两个入口，只有代码注释提到
- rule-6e4403b39b81｜派工把基类行为转成某页义务时附上该页布局含守卫 id 的证据，拿不出不写成义务｜读到：规格的基类副作用表里某项带守卫条件（子类布局须含某 id）；写错：派工或切片计划写「某页承接基类淡入钩子（移交义务）」，没附该页布局含守卫 id 的证据
