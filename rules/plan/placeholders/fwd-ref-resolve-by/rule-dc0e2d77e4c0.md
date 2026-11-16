# 页面的数据钩子要在所归切片的数据层有提供方，FWD-REF 的 resolve_by 切片要能提供

审的是：计划与派工
触发（任一种）：
- 读到：页面规格写着加载远端数据（如“加载远端分类后嵌入分页内容”），源端页面调用自己的网络 Service；写错的样子：切片 pages_owned 或 wires 里有这个页面，但 Step 3c 数据层 scope 里没有提供该数据的 Service
- 读到：UI-only 转换把页面的加载方法写成数据前向引用；写错的样子：FWD-REF 的 resolve_by 指向的切片里没有能实现该数据的提供方，registry 里只写了一个无人实现的 Store 名
适用范围：计划阶段生成切片、UI-only 转换登记数据前向引用时
做法：
- 生成切片时逐个检查 pages_owned 中页面的数据钩子，确认 Step 3c 数据层 scope 内都有提供方
- 登记数据 FWD-REF 时确认 resolve_by 切片能提供该数据；没有就报计划缺口，不只写一个 Store 名
来源：1 张卡，1 个应用
- case-55f663018fc75d76bb0c（组件岛Widget Island）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3、诊断
