# ValueAnimator 改写成的自驱帧循环

agent 会看到什么：读到 ValueAnimator.ofFloat / ObjectAnimator 设 setDuration、addUpdateListener 逐帧写进度并 invalidate()，有没有 setInterpolator；产物里 postFrameCallback 的 FrameCallback 和 pending 去重标志、进度是不是直接取 (now - start) / duration

## 规矩

- rule-a49a3b328835｜用 postFrameCallback 自写帧循环并以待决标志去重时，回调入口第一行先清标志｜读到：源端用 ValueAnimator（0→1、固定时长）加 onAnimationUpdate 逐帧写进度并 invalidate()，或规格写「回调先清标志再绘制」的重绘契约；写错：调度函数里 if (pending) return; pending = true; 再 postFrameCallback(...)，而 FrameCallback 子类的 onFrame 或它转发到的宿主方法里没有 pending = false，续帧被拦下
- rule-db766fd40f52｜ValueAnimator 没设插值器时，帧循环进度套 AccelerateDecelerate 公式｜读到：ValueAnimator.ofFloat / ObjectAnimator 设了 setDuration、addUpdateListener，animatedValue 直接写进绘制用的进度字段，全文没有 setInterpolator；写错：自驱帧循环里进度直接取 Math.min(1, (now - start) / duration) 这个时间分数，注释标「线性」，没有套插值函数
