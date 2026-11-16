# Activity 的屏幕方向声明与运行时切换

agent 会看到什么：读到 AndroidManifest.xml 的 android:screenOrientation 或运行时 setRequestedOrientation；交回的页面没有 setPreferredOrientation，或进入时切了方向、离开和返回时不恢复

## 规矩

- rule-6061f45fd863｜源 activity 声明 sensorLandscape 时，页面进入设横屏方向、离开恢复｜读到：AndroidManifest.xml 的 <activity> 有 android:screenOrientation="sensorLandscape"；写错：对应页面没有调 setPreferredOrientation，进入后仍是竖屏；或设了横屏但离开时不恢复
- rule-c6f38e82a0f8｜横屏可触发的「另起 Activity」改成同窗口 push 时，跳转前切目标方向、返回后恢复｜读到：页面运行时用 setRequestedOrientation 切横屏，横屏界面上的入口调 startActivity 或 login(activity) 这类另起 Activity 的拦截；写错：拦截直接用 NavPathStack 的 push 把按竖屏设计的页面推进同一窗口，前后都没有 setPreferredOrientation，返回后也不恢复原方向
