# 目标页的状态字段，按源 ViewModel 写对应 LiveData 的位置定赋值来源和时机

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
