# 权限插件换成 OHOS 同包分支时，逐组核对应用实际请求的权限映射，不以构建通过放行

审的是：计划与派工
触发（任一种）：
- 读到：应用 Dart 代码经 permission_handler 请求 Android 专用权限组（Permission.storage、Permission.photos 等），并用授予结果门控下载、保存等核心流程；写错的样子：插件替代记录里 permission_handler 只写成同包同 API 分支（F2）的 dependency_overrides，solution JSON 的 methods 为空，以注册器加 HAP 构建标成 build_verified，没有逐组写权限映射
适用范围：插件替代阶段为权限类 Flutter 插件选 OHOS 同包分支、并据此判定应用 Dart 可保持冻结时
做法：
- 先搜应用实际请求的每个 Permission.xxx 及其门控流程，逐组查看 OHOS 分支的权限映射和状态判定（分组到 ohos.permission 列表的映射、列表为空时返回的状态），在 solution JSON 的 methods 里逐组记为 implemented 或 unsupported
- 映射为空并判为拒绝的组不以 build_verified 放行，作为必须修改点交给 dart-adapted
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- permission_handler 的 OHOS 分支把 storage 组映射为空权限列表，状态判定落到 DENIED：同 API 能编译不等于权限语义等价，storage 组在 OHOS 上一请求就被拒（出处：卡里修好并验证过）
针对本应用要查的：
- 每个权限组在 OHOS 分支上的映射和状态：pubspec.yaml 的 dependency_overrides 指向的 OHOS 插件分支源码里，把权限组映射到 ohos.permission 列表的工具类，以及判定授予状态的那段；逐组读出映射到的 ohos.permission 列表；列表为空时看返回的状态（如 DENIED），据此记 implemented 或 unsupported
来源：1 张卡，1 个应用
- case-3cc99a6c512ab85ed874（app-photo-shop-flutter）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1、诊断；取值 1 ← 诊断
