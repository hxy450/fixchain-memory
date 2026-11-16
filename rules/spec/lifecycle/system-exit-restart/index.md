# System.exit 一类的应用「重启」

agent 会看到什么：读到源方法体是 System.exit(0)、Runtime.exit 或 Process.killProcess、注释写「full app restart」，调用点在通知点击、语言切换、数据恢复之后，或同一个源方法被几份规格引用；规格的服务层契约写「忠实迁移 = 退出应用（terminateSelf），不附加重启」，source-notes 没登记它和源码注释的差异

## 规矩

- rule-face0047d8aa｜源端用 System.exit 一类调用做「重启」时，规格写明系统重建语义，目标等价是 restartApp 加携带状态｜读到：源码里方法体是 System.exit(0)（或 Runtime.exit、Process.killProcess），方法注释写「full app restart」，调用点是通知点击、语言切换、数据重置一类；写错：规格把它写成「System.exit(0) 忠实迁移 = 退出应用（terminateSelf），不附加重启」，或实现映射表里只有 context.terminateSelf()
- rule-3b496b413fde｜同一源方法出现在几份功能规格里时先核对口径，矛盾时按用户可见终态的 AC 修正服务层契约｜读到：同一个源方法（如重启方法）被几份功能规格引用：有的 AC 写「点击通知后应用重启进入主页」，有的写「ApplicationContext 重启」；写错：本份规格的服务层契约写「退出应用（terminateSelf），不附加重启」，与别的规格里描述用户可见终态的 AC 相反
- rule-c06af54d9cc0｜实现时读到源码注释与规格契约相反，要在 source-notes 差异项里登记并上报，不沉默沿用｜读到：源码注释写「Performs a full app restart」，规格的服务层契约却写「退出应用（terminateSelf），不附加重启」；写错：source-notes 的差异项里没有这一条，代码头注释只复述规格的判断（「注释称 full restart 实为退出」）
