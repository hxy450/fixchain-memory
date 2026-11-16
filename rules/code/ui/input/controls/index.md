# 选择、开关与进度控件

源端有 CheckBox、RadioButton、Switch、SeekBar、Compose Slider、按状态切图的 ImageButton、ProgressBar，目标端有 Checkbox、Radio、Toggle、Slider、Progress 和选中、加载状态时

## 触发族

- [选项的选中、取消选中和按选中决定的按钮可用](selection-logic/index.md)（4 条）：读到 ViewModel 的选择方法（同值再点置 null）、默认选中的回退、Compose Button(enabled = …) 按选中数决定可用、共享 @Composable 弹层内部的点击和步进；产物里对应的 onClick、.enabled(...) 和子类覆写的默认值方法
- [ImageButton 一类图标按钮和开关的状态切换与获焦](icon-buttons-toggles/index.md)（9 条）：读到源端 ImageButton / ImageView 按状态 setImageResource、setTextColor 切换图标和文字颜色（按选中数、播放暂停、各开关自己的状态），或布局里的 <ImageButton> / <Button>；产物里 Image 的资源怎么选（两个独立 if）、开关行共用 @Builder 传 boolean 值参、复用开关组件的 @Event 回调、Image(...).onClick 没有 .focusable(true)
- [按偏好二选一的 Compose 进度组件](progress-variant/index.md)（2 条）：读到 Compose 按布尔偏好在 CircularWavyProgressIndicator 和 CircularProgressIndicator 之间切换；产物里只写了一种 Progress({ type: ProgressType.Ring })，没有另一分支、占位登记或 decision_gaps
- [CheckBox、RadioButton 和单选列表行](checkbox-radio/index.md)（4 条）：读到带 android:text 的 CheckBox / RadioButton、RadioGroup，或 setSingleChoiceItems / ListPreference 的单选列表；产物里 Checkbox / Radio 加 Text 的行的可点范围和选中样式
- [勾选控件和勾选状态](checkbox/index.md)（7 条）：源端 CheckBox、checkable 菜单项、实现 Checkable 的自定义 View 和它们的 setChecked / postDelayed；产物里 Checkbox 的 shape、select、onChange，MenuItem 的 selectIcon 和勾选后的延时
- [平台 SeekBar、Switch 控件迁 Slider、Toggle](seekbar-switch-controls/index.md)（5 条）：读到布局里的 <SeekBar>、Switch、SwitchPreference（常没写 style、android:thumb、android:track）和 setOnSeekBarChangeListener；交回的是只改了颜色的 Slider / Toggle、Slider.onChange 当等价，或 blockSize 传了数字
- [Compose 的 Slider](compose-slider/index.md)（2 条）：读过的 Compose 源码里有 Slider（valueRange、steps、SliderDefaults.colors）；交回的代码里 ArkUI Slider 的 step 和 thumb、轨道、刻度的画法
- [控制进度显示的加载状态](loading-flag-reset/index.md)（1 条）：读到源码先 progressBar.setVisibility(View.VISIBLE) 显示进度，再调用遇到空查询等情况会提前 return 的方法；产物里控制进度显示的布尔 @Local 置 true 之后，某个分支直接 return、没有复位为 false
- [Compose 的不定进度条](compose-indeterminate-progress/index.md)（1 条）：读到 Compose 里没传 progress 的 LinearProgressIndicator()（不定进度、持续动画），可能带 Modifier.zIndex 叠在内容上；产物里定值的 Progress({ value, type: ProgressType.Linear })、圆形 LoadingProgress，或放进 Column 流里把内容往下推的进度条
- [按值表索引的 SeekBar 进度](seekbar-value-table/index.md)（2 条）：读到源端先建刻度值表，再 SeekBar.setMax(values.size() - 1)、setProgress(索引)，步进按索引 ± 1 移动；产物里 Slider 的 max、value 由谁赋值，步进函数改的是索引还是偏好值
- [Compose 的 CircularProgressIndicator](compose-progress-indicator/index.md)（1 条）：读过的 Compose 源里有 CircularProgressIndicator()（传不传 progress，带 Modifier.size、strokeWidth、color）；交回的代码里写成 LoadingProgress、Progress({ type: ProgressType.Ring }) 还是自绘，尺寸、描边和颜色是否照源端
