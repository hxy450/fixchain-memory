# FWD-REF 的 resolve_by 承接切片

agent 会看到什么：覆盖矩阵里承接的切片标为 simple/stub，或页面要加载远端数据而 UI-only 转换写成数据前向引用，占位登记里 FWD-REF 的 resolve_by 指向一个没有 wires、没有数据提供方的切片

## 规矩

- rule-3e7de9aa6325｜登记 FWD-REF 前先读承接切片计划，simple/stub、没有 wires 的切片不能当承接者｜读到：覆盖矩阵里承接这个 feature 的切片标为 simple/stub；写错：占位登记里 `FWD-REF` 的 resolve_by 指向一个切片，而那个切片计划里没有 integration_points / wires，也没有对应 Step 写这条接线
- rule-dc0e2d77e4c0｜页面的数据钩子要在所归切片的数据层有提供方，FWD-REF 的 resolve_by 切片要能提供｜读到：页面规格写着加载远端数据（如“加载远端分类后嵌入分页内容”），源端页面调用自己的网络 Service；写错：切片 pages_owned 或 wires 里有这个页面，但 Step 3c 数据层 scope 里没有提供该数据的 Service
- rule-5de2a4cf5f9c｜共享组件的服务占位，resolve_by 指向规格里真正拥有该服务的 feature 切片｜读到：spec 里某项服务（如图片上传）归某个 feature；实现共享组件时这项服务还没就绪；写错：占位登记的 resolve_by 指向一个不拥有该服务的切片，或者写成「由各宿主页承接」，把职责下推给每个宿主
- rule-f3d4d79c62bc｜占位推给后续批次时，标成阻塞项并核对派工里有承接它的实际批次｜读到：实现报告说某分支依赖另一片或共享组件扩展才能完整，先降级实现并登记占位；写错：占位登记写着推给某个后续批次（如「组件完整化」批次），派工计划里没有这个批次的实际派工；报告没把它标成阻塞项、没写必须的派工
