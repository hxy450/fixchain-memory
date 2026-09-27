# ui/theme

主题、语义色、控件默认样式与 style 继承属性（圆角、高度、渐变、字号）的迁移，被引用 drawable 的取值，视觉属性逐项取自源布局与适配器，颜色约束的写法，以及按色值选择颜色资源

[上一级](../index.md)

## 本级经验

- [“页面零硬编码色值”只禁止字面色值，不禁止用 $r 引用语义色](lesson-2e4279c4b82f06af64fd.lesson.md)
  - 时机：规格提取阶段书写颜色约束，或页面实现阶段解读规格里的颜色约束时
  - 情境：规格或功能说明写有“页面代码零硬编码色值”“深浅色由资源限定词目录负责”等全局约束，而具体控件仍需要与源端一致的颜色。
- [布局引用的 @drawable（progressDrawable、背景 shape、标签背景）先打开取数值：高度、圆角、轨道色、渐变与描边写进规格与实现](lesson-771d1ba1a032b769097a.lesson.md)
  - 时机：规格提取与界面实现阶段，为进度条、搜索框、分组标签等引用 drawable 的控件确定高度、圆角、颜色与描边时
  - 情境：源布局以 progressDrawable=@drawable/xxx、background=@drawable/bg_xxx 引用 layer-list/shape 资源，尺寸、圆角、轨道色、渐变和描边写在被引用文件里；目标工程可能已有名称相近、含义不同的颜色资源。
- [引用 style 或抽成共享 @Builder 的控件：先展开共享默认值，再逐实例叠加元素自身的覆写（字号、圆角、间距）；圆角不按半高推，也不照抄相邻控件](lesson-bc5b8558ab086168b462.lesson.md)
  - 时机：界面实现阶段（含返修期重写弹窗或按钮），为通过 style 继承形状、尺寸与渐变的控件确定修饰链时；把重复 XML 元素抽成 @Builder 时
  - 情境：源 XML 控件以 style="@style/X" 继承圆角、高度、渐变等属性，元素本身只覆写部分项；同一或相邻布局里有圆角更大的卡片，或同 style 但显式覆写成胶囊的按钮。或按键等控件以 style 给默认 textSize、单个控件再覆写不同字号；多个同构元素（分组标题）各自带不同的 layout_marginTop。
- [把 Android 主题隐式提供的控件外观写成目标控件的显式样式](lesson-47785524c7f132ea7efe.lesson.md)
  - 时机：规格提取阶段写控件转换决策，或页面实现阶段写出按钮等控件的修饰链时
  - 情境：源布局中的 Button 等控件没有声明 background / backgroundTint / textColor / 圆角，外观来自应用主题（如 Theme.MaterialComponents 的 colorPrimary、colorOnPrimary）；目标工程已迁移同名语义色资源，而 ArkUI 对应组件不设样式时使用平台默认外观。
  - 例外：源控件已在布局或 style 中显式声明样式，此时按显式声明转换；决策记录明确要求目标端采用平台默认外观
- [按源端控件的实际色值在颜色资源里反查同值键，不按 accent、primary 等名称选键](lesson-4e9507a2a793c5583aa8.lesson.md)
  - 时机：界面实现阶段，为按钮、背景、文字设置颜色资源引用时
  - 情境：源端颜色以 shapeSolidColor、background、textColor 等硬编码色值或色值资源给出；目标工程已有多组语义名相近但色值不同的颜色资源（如脚手架留下的 color_accent 与迁移出的 brand_accent）。
- [视觉属性逐项取自源布局、item 布局与适配器分支，缺项就补读，不以近似值、通用卡片或自拟分隔线代替](lesson-e4e65a99e545871f96ae.lesson.md)
  - 时机：界面转换与视觉返修阶段，确定标题栏背景、文字颜色与字号、周末与选中样式、item 尺寸、胶囊圆角、行高与分隔线时
  - 情境：页面规格只给合成的结构（无颜色与尺寸），视觉数值分散在 Fragment 布局、include 布局、item 布局与适配器 convert 分支里；转换者可能只读到部分文件，或读到了却按经验取整。
