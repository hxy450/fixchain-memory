# BuildConfig 的构建字段（DEBUG、VERSION_NAME、VERSION_CODE）

agent 会看到什么：读到源端条件或页面用 BuildConfig.DEBUG、BuildConfig.VERSION_NAME / VERSION_CODE；交回的表达式删掉了 DEBUG 腿、没有 BuildProfile.DEBUG，或版本号抄成了页面常量

## 规矩

- rule-69c6e59cd235｜源端条件里的 BuildConfig.DEBUG 腿写成 BuildProfile.DEBUG，不以无等价为由删掉｜读到：源端显隐条件含 BuildConfig.DEBUG（如 BuildConfig.DEBUG || 某开关）；写错：目标端表达式只剩另一腿，没有 BuildProfile.DEBUG；注释写「DEBUG 腿无 HMOS 运行期等价」「无构建标志基建」「按 release 语义」
- rule-8ef92c41b13c｜源端用 BuildConfig.VERSION_NAME/CODE 时，目标从应用包信息读，不抄成页面常量｜读到：源端页面用 BuildConfig.VERSION_NAME 显示版本，或用 BuildConfig.VERSION_CODE 比较更新提示；写错：页面里出现与 app.json5 的 versionName / versionCode 相同的字面量（模块常量，或 aboutToAppear 里的赋值）
- rule-15a13d1df2c2｜源码有 debug/release 构建分支时，目标按 appProvisionType 判两支，不写「不迁移」｜读到：源方法里有按 BuildConfig.DEBUG 判构建形态的分支（如 debug 构建直接切换、release 构建走渐显动画）；写错：目标只留一支（如恒 animateTo），注释写「debug 分支无构建形态对等，不迁移」
