# 给共享组件传值前代入它的可见性分支核对，只构造的层不能传会命中隐藏分支的值

审的是：代码
触发（任一种）：
- 读到：共享组件里有 .visibility(值 === 0 ? Visibility.Hidden : Visibility.Visible) 一类分支；源端这一层只构造、保持 View.VISIBLE；写错的样子：页面给这一层的组件参数传读自恒为 0 的数据的值，组件走到 Visibility.Hidden，整层不显示；共享文件不能改时也没有改渲染路径或上报缺口
适用范围：页面接线时给已写好的共享组件传参
做法：
- 传值前读组件的可见性与取色分支，把要传的值代入，核对结果与源端该层状态一致；最小检查：这一层传 0 时 visibility 表达式是否返回 Visibility.Visible
- 共享文件不能改时，改用不走隐藏分支的渲染，或上报组件缺口，不传会命中隐藏分支的值
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Visibility.Hidden：隐藏但参与布局占位：命中这一分支时组件不画，但仍占位（出处：鸿蒙 SDK 的 ets/component/enums.d.ts，Visibility.Hidden）
来源：1 张卡，1 个应用
- case-1320d29332e802ec2cce（Privacy Friendly 2048）：做法第 1 步 ← 建议 4；做法第 2 步 ← 建议 4、诊断
