# app/settings

设置项迁移：偏好存储的同步装载与读写时序，偏好键与默认值（同一键按读点的不同缺省值）之外，每个开关的运行期消费方与应用入口；onPreferenceChange 返回值决定的落值时刻与验证补偿；设置保存的副作用（远端、本地缓存、刷新事件）与切换即持久化界面状态的恢复，应用内语言切换的即时生效；应用壳下传的页面显示设置：占位初值来源与壳层一次计算的派生判定；只改会话字段的选项不建偏好键，以 null 区分缺键而空串合法时的存在性判断

[上一级](../index.md)

## 本级经验

- [SharedPreferences 迁移保留同步时序：onCreate 用 getPreferencesSync 装载，读写走 Sync 接口、异步 flush](lesson-9fa98065e5de983b7c01.lesson.md)
  - 时机：基础层偏好迁移阶段，设计偏好存储封装的初始化与读写时序时；派工者为该任务写验收标准时
  - 情境：源端用 SharedPreferences（或其封装库）在 Application.onCreate 构建，之后任意读都等待载入完成；目标改用 @ohos.data.preferences，派工或封装设想“异步载入 + 内存缓存 + 写队列”，载入完成前的读返回调用方默认值。
- [onPreferenceChange 返回 true 即接受并持久化新值：其中发起的验证按源顺序先落值再补偿，取消不回滚](lesson-8b84279c4ecbeaf26e3e.lesson.md)
  - 时机：设置页实现阶段，把 Preference 的 onPreferenceChange 监听（含其中发起的验密、确认弹窗）翻译成目标开关回调时；规格提取阶段描述这类联动流程时
  - 情境：源端在 onPreferenceChange 里发起异步验证后立即 return true，验证成功的回调只做补偿动作（如再次 setChecked 同值），取消没有回滚分支；目标用受控 Toggle 与回调实现，写者倾向“先回滚、验证成功才落值”。
- [同一偏好键在不同读点用不同缺省值时按读点保留，不收敛成键常量上的单一默认](lesson-0c355313bc2e9e0cb7ab.lesson.md)
  - 时机：偏好键表与访问器设计阶段，以及页面实现中修改某个偏好读取的缺省值时
  - 情境：源端同一键在不同调用点以不同 defValue 读取（如过滤逻辑读 false、菜单显隐读 true）；目标准备在键常量或单一访问器里集中定义一个默认值，键表或规格摘要只写了一个缺省。
- [源端 SharedPreferences.Editor 累积 put 后一次 commit 的流程（恢复、导入），目标先暂存、全部校验通过后再 put 并 flush：preferences.putSync 立即改共享实例，中途失败不能留下部分写入](lesson-24bc4929b771a9a33ef4.lesson.md)
  - 时机：数据层实现阶段，迁移 Editor 批量写入后 commit/apply 的恢复或导入流程时
  - 情境：源端遍历输入逐键 editor.putX，遇到未知键或格式错误时抛出，末尾才 commit；目标准备逐键 putSync 到共享 preferences 实例。
  - 例外：本条只管同一个 Editor 累积、末尾一次提交的流程：源端每个键各自 edit()…apply()/commit() 时，失败前已提交的键在源端本来就留着，目标逐键 put 是对的，不改成暂存。源端在这个 Editor 上调了 clear() 的（恢复等于整体替换），暂存校验通过后先 clear 再 put，不论源端 clear 写在 put 之前还是之后，也不漏掉这一步只做覆盖写。
- [源端用 getString(key, null) 区分缺键、空串又是合法值时，偏好封装提供 has 判断，不以空串作缺省哨兵](lesson-463f8ca86a0d06dd5022.lesson.md)
  - 时机：数据层与设置实现阶段，迁移以 null 默认值区分“键不存在”的偏好读取（历史列表、可选路径等）时
  - 情境：源端 SharedPreferences.getString(key, null) 只把缺键当作不存在，空串是合法值（例如表示根目录或默认位置）；目标偏好封装只提供 get(key, def)，没有存在性判断。
- [源端选项只经 setter 改会话字段、不写持久偏好时，目标落成会话态并接到读取它的流程，不新建偏好键](lesson-372d4a11039d986a573d.lesson.md)
  - 时机：规格提取阶段整理“读写偏好键”清单，以及实现与接线阶段为弹层或设置选项确定写入目标（持久偏好还是会话状态）时
  - 情境：源端选项回调里写偏好的 editor.putString 被注释或不存在，只调用应用接口的 setXxx 改会话字段，业务流程经对应 getter 读取；目标的偏好键表、会话状态与应用接口由不同切片产出，规格可能把该项列入持久键或引用并不包含它的权威键表，实现者在目标端找不到对应的会话 setter。
- [设置页由 addPreferencesFromResource/PreferenceFragment 挂载时，缺持久值的偏好会写入 android:defaultValue：目标在设置页出现时按 XML 顺序为缺键补写默认值并落盘，不只在读取时回退默认](lesson-4283cc343b875489b851.lesson.md)
  - 时机：规格提取与设置页实现阶段，迁移带 android:defaultValue 的 PreferenceScreen XML 时
  - 情境：源设置页由 PreferenceFragment/PreferenceActivity 以 XML 挂载偏好，各项有 defaultValue；目标偏好服务只在读取时回退默认值；偏好文件内容会被备份等流程读取。
  - 例外：不补写的键：XML 里标 android:persistent="false"、没有 key，或应用给偏好另设了 PreferenceDataStore 的项，源端挂载时不写偏好文件，目标也不写。时机要前移的：源端在主界面启动时调 PreferenceManager.setDefaultValues 的，默认值在应用首次启动就写进偏好文件，目标对应在启动流程里补写，而不是等进入设置页。
- [迁移设置开关、设置保存与持久化的界面状态时为每项落实运行期消费方：只调持久化 setter、只写远端设置不算完成](lesson-4d0f0176b3d09c33f1eb.lesson.md)
  - 时机：功能接线阶段实现设置页开关与偏好仓库，或页面转换遇到按偏好切换的渲染与行为分支时；迁移设置页的保存逻辑，或切换即持久化的界面状态（如首页视图位置）时
  - 情境：源端设置用 DataStore/SharedPreferences 持久化，并被主题、计时器、反馈等运行期代码实时读取；目标端的设置页、偏好仓库、主题状态和消费页面由不同任务编写，靠占位登记传递“持久化并立即生效”的契约。也包括源端设置保存除远端同步外还更新本地配置缓存并发刷新事件（如排序设置保存后各列表按新配置排序），目标只写远端设置；以及源端切换视图即写偏好、启动时读取恢复，目标只改内存状态。也包括应用内语言选择只调用持久化的偏好语言接口，而规格要求保存后立即切换。
  - 例外：主题设置里有“跟随系统”一项时，目标对应设成未设置颜色模式（COLOR_MODE_NOT_SET），由系统深浅色决定，不在启动时读一次系统当前模式再固定成深色或浅色；只有用户选了明确的深色、浅色才设成对应模式。源端某项设置本来只在启动时读一次（改完要重启才生效）时，目标照源端的生效时机，不必为它补即时生效。
- [页面显示设置由应用壳下传时：占位初值取源端默认值常量而非 @Preview 实参，派生判定（如省流是否生效）在壳层算一次共享，多值枚举不按 0/1 判](lesson-0670bec94637c8ff8c28.lesson.md)
  - 时机：页面转换与功能接线阶段，为由应用壳下传的显示设置确定初值、读取方式与激活判定时；数据模型阶段为设置列写类型与注释时
  - 情境：Android 页面的显示设置是 Composable 必填参数，由主 Activity 从设置存储读取并下传（@Preview 里另有一组示例实参）；省流一类设置是 Auto/Always/Never 三值 ordinal 枚举，激活结果由应用壳统一计算一次；目标页面改为各自读取设置存储。
