# 点击、输入与控件

源端有 setOnClickListener、Compose clickable、EditText / TextField、CheckBox、Switch、SeekBar、ProgressBar、OnTouchListener、onKeyDown，目标端有 .onClick、TextInput、Checkbox、Toggle、Slider、Progress、.onTouch、手势、.onKeyEvent 时

## 子主题

- [点击](click/index.md)（23 条）：源端有 android:onClick、setOnClickListener、数据绑定的 android:onClick="@{…}"、Compose Modifier.clickable，目标端有 .onClick、它挂在哪一层和点击前的门控时
- [选择、开关与进度控件](controls/index.md)（38 条）：源端有 CheckBox、RadioButton、Switch、SeekBar、Compose Slider、按状态切图的 ImageButton、ProgressBar，目标端有 Checkbox、Radio、Toggle、Slider、Progress 和选中、加载状态时
- [输入框与软键盘](text/index.md)（56 条）：源端有 EditText、SearchView、Compose TextField、android:inputType / maxLength / textCursorDrawable、windowSoftInputMode，目标端有 TextInput、TextArea、Search、caretColor、inputFilter、获焦和键盘避让时
- [触摸、手势与按键](touch/index.md)（24 条）：源端有 OnTouchListener / onTouchEvent、GestureDetector、跟手拖动、onKeyDown / dispatchKeyEvent，目标端有 .onTouch、PanGesture、parallelGesture、.onKeyEvent 时
