# app/modules

构建模式常量与多模块工程（products 壳 HAP + features/components HAR）的边界：BuildConfig.DEBUG 映射为 hvigor 生成的 BuildProfile.DEBUG、HAR 中构建模式的来源，跨模块导入方式、页面迁入或移动时资源闭包的归属与按模块校验，按页面归属规划业务模块边界（不按功能编号或历史包名）；单模块内可复用函数不从路由页面模块导出，放进普通模块

[上一级](../index.md)

## 本级经验

- [BuildConfig.DEBUG 映射为 hvigor 生成的 BuildProfile.DEBUG，不因源码目录检索不到就删 DEBUG 分支](lesson-3af52968ce5762501cd3.lesson.md)
  - 时机：实现与收口阶段，把源端含 BuildConfig.DEBUG 的可见性或行为条件转换为 ArkTS 时
  - 情境：目标为 hvigor 构建的工程，源码目录内尚无 BuildProfile 引用，模块根目录也没有 BuildProfile.ets；规格或已批准决策写着“DEBUG 构建 || X”一类条件。
  - 例外：代码位于 HAR 模块时，裸模块名 'BuildProfile' 只在宿主 HAP 可解析，构建模式改由壳层入口注入
- [HAR 里需要构建模式时不引用宿主的 BuildProfile：用本模块生成的 BuildProfile，须与宿主构建模式一致时由壳层入口注入](lesson-6bd9ae0de39cecc06744.lesson.md)
  - 时机：多模块拆分、插桩或结构修复阶段，把含 DEBUG 等构建模式判断的代码迁入或写入 HAR 模块时
  - 情境：工程拆为 products 壳 HAP 与 features/components 等 HAR 模块；迁移或新增的 HAR 代码需要构建模式常量，源端或壳层写法是 import { DEBUG } from 'BuildProfile'（裸模块名只在宿主 HAP 可解析）；每个 HAR 在模块根另有自己生成的 BuildProfile.ets；整包 assembleHap 能通过，IDE 按模块做 ArkTS 检查。
  - 例外：代码位于 HAP 模块时，直接从宿主的 'BuildProfile' 读 DEBUG（生成文件同时导出 DEBUG 常量和兼容用的默认类 BuildProfile，hvigor-ohos-plugin 6.23.6），见 BuildConfig.DEBUG 映射一条
- [多模块工程跨模块使用类只从模块包名入口导入：静态检测误报时不改成跨模块相对路径](lesson-de57dd7aa272b8dd8248.lesson.md)
  - 时机：多模块工程的实现、插桩或结构修复阶段，宿主页或其他模块要使用某个 HAR 的类，或为通过静态检测调整导入路径时
  - 情境：工程拆为壳 HAP 与多个 HAR，HAR 在 Index.ets 导出对外的类，并在使用方的 oh-package.json5 中声明依赖；结构检测或孤儿文件扫描不解析模块名，把合法的包名导入报为未使用或孤儿。
- [规划业务模块拆分时按页面归属建表，不把功能编号或源端包分组一对一当作模块边界](lesson-99b35920e77ae01076ea.lesson.md)
  - 时机：架构重构规划阶段，确定业务模块划分及各页面、模型、服务、ViewModel 的归属时；执行搬迁时判断页面去向时
  - 情境：目标工程要从单模块拆成多个业务模块；基线功能清单或源工程按历史包名分组，同一业务对象（列表、新增、详情、编辑与数据层）分散在不同功能组或包里，详情页只经路由从另一业务的列表进入。
- [页面与组件共用的非 UI 函数放进普通模块：不从路由页面模块具名导出供生产代码导入](lesson-b58f26f0fdb7fb00db9e.lesson.md)
  - 时机：界面实现阶段，新组件或弹窗要复用某个页面文件里的校验、工具函数，决定函数放在哪个模块、从哪里导入时
  - 情境：可复用的非 UI 函数（正则校验、提交前校验链等）定义在 pages/ 下经路由表或 pageMap 注册的页面模块中，该页面可能已为单测导出个别函数；新组件会被主 Ability 首页静态导入，工程同时带有 entry_test 单测或 UI 测试 HAP。
  - 例外：函数本来就定义在 services/、utils/ 等非页面模块中
- [页面迁入或在 HAR 之间移动时带走资源闭包：静态 $r 与按名取资源都要在本模块或已声明依赖中可解析](lesson-edb937b04e0f1494ca37.lesson.md)
  - 时机：架构重构或模块拆分阶段，把页面迁入 HAR 或在 feature 间移动页面、确定字符串/媒体/颜色资源归属时；在 HAR 页面把按名取资源改写为静态 $r 时
  - 情境：多模块工程（壳 HAP + HAR）里页面或组件移入某个 HAR；页面用 $r('app.string/media/color.x') 或 getStringByNameSync/localized('x') 使用资源，定义可能仍只在壳模块、AppScope 或另一个 feature；整包构建会合并资源，只有按模块分析才报 Unknown resource name。
