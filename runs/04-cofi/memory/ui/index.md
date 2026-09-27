# ui

界面迁移：布局与尺寸约束、主题样式、状态刷新、输入控件、图形资源、结果反馈与多页面导航（含返回键）的跨栈转换

[上一级](../index.md)

## 子主题

- [feedback](feedback/index.md) — 操作结果反馈：Snackbar 一类提示的宿主、时长与成功/失败态渲染
- [graphics](graphics/index.md) — 图标与图形资源：动画矢量的状态帧、系统符号替代、资源迁移中的静态化标注
- [input](input/index.md) — 输入控件：源端输入约束（长度、字符集、受控值）到 TextInput 等组件属性的转换
- [layout](layout/index.md) — 容器选择、约束与定位（ConstraintLayout、RelativeContainer、Column 等），尺寸约束（滚动容器定高、百分比尺寸），以及随滚动折叠的顶栏
- [navigation](navigation/index.md) — 多屏拆成多页面后的导航：目的地命名与参数、返回栈重建、返回键分发、挂载与生命周期归属
- [state](state/index.md) — ArkUI V2 状态刷新与订阅：@Builder 参数、页面与共享模型的绑定、ForEach 键与子组件刷新、监听的注册与释放
- [text](text/index.md) — 文本展示：源端对展示文本的加工（富文本、链接识别与点击）到 ArkUI Text/StyledString 的转换
- [theme](theme/index.md) — 主题、语义色与控件默认样式的迁移，以及颜色约束的写法
