# app/modules

多模块工程（products 壳 HAP + features/components HAR）的边界：构建模式常量的来源、跨模块导入方式、页面迁入或移动时资源闭包的归属与按模块校验，按页面归属规划业务模块边界（不按功能编号或历史包名）

[上一级](../index.md)

## 本级经验

- [HAR 模块不引用宿主 BuildProfile：构建模式由壳层入口注入，跨模块只从包名入口导入](lesson-6bd9ae0de39cecc06744.lesson.md)
  - 时机：多模块拆分、插桩或结构修复阶段，把代码迁入或写入 HAR 模块、需要 DEBUG 等构建模式常量，或调整跨模块导入时
  - 情境：工程拆为 products 壳 HAP 与 features/components 等 HAR 模块；迁移或新增的 HAR 代码需要构建模式常量（裸模块名 'BuildProfile' 只在宿主 HAP 可解析，每个 HAR 另有自己生成的 BuildProfile），或宿主页要使用其他模块的类；整包 assembleHap 能通过，IDE 按模块做 ArkTS 检查。
- [规划业务模块拆分时按页面归属建表，不把功能编号或源端包分组一对一当作模块边界](lesson-99b35920e77ae01076ea.lesson.md)
  - 时机：架构重构规划阶段，确定业务模块划分及各页面、模型、服务、ViewModel 的归属时；执行搬迁时判断页面去向时
  - 情境：目标工程要从单模块拆成多个业务模块；基线功能清单或源工程按历史包名分组，同一业务对象（列表、新增、详情、编辑与数据层）分散在不同功能组或包里，详情页只经路由从另一业务的列表进入。
- [页面迁入或在 HAR 之间移动时带走资源闭包：静态 $r 与按名取资源都要在本模块或已声明依赖中可解析](lesson-edb937b04e0f1494ca37.lesson.md)
  - 时机：架构重构或模块拆分阶段，把页面迁入 HAR 或在 feature 间移动页面、确定字符串/媒体/颜色资源归属时；在 HAR 页面把按名取资源改写为静态 $r 时
  - 情境：多模块工程（壳 HAP + HAR）里页面或组件移入某个 HAR；页面用 $r('app.string/media/color.x') 或 getStringByNameSync/localized('x') 使用资源，定义可能仍只在壳模块、AppScope 或另一个 feature；整包构建会合并资源，只有按模块分析才报 Unknown resource name。
