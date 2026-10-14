# ui/resources

位图与资源限定符：nodpi/sw目录尺寸、sw分档判档、9-patch、窗口背景填充

[上一级](../index.md)

## 本级经验

- [nodpi与sw分档目录的位图按源目录语义换算显示尺寸](lesson-a65702f24f69b6367f21.lesson.md)
  - 时机：界面实现与结构收尾阶段，为wrap_content显示的位图写ArkUI Image显式宽高、计算wrap_content容器宽度，或审核图标尺寸自愈脚本结果时
  - 情境：源位图只放在drawable-nodpi，或只按最小宽度放在drawable-swNNNdp等无密度限定目录；资源转换已把单份位图拍平到base/media。
- [values-swNNNdp分档按设备最短边dp判档，不换成窗口宽断点](lesson-9d9da10ec790154f53de.lesson.md)
  - 时机：规格提取、派工与界面实现阶段，把swNNNdp限定符的多档取值翻译成目标端选档逻辑时
  - 情境：源工程用values-swNNNdp为同一dimen提供多档取值，目标端没有等价资源限定符，需要在代码中按设备尺寸选档。
- [窗口位图背景按BitmapDrawable默认FILL拉伸铺满](lesson-db24eac3d20f6a1ea534.lesson.md)
  - 时机：规格提取与界面实现阶段，为安卓窗口级或视图级位图背景选择ArkUI填充模式时
  - 情境：源以new BitmapDrawable(...)设置窗口或视图背景（未改gravity），背景位图宽高比与目标窗口不同；目标用全屏Image或backgroundImage承载。
  - 例外：源代码显式设置了Drawable的gravity或ImageView的scaleType，此时按显式值映射
- [迁移9-patch背景时保留拉伸区和内容内边距](lesson-4df449ad7ae7324abaca.lesson.md)
  - 时机：资源转换、派工与界面实现阶段，迁移.9.png背景并交代其绘制方式时
  - 情境：源以.9.png作容器背景，四边1px标记定义拉伸区与内容内边距；资源可能位于drawable-nodpi，按物理像素绘制。
