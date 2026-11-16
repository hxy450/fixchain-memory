# 派 UI 转换时，把「百分比宽不扣 margin、水平 margin 下沉为父 padding」放进转换者实际读的参考

审的是：计划与派工
触发（任一种）：
- 读到：源布局里有 match_parent（或两侧约束 0dp）又带 layout_marginHorizontal / marginStart / marginEnd 的视图；写错的样子：派工的必读检查项、映射参考和前置 skill 里只有 match_parent → '100%'、margin → .margin()，没有「百分比宽不扣 margin」这条；它只在没分给转换者的 skill 里
- 读到：转换器预载或要读的映射参考只逐属性给出 match_parent → '100%'、layout_margin → .margin()，pitfalls 清单里没有「100% 加水平 margin 溢出」；写错的样子：页面转换任务的派工说明里没有交代 match_parent 与水平 margin 同链时的组合写法
适用范围：派发安卓布局到 ArkUI 的页面或组件转换任务、决定转换者加载哪些参考和检查项时
做法：
- 派工的检查项、映射参考或前置 skill 里写上：width('100%') 按父宽算、水平 margin 另向外扩；源子视图占满父宽又带水平 margin 时，不并写 .width('100%') 与水平 .margin，水平间距下沉为父容器或包装容器的 padding，或写 .width('calc(100% - Nvp)')（N 为两侧 margin 之和）
- 这条规则只在转换者不预载的 skill 里（如 android-view-to-arkui 的 Layout Parameter Mapping）时，一并交给转换者，或补进它必须逐条检查的 pitfalls 清单
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 在 Row、Column、Flex 交叉轴上布局时，子组件交叉轴的大小与 margin 的和为整体：检查项要写的依据（出处：ts-universal-attributes-size.md，margin）
来源：3 张卡，3 个应用
- case-28bedbfdb77e8d050b15（免费来电多多）：做法第 1 步 ← 建议 4；做法第 2 步 ← 建议 4
- case-be590c45de6e4195a7aa（实时公交）：做法第 1 步 ← 建议 4、建议 3；做法第 2 步 ← 建议 4
- case-c42ad6674b3abc0daece（AntennaPod）：做法第 1 步 ← 建议 3、建议 1；做法第 2 步 ← 建议 3
