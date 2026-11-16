# 路由或弹窗核查清单缺源端 AlertDialog.Builder 弹窗时，回源文件补查并补进清单

审的是：计划与派工
触发（任一种）：
- 读到：源控制器里有 AlertDialog.Builder 构造的弹窗、Settings.ACTION_APPLICATION_DETAILS_SETTINGS 跳转，或多个失败分支各有不同 UI；写错的样子：路由核查清单、fix-plan 只列了 MessageDialog.show、startActivity 抽出来的边（失败弹窗、登录跳转），AlertDialog.Builder 构造的弹窗和它的“去设置”跳转不在清单里
适用范围：按路由或弹窗核查清单派工、移植源端控制器流程时
做法：
- 清单里没有某个弹窗时，到源文件里补查 AlertDialog.Builder、Settings.ACTION_APPLICATION_DETAILS_SETTINGS 等调用；把源方法的每个失败分支和对应 UI 各列成一条清单项再派工
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Settings.ACTION_APPLICATION_DETAILS_SETTINGS：显示某个应用的详情页：源文件里搜到它，说明有一条“去设置”的跳转边（出处：android.provider.Settings#ACTION_APPLICATION_DETAILS_SETTINGS）
来源：1 张卡，1 个应用
- case-845435c8343c4c012e1f（记得日历）：做法第 1 步 ← 建议 3、建议 1
