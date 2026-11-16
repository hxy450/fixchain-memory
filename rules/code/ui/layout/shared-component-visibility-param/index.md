# 共享组件和子页面的显隐入参

agent 会看到什么：读到源端控件在构造、绘制或宿主 Adapter 绑定时按条件改显隐，目标由共享组件或子页面承载；产物里组件的 @Param / @Prop 入参、默认值和组件内的 .visibility(...) 分支

## 规矩

- rule-a68aa475a9a4｜宿主 Adapter 绑定行时改写行内视图、共享行组件无对应入参时，给组件加默认原行为的入参｜读到：宿主 Adapter 绑定行时（`onBindViewHolder` 或它前后的钩子）按条件改写行内视图，如把行内某个按钮 `setVisibility(View.GONE)`；写错：目标宿主照常构造共享行组件，没传任何显隐入参，组件里那个 `Button` 在所有行都显示
- rule-50283aa2200f｜子页面带默认值的 @Param 都要由宿主给出真实来源，撤掉传参时改派生或在回执列未决｜读到：子页面声明了带默认值的 @Param（类型为 number、默认 0 这类），取默认值时拦截新增或切换条目元信息；源端按当前所选对象的 type 控制新增按钮显隐和条目元信息；写错：宿主创建子页面时没传这个 @Param，或传了又删掉，子页面一直落在默认值上；回执里也没列为未决
- rule-2c017ec678f5｜共享组件的构造态与绘制后状态不同时，加构造态参数，只在已绘制且值为 0 时隐藏｜读到：源控件构造时就设好背景、保持 View.VISIBLE，只有绘制方法在值为 0 时 setVisibility(View.INVISIBLE)；有的层只构造、从不调绘制方法；写错：共享组件写成 .visibility(值 === 0 ? Visibility.Hidden : Visibility.Visible)，没有参数能表示「构造后没绘制」的可见空格
- rule-dd5f0c07bc94｜给共享组件传值前代入它的可见性分支核对，只构造的层不能传会命中隐藏分支的值｜读到：共享组件里有 .visibility(值 === 0 ? Visibility.Hidden : Visibility.Visible) 一类分支；源端这一层只构造、保持 View.VISIBLE；写错：页面给这一层的组件参数传读自恒为 0 的数据的值，组件走到 Visibility.Hidden，整层不显示；共享文件不能改时也没有改渲染路径或上报缺口
- rule-e3c09a615674｜源 Fragment 自带第二轮装载再定显隐时，目标组件内也做这一轮，不等宿主｜读到：源 Fragment 的 `Maybe` 装载链在首轮成功后某项数据仍为 null 就再装载一次，装完再重算控件显隐；第二轮完成前只用一个临时字段兜底；写错：目标组件注释写「装载链不在此重复」，数据为 null 时一直用临时字段，重算只挂在 `@Monitor` 宿主换新实例上，组件内没有第二轮装载，也没有登记 `FWD-REF`
- rule-b839e3d05c39｜组件来源列了 Adapter 时，显隐按它的 setVisibility 分支定，不按 XML 初值｜读到：共享组件表把某个 `Adapter` 列为组件来源，Adapter 的 `getView` / bind 方法里对 TextView 按状态 `setText`、`setVisibility(...)`；写错：组件的显隐条件只按 XML 里 `android:visibility` 的初值或按空串判断写，和 Adapter 各分支（如某些类型文件名为空也 VISIBLE）不符
