# V2 页面里的自定义弹窗

agent 会看到什么：@ComponentV2 页面要弹自定义弹窗：产物里的 CustomDialogController、openCustomDialog 的 builder 或 ComponentContent，以及弹窗组件自己 new 的 ViewModel

## 规矩

- rule-2cec983ce40e｜@ComponentV2 页面不用 CustomDialogController 套 V2 struct 做弹窗｜读到：项目锁定 V2，页面写 `@ComponentV2`；规格转换决策给的是「CustomDialog（UIContext 形）或 bindSheet」或「@CustomDialog」；写错：页面字段初始化 `new CustomDialogController({ builder: ... })`，builder 是 `@ComponentV2` struct；打开页面报 TypeError: class constructor cannot called without 'new'
- rule-6cd239070ebd｜组件外函数开自定义弹窗时用 ComponentContent，不在 builder 闭包里调全局 @Builder｜读到：安卓 BottomSheetDialog / DialogFragment 类弹窗要被多个入口复用；写错：导出的普通函数（只持有 UIContext）里 openCustomDialog({ builder: () => { 全局Builder(...) } })，闭包不属于组件实例，直接调模块级 @Builder function 创建 @ComponentV2 组件
- rule-695d07f7827b｜弹窗和宿主各持一个 ViewModel 时，弹窗改的持久化偏好要同步到宿主的状态来源｜读到：弹窗组件里 `new` 了自己的 ViewModel 实例，改偏好后经它持久化，再只用回调通知宿主；宿主刷新时把自己 ViewModel 的字段回填到 @Local；写错：宿主回调里只改 @Local，删掉了调用宿主 ViewModel 的 setter；关闭后刷新用旧快照覆盖 @Local，下次打开把旧值当初始值传给弹窗
