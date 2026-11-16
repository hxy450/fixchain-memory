# 公共组件的标题栏先复用现有导航组件；新建时返回入口用迁入的返回图标

审的是：代码
触发（任一种）：
- 写错的样子：公共组件里新写了一个 @Component 标题栏或导航条，而共享组件表把导航条这一行归到现有框架组件
- 读到：安卓页面的返回入口引用 @drawable 下的返回图标，且这张图已迁入目标的 media 资源；写错的样子：返回按钮里写的是 Text('‹') 这类字面字符，或者只剩一个没有内容的可点击 Button()
适用范围：基础层生成公共组件时的标题栏、头部导航和返回入口
做法：
- 共享组件表归到现有框架的行（导航条等），直接 import 那个现有组件使用，公共组件库里不再新建同类组件
- 确需新建标题栏时，返回入口写成 Image($r('app.media.<返回图标迁入后的名字>')) 放进可点击的按钮或容器，图标用安卓同名返回图标的已迁入资源；标题文字、字号、颜色照页面规格里的标题样式
- 不用字面字符代替返回图标，也不留下没有内容的可点击 Button
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- (src: PixelMap | ResourceStr | DrawableDescriptor | ImageContent): ImageAttribute：Image 的构造，src 传 $r('app.media.名') 这类资源（出处：鸿蒙 SDK 的 ets/component/image.d.ts，ImageInterface）
- $r(value: string, ...params: any[]): Resource；value 的格式是 'belonging.type.name'，图片用 'app.media.名'：引用已迁入 media 目录的返回图标（出处：鸿蒙 SDK 的 ets/component/common.d.ts，$r）
针对本应用要查的：
- 返回图标迁入后的资源名：源工程布局 XML 里返回入口的 android:src 或 android:background 引用的 drawable 名；目标工程 resources 下 media 目录里的同名文件；同名对上就写进 $r('app.media.名')；目标里没有这张图时登记缺口，不用字符顶替
- 共享组件表指定复用的现有组件：共享组件表里标为现有框架的那一行写的组件位置，到目标工程对应目录找导出的 @Component；读出组件名和入参，在页面里 import 后照入参使用
来源：1 张卡，1 个应用
- case-8f39b7ae0d79870e9ad8（掌上燃气管家）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2；做法第 3 步 ← 建议 2、诊断
