# 窗口亮度的读取和手势调节

agent 会看到什么：读到源手势在 ACTION_DOWN 读 window.attributes.screenBrightness、等于 BRIGHTNESS_OVERRIDE_NONE 时回退 Settings.System.SCREEN_BRIGHTNESS；产物里亮度基线写死 0.5、注释称 window 无亮度读取 API，只调了 setWindowBrightness

## 规矩

- rule-4ca9bb356d1e｜亮度手势的首拖基线读当前窗口亮度，读不到回退系统设置，不写死 0.5｜读到：源手势在 ACTION_DOWN 读 window.attributes.screenBrightness，等于 BRIGHTNESS_OVERRIDE_NONE 时回退 min(Settings.System.SCREEN_BRIGHTNESS, 255) / 255，ACTION_MOVE 再按位移增量写回窗口；写错：目标手势首调把亮度基线写死为 0.5，字段注释或 TODO 写「window 无亮度读取 API」，只用了 setWindowBrightness 写入
- rule-13c11b40b1ad｜前屏补光开启时同时提亮窗口和打开全屏白色覆盖层，拍照结束等路径两者一起复位｜写错：VM 的补光处理只调 setWindowBrightness 提亮，预览门面接口没有开白色覆盖层和结束拍照的转发方法，页面也没绑定；拍照结束时只恢复亮度
