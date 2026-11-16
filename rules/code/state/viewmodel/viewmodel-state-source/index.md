# ViewModel 发布的数据在目标端的来源和赋值时机

agent 会看到什么：读到源 ViewModel 用 LiveData / MutableLiveData 发布页面数据（选中项变化时的附带查询、单独持久化的一项、text 前缀的格式化字段、WorkInfo 聚合、初始化时同步写入、只在 success 里写值），Fragment observe 后绑定控件；产物里目标 VM / gateway 的字段从哪赋值、什么时候赋值（await 之前或之后、catch 里置 0、map.delete）

## 通用查法

### 目标页的状态字段，按源 ViewModel 写对应 LiveData 的位置定赋值来源和时机

审的是：代码
触发（任一种）：
- 读到：源 ViewModel 用 LiveData / MutableLiveData 发布页面数据（setValue、postValue 或 .value = …），Fragment / Activity 里 observe 后绑定控件；写错的样子：目标 ViewModel / gateway 里被 build 读取的 @Local / @Trace 字段没有赋值处、只在部分分支赋值，或赋值的时机、条件和源端不同
适用范围：把源 ViewModel 的 LiveData 状态迁成 ArkUI 状态字段时，核对每个字段的赋值来源和时机
做法：
- 列出目标组件读的每个状态字段，在源 ViewModel 里找到写对应 LiveData 的每一处（setValue / postValue / .value =），记下它在哪个回调里写（初始化、选中项变化、请求的 success 回调）、写的是什么
- 目标在同样的时机、同样的条件下给字段赋值，源端不写的情形（如失败分支）目标也不写；源端写入点在目标里找不到对应赋值的补上，不靠默认值撑着
针对本应用要查的：
- 源端写这个 LiveData 的位置、时机和值：源工程里该页面的 ViewModel（Java 或 Kotlin）：按 LiveData 字段名搜 setValue(、postValue(、.value =，再看 Fragment / Activity 里对应的 observe 和它绑定的控件；每个写入点记下所在的回调（初始化、选中项回调、请求的 success / failure）和写入的表达式，照着在目标 ViewModel / gateway 的对应时机赋值
来源：3 张卡，2 个应用
- case-2906493a39c662495a11（app_hnaccurateweather_live_android）：做法第 1 步 ← 建议 2
- case-3eb3514a903386524e37（骑行记录）：做法第 2 步 ← 建议 5
- case-9ccc879e5d89039f29f4（app_hnaccurateweather_live_android）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1

## 规矩

- rule-05f1f1b391f4｜组件用 available 一类开关条件渲染可选区块时，开关要有真实赋值来源，迁入源端选中项变化时的查询｜读到：源端 ViewModel 在选中项变化时触发附带查询（如 `setSelectDay(index)` → 按今天的 id 加 `index - 1` 查当日数据）写进 `LiveData`，Fragment 里 `observe` 后绑定几个 `TextView`；写错：目标组件用 `if` 加区块数据的 `.available` 条件渲染该区块，而 gateway / ViewModel 只映射了别的字段，这个数据对象一直是默认值 `available=false`，区块永不显示
- rule-d767eb051bc5｜源 ViewModel 把单独持久化的一项和列表合并展示时，目标 load() 同时读它，删除和设置走它自己的路径｜读到：源 `ViewModel` 的加载方法把单独持久化的一项（如定位得到的当前城市）和收藏列表一起交给 `LiveData` 展示，并为这一项另有删除、设为推送的方法；写错：目标 VM 的 `load()` 只读收藏列表，这一项只在主动触发时才赋值；对它的删除沿用列表的 delete，设置只在列表里查找，查不到就抛错
- rule-37bb2425c0c2｜转写 "${x}…" 拼接时先读 x 的定义，text 前缀的字符串字段不映射到原始数值｜读到：源端 observe 一个返回 LiveData<String> 的 text 前缀字段，拼成 "${x}…" 文案；写错：目标页面直接把状态里的原始数值拼进模板字符串（`${this.store.<数值字段>}…`），没有经过格式化，显示成裸秒数
- rule-882939e75ec3｜替代源端 WorkInfo 聚合时，作业结束写成 COMPLETED 留在状态表里，不删 key｜读到：源端宿主观察 WorkManager 的 WorkInfo 列表（LiveData），把作业状态映射成 url→状态 表并 postSticky 粘性广播；查询面专门排除完成态，订阅方遍历事件里的全部 url 再过滤；写错：目标下载服务的作业收尾写成 map.delete(url) 后再发事件；查询方法在判断 COMPLETED，但全文件没有写入 COMPLETED 的地方
- rule-d4db6c33aa1e｜源端初始化时同步写入的输入状态，在目标初始化方法的第一个 await 之前赋值｜读到：源 Activity / Fragment 初始化时同步写 viewModel.keyWord.value = … 和 EditText.setText(…)，搜索动作读取输入框当前文本；写错：ViewModel 的初始化方法先 await 存储或 SDK 的绑定调用，之后才给 TextInput 双向绑定的字段（关键词、清除按钮可见性）赋初值；页面在 aboutToAppear / onReady 里以 void 调用它、不等待
- rule-cbcce07a08ad｜首屏由本地登录态、XML 静态内容、配置开关和远端接口组成时，按来源分开加载，静态内容同步首帧渲染｜读到：源 Fragment 的 onResume 同步读本地登录态；布局 XML 里提醒区默认 visible、带静态 android:text 和图标，之后才被远端请求覆盖；另有配置开关和远端接口；写错：目标组件把账户态、开关、提醒和远端数据全放进一个快照，只留一个异步加载钩子（一个 `FWD-REF`）；提醒默认 []，空时只显示加载或「错误 + 重试」
- rule-ede6186546d3｜计数类状态请求失败时保留旧值并显示失败可重试，不在 catch 里置 0｜读到：源 `ViewModel` 只在 success 回调里写 `LiveData`，失败走错误处理、不覆盖旧值；规格写「失败可见、可重试、不伪造数据」；写错：目标 VM 的 `catch` 里把计数写成 `0`（如 `this.count = 0`），界面显示「0 天」一类的假数据
- rule-e7099487123a｜从安卓 ViewModel 迁移时带上驱动界面的常量和状态，Tab 顺序按源数组，不用内部 id 当标题｜读到：源 ViewModel 里有驱动界面的常量和状态：Tab 文案数组 arrayOf(...) 及下标到类型的映射、选中项下标、距离等格式化函数；列表项字段来自 item 布局；写错：目标 Tab 顺序照规格 AC 或枚举类型的列举顺序写；列表卡片用内部 id 当主标题、少了 item 布局里的字段；目标 ViewModel 没有选中下标和格式化好的文本，页面显示不出选中态
