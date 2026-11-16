# 工厂按 type 分派的编辑项列表

agent 会看到什么：读到源端遍历配置列表、经工厂按每项 type 用 when 分支 create 对应 Fragment 并按顺序加进同一容器（else 落到空 Fragment）；产物里的列表提供函数、按类型分支的渲染、未匹配类型的回退和对应用例

## 规矩

- rule-aa5561f48fa9｜源端 factory 按 type 分派 Fragment 时，目标列表收全各 type、保持顺序，不按 type 过滤｜读到：源码把配置里的编辑项列表逐项交给 factory，按 type.name 分派到各自的 Fragment（when 分支），没有「须先选中某项」之类前置条件；写错：目标的列表提供函数里写了 .filter(item => item.type !== '<某 type>' && …)，或只在某个选中状态下放行该 type，把它挪给页内另一个入口承载
- rule-61c6e4d4f664｜删除或替换某 type 的替代入口时，一并移除列表里与该 type 相关的排除条件｜写错：改动删掉了某个 type 的页内替代入口（如页内文本编辑器），列表提供函数里 item.type !== '<该 type>' 或「选中子模块才放行」的条件还留着
- rule-88a0cfa663ef｜源端工厂按配置项 type 逐个创建 Fragment 时，目标逐行显式分派到专页，按配置顺序放在同一列表｜读到：源端编辑 Fragment 遍历配置列表，经工厂按每项的 type 用 when 分支各自 create 对应 Fragment，按顺序加入同一个容器；外观类（背景、文字色、边框）也在同一个 when 里；写错：目标用一个通用控件（Toggle / Slider / TextInput / Radio）按类型分支统一渲染多数类型，已有专页的类型没接专页；外观类编辑器放在列表外、提前显示，或和列表里的同类项重复
- rule-b95c9745f045｜源端工厂的 else 落到空 Fragment 时，目标未匹配类型空渲染，不显示占位文案｜读到：源端工厂的 else 分支 create 一个什么都不显示的空 Fragment；写错：目标把非工厂 type 映射成 `'unsupported'` 之类，用 Text(...) 在界面上显示「暂不支持」一类 fallback 文案
- rule-ce6033bad244｜为配置驱动的编辑项列表写用例时，按源端配置断言每项都在且顺序一致，子集只按源端实际移除的项｜读到：源码按配置列表逐项由 factory 创建 Fragment，另有子模块场景按固定的几个 type 从列表里移除；写错：测试没有「配置含多个 type、未选中子模块时这些项都在列表里、顺序与配置一致」的 expect(...) 断言，或子模块用例断言的移除项比源端多
