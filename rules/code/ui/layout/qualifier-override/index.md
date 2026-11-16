# 资源限定符目录的覆盖（values-w / sw、layout-land）

agent 会看到什么：读到源 res 里同名资源在 values-w<N>dp、values-sw<N>dp 的 dimens.xml 或 layout-land 下另有定义，交回的代码只用了基础值，或方向分支漏了部分属性

## 规矩

- rule-32caefa759bc｜合并 layout 与 layout-land 时逐控件逐属性比两份 XML，每个差异都有方向分支或覆盖说明｜读到：源 res/layout/ 和 res/layout-land/ 下有同名布局，同一 android:id 的 background、textSize、margin、layout_weight 不同；写错：目标组件对 layoutWeight、margin、fontSize 做了 isLandscape 分支，背景形状（borderRadius / backgroundColor）却没有分支，转换报告也没说明被哪段运行时代码覆盖
- rule-2e6fff7b2842｜源 @dimen 有宽度限定覆盖时，目标按窗口宽度取值，不写单值 $r('app.float…')｜读到：源布局用 @dimen/… 设 padding 或 margin，而源 res 的 values-w<N>dp 或 values-sw<N>dp 下的 dimens.xml 覆盖了同名键；写错：目标各处写成 $r('app.float.…') 单值（只有基础值）；或者把水平、垂直等几个源 dimen 合成一个常量
- rule-bb88f4584b5f｜资源有横屏覆盖时，几何代码在重算入口里运行期读资源，不用写死的常量｜读到：源码 getResources().getInteger(R.integer.x) 读的资源在 res/values-land 有覆盖；或工程里同时有同名的常量和需要 context 的资源读取函数；写错：目标几何计算直接引用写死竖屏值的 export const 常量，没有调用 resourceManager 或现有的按 context 读取的函数
- rule-db4c8352707e｜源布局有 layout-land / layout-sw600dp 同名变体时，按窗口条件写两套分支｜读到：被替代的源布局在 res/layout-land/（或 layout-sw600dp/）下有同名 XML；占位登记或移交行写明「横屏变体 layout-land/… 权重 …」；写错：共享组件只按 res/layout/ 的竖屏结构写 layoutWeight，没有按窗口方向的分支，头注只溯源 res/layout；也没有登记横屏移交项
- rule-a0a69937d1ab｜sw 限定符译成运行期条件时，用 display 宽高较小者比阈值，不用 mediaquery min-width｜读到：源工程 `values-sw<N>dp-land` / `values-sw<N>dp` 里的覆盖值，或规格写“最小宽度≥N”；写错：目标用 mediaquery.matchMediaSync('(min-width: Nvp) and (orientation: landscape)') 或按窗口 width 判断，手机横屏也命中
