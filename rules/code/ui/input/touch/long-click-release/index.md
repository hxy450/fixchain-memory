# 长按监听（setOnLongClickListener）和松手回调

agent 会看到什么：读到源端同一个 View 既有 setOnClickListener 又有 setOnLongClickListener，触摸监听在 MotionEvent.ACTION_UP 时停止长按动作；产物里组件只挂了 .onClick(...)，没有 LongPressGesture 和松手时的 onActionEnd

## 规矩

- rule-5a8740b9eb44｜源端快门有点击和长按两条入口时，目标快门同时挂 onClick 和 LongPressGesture 及松手回调｜读到：源端快门 View 同时有 setOnClickListener 和 setOnLongClickListener，触摸监听里 MotionEvent.ACTION_UP 时停止连拍；写错：目标快门组件只挂了 .onClick(...)，没有 LongPressGesture，也没有松手停止的回调
