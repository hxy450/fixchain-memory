"""Recall worker prompts, answer parsing and key-slot environment for recall_hook.py.

Extracted verbatim from a2h-replay-bench harness/bench.py (where the same recall arms are evaluated); keep the two
in step when a recall method changes. KEYS: slot csv (slot,api_key,base_url), from RECALL_KEYS or BENCH_KEYS;
recall_hook.py install records the resolved path in its config, so the hook does not depend on the environment.
"""
from __future__ import annotations

import csv
import json
import os
from pathlib import Path
import re

KEYS = Path(os.environ.get("RECALL_KEYS") or os.environ.get("BENCH_KEYS") or "glm-keys.csv")

INJECT_DIGEST = ("首次明确写入前的经验提示，本次修改尚未执行（不是用户拒绝，无需询问用户）。"
                 "以下是从团队经验库查到、与你接下来整个任务相关的历史迁移经验，每条一行：经验标题 → 对你这次任务的提醒，"
                 "括号里是经验正文的路径，需要细节时自己读。请结合当前源码与规格判断是否适用；"
                 "必要时调整这次待写内容后再提交，不适用就直接继续：\n\n{lessons}")
RECALL_HEAD = ("【暂停迁移】以上是你到目前为止的工作过程。你下一步准备做下面这次写入，但在真正写之前，"
               "你现在的工作不是迁移，而是基于你对这个任务的全部理解，在团队经验库里查找{goal}的历史经验。\n\n"
               "## 你准备做的写入\n{pending}\n\n")
GOAL_TASK = "能防止你接下来的工作出错（经验只在这里查这一次，之后的全部写入都靠这次的结果）"
RECALL_GOAL = {"beam2": "能防止这次写入出错", "task": GOAL_TASK}
# beam2 = memeval/recall53.py PROMPTS["beam2"] (steps verbatim); task = the same steps with the inventory over the whole task
RECALL_STEPS = {
    "beam2": ("经验库根索引：{root}/index.md。请严格按以下步骤：\n"
              "1. 读根索引，以及它列出的每一个顶层分支的 index.md（全部都读）。\n"
              "2. 写法盘点：逐项列出（待写内容里，如果有；否则任务里预计要用到的）每一种组件、修饰符/属性、API 调用、事件回调、"
              "生命周期与数据流写法，并写出它对应的源端写法，格式「源端写法 → 目标写法」。至少 12 项。"
              "特别要包括逐属性机械直译、你觉得理所当然的地方（尺寸与边距、默认值、回调时机、平台判定等），它们最容易在不知不觉中出错。\n"
              "3. 把盘点项按机制归组（如布局尺寸、事件与状态、弹层、平台能力、数据与状态模型），每组至少打开 1 个最对口的叶子主题 index.md，"
              "整体至少 6 个不同的叶子主题；在索引里逐条对照「时机/情境」。\n"
              "4. 至少读 6 条经验正文，优先读能对上某个盘点项的。\n"
              "5. 对每条读过的经验，对照盘点项判断是否适用：适用就说明会改变哪一项写法。\n"
              "6. 登记移交、写后自检、占位规则这类通用流程经验视为已知，除非它会改变某一项具体写法，否则不要返回。"
              "最后只返回会改变具体写法的经验。"),
    "task": ("经验库根索引：{root}/index.md。请严格按以下步骤：\n"
             "1. 读根索引，以及它列出的每一个顶层分支的 index.md（全部都读）。\n"
             "2. 写法盘点：盘点范围是你接下来要完成的整个任务，这次待写内容只是其中第一步。逐项列出整个任务会写到的组件、修饰符/属性、"
             "API 调用、事件回调、生命周期与数据流写法、平台配置与资源，以及规格或决策里要定下的跨栈映射，并写出对应的源端写法，"
             "格式「源端写法 → 目标写法」。至少 20 项。特别要包括逐属性机械直译、你觉得理所当然的地方（尺寸与单位、默认值、"
             "回调时机、平台判定、系统设置跟随等），以及源端没写出来、靠平台默认行为的地方，它们最容易在不知不觉中出错。\n"
             "3. 把盘点项按机制归组（如布局尺寸、绘制与单位、事件与输入、弹层、生命周期、平台能力与配置、资源、数据与状态模型），"
             "每组至少打开 1 个最对口的叶子主题 index.md，整体至少 8 个不同的叶子主题；在索引里逐条对照「时机/情境」。\n"
             "4. 至少读 8 条经验正文，优先读能对上某个盘点项的。\n"
             "5. 对每条读过的经验，对照盘点项判断是否适用：适用就说明会改变哪一项写法。\n"
             "6. 登记移交、写后自检、占位规则这类通用流程经验视为已知，除非它会改变某一项具体写法，否则不要返回。"
             "最后只返回会改变具体写法的经验。"),
}
OUT_CAP8 = ("\n\n最后一条消息只输出一个 JSON 对象，不要任何其他文字或代码块标记：\n"
            '{"lessons": [{"id": "lesson-…", "applies": true, "change": "会改变哪一处写法（≤40字）"}], '
            '"decisions": ["你盘点出的关键写法，每条≤40字"]}\n'
            "lessons 只列你判断适用、会改变做法的经验，按重要性排序，最多 8 条；没有就给空数组。")
OUT_ALL = ("\n\n最后一条消息只输出一个 JSON 对象，不要任何其他文字或代码块标记：\n"
           '{"lessons": [{"id": "lesson-…", "applies": true, "change": "给接下来的你自己的提醒：什么情况下、怎么写（≤60字）"}], '
           '"decisions": ["你盘点出的关键写法，每条≤40字"]}\n'
           "lessons 列出你判断适用、会改变某一处做法的全部经验，按重要性排序，不设条数上限；没有就给空数组。")
RECALL_OUT = {"beam2": OUT_CAP8, "task": OUT_CAP8, "nocap": OUT_ALL}
# nocap = the task steps with every applicable lesson returned (the 8-lesson cap crowded out what the worker had read)
RECALL_GOAL["nocap"] = GOAL_TASK
RECALL_STEPS["nocap"] = RECALL_STEPS["task"]

# sweep family (developed in harness/recall_lab.py): inventory from the source side, then the library's own subtopic
# lists as a checklist (fixes topics the agent's inventory never pointed at); every applicable lesson returned
SWEEP = ("经验库根索引：{root}/index.md。请严格按以下步骤：\n"
         "1. 读根索引，以及它列出的每一个顶层分支的 index.md（全部都读）。\n"
         "2. 任务盘点（源端视角）：盘点范围是你接下来要完成的整个任务，这次待写内容只是其中第一步。逐项列出整个任务要处理的源端"
         "行为与写法：组件与属性、API 调用、事件与回调、生命周期与数据流、平台配置与资源，以及规格或决策里要定下的跨栈映射。"
         "每项只写源端写法和它在源端的效果，先不要写目标写法——目标写法查完经验再定。至少 20 项。"
         "必须包括源端没写出来、靠平台默认行为实现的效果，它们最容易漏。\n"
         "3. 子主题逐项筛查：把第 1 步读到的各分支 index 里列出的子主题清单当作检查表，逐个判断你的任务会不会碰到它"
         "（对照盘点项，也对照源端靠平台默认行为的地方），写出「子主题 → 碰到/碰不到」。碰到的都打开它的 index.md；"
         "打开的子主题若还列着下级子主题，对下级同样逐个判断。在打开的索引里逐条对照「时机/情境」。\n"
         "4. 时机/情境对得上的经验都读正文，不设上限，至少 8 条。\n"
         "5. 对每条读过的经验，对照盘点项判断是否适用：适用就说明会改变哪一项写法。\n"
         "6. 登记移交、写后自检、占位规则这类通用流程经验视为已知，除非它会改变某一项具体写法，否则不要返回。"
         "最后只返回会改变具体写法的经验。")

# sweep2 = sweep with a stricter return filter: one lesson per mechanism, process lessons only when they change a
# concrete item (sweep opened every process subtopic and returned 15 process lessons for main)
SWEEP2 = SWEEP.split("6. ")[0] + (
    "6. 返回前逐条筛：(a) 同一机制有多条经验时只留最贴切的一条；(b) 流程类经验（交接登记、构建、门禁、写后自检、输入读取、占位等）"
    "视为已知，除非它会改变这个任务里某一项具体写法或某一条规格决定，否则不返回；(c) 每条要能指出它改变的是哪一项写法或决定，"
    "指不出就不返回。")

# sweep3 = sweep2, and an opened subtopic's own subtopics are all opened (a nested topic is judged from a one-line
# description two hops away; converter opened ui/navigation but skipped ui/navigation/back-stack in 2 of 3 runs)
SWEEP3 = SWEEP2.replace("打开的子主题若还列着下级子主题，对下级同样逐个判断。",
                        "打开的子主题若还列着下级子主题，下级子主题全部打开，不再逐个判断（下级描述更细，最容易被误判成碰不到）。")
assert SWEEP3 != SWEEP2

for _m, _s in (("sweep", SWEEP), ("sweep2", SWEEP2), ("sweep3", SWEEP3)):
    RECALL_GOAL[_m], RECALL_STEPS[_m], RECALL_OUT[_m] = GOAL_TASK, _s, OUT_ALL

# ---- end of agent: the agent has handed back its report; review what it wrote, then let it fix
# oracle_end  every lesson linked to the unit's cards, full bodies
# review_end  a worker forked from the whole transcript (same model, Read/Glob/Grep) runs the sweep3 checklist against
#             the files the agent actually wrote and returns what to change; injected one line per lesson
END_ARMS = {"oracle_end", "review_end"}
END_HEAD = "【交付前复查】你的报告已送达调用方。"
END_ASK = "请对照源码与规格逐条核对，适用就直接修改相应文件，不适用就跳过；改完后简要说明改了哪些地方。"
END_ORACLE = END_HEAD + "以下是从团队经验库查到、与你这次任务相关的历史迁移经验。" + END_ASK + "\n\n{lessons}"
END_REVIEW = (END_HEAD + "交付前对照团队经验库做了一次复查（在另一个窗口完成），下面是核对你写的文件后认为需要修改的地方，"
              "每条一行：经验标题 → 问题与改法，括号里是经验正文的路径，需要细节时自己读。" + END_ASK + "\n\n{lessons}")
REVIEW_HEAD = ("【暂停】以上是你完成这个任务的全部过程，代码与规格都已写入工程。你现在的工作不是继续迁移，而是交付前复查："
               "在团队经验库里查找与你刚完成的工作相关的历史经验，对照你实际写下的文件，找出需要修改的地方。\n\n")
RECALL_STEPS["review"] = (
    "经验库根索引：{root}/index.md。请严格按以下步骤：\n"
    "1. 读根索引，以及它列出的每一个顶层分支的 index.md（全部都读）。\n"
    "2. 任务盘点（源端视角）：逐项列出这个任务处理过的源端行为与写法：组件与属性、API 调用、事件与回调、生命周期与数据流、"
    "平台配置与资源，以及规格或决策里定下的跨栈映射。每项写源端写法和它在源端的效果，再注明你写成的目标写法在哪个文件。"
    "至少 20 项。必须包括源端没写出来、靠平台默认行为实现的效果，并注明你写的文件里有没有对应处理，它们最容易漏。\n"
    "3. 子主题逐项筛查：把第 1 步读到的各分支 index 里列出的子主题清单当作检查表，逐个判断这个任务有没有碰到它"
    "（对照盘点项，也对照源端靠平台默认行为的地方），写出「子主题 → 碰到/碰不到」。碰到的都打开它的 index.md；"
    "打开的子主题若还列着下级子主题，下级子主题全部打开，不再逐个判断（下级描述更细，最容易被误判成碰不到）。"
    "在打开的索引里逐条对照「时机/情境」。\n"
    "4. 时机/情境对得上的经验都读正文，不设上限，至少 8 条。\n"
    "5. 对每条读过的经验，打开你写的对应文件核对：经验指出的错误写法你有没有写，经验要求的处理你有没有漏。"
    "凭记忆不算核对，要读文件的当前内容。\n"
    "6. 返回前逐条筛：(a) 同一处问题有多条经验时只留最贴切的一条；(b) 流程类经验（交接登记、构建、门禁、写后自检、占位等）"
    "不返回；(c) 只返回核对文件后确认需要修改的地方，要能指出文件和改法。")
RECALL_OUT["review"] = (
    "\n\n最后一条消息只输出一个 JSON 对象，不要任何其他文字或代码块标记：\n"
    '{"lessons": [{"id": "lesson-…", "applies": true, "change": "哪个文件哪一处：现在写成什么 → 应改成什么（≤80字）"}], '
    '"decisions": ["核对过、确认没问题的关键写法，每条≤40字"]}\n'
    "lessons 列出核对后确认需要修改的全部地方，每条挂一条依据经验，按重要性排序，不设条数上限；没有就给空数组。")


def digest_lines(app, res):
    changes = {}
    for x in (res.get("answer") or {}).get("lessons") or []:
        changes[re.sub(r"\.lesson\.md$", "", str(x.get("id", "")).replace("\\", "/").split("/")[-1])] = str(x.get("change", ""))
    out = []
    for lid in res["lessons"]:
        f = next(app.recall_library().rglob(f"{lid}.lesson.md"))
        title = f.read_text(encoding="utf-8").splitlines()[0].lstrip("# ").strip()
        out.append(f"- {title} → {changes.get(lid, '')}（{f.as_posix()}）")
    return "\n".join(out)


def pending_text(fw, rw):
    i = rw(fw["input"])
    target = i.get("file_path") or i.get("notebook_path") or ""
    if fw["tool"] == "Write":
        return f"工具：Write\n文件：{target}\n<pending>\n{i.get('content', '')}\n</pending>"
    if fw["tool"] == "Edit":
        return f"工具：Edit\n文件：{target}\n<old>\n{i.get('old_string', '')}\n</old>\n<new>\n{i.get('new_string', '')}\n</new>"
    body = i.get("command") or json.dumps({k: v for k, v in i.items() if k != "file_path"}, ensure_ascii=False, indent=1)
    head = f"工具：{fw['tool']}\n" + (f"文件：{target}\n" if target else "")
    return f"{head}<pending>\n{body}\n</pending>"


def slot_env(slot, cfg_dir):
    base, token = key(slot)
    env = {k: v for k, v in os.environ.items() if not k.startswith(("ANTHROPIC_", "CLAUDE_CODE_", "CLAUDECODE"))}
    env.update(CLAUDE_CONFIG_DIR=str(cfg_dir), ANTHROPIC_BASE_URL=base, ANTHROPIC_AUTH_TOKEN=token,
               CLAUDE_CODE_DISABLE_UNKNOWN_MODEL_WINDOW_ENFORCEMENT="1", CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC="1",
               DISABLE_AUTOUPDATER="1")
    return env


def topic_catalog(lib):
    """Every topic of the library with its scope line, flat (path — description): lets a worker judge nested topics
    without walking the index tree."""
    out = []
    for f in sorted(lib.rglob("index.md")):
        if f.parent == lib:
            continue
        lines = f.read_text(encoding="utf-8").splitlines()
        desc = next((x.strip() for x in lines[1:8] if x.strip() and not x.startswith(("[", "#"))), "")
        out.append(f"- {f.parent.relative_to(lib).as_posix()} — {desc}")
    return "\n".join(out)


def parse_answer(text):
    """The worker's final JSON; when it is malformed (e.g. unescaped quotes inside a reminder), recover the lesson
    entries one by one, anchored on the closing quote-brace of each entry."""
    m = re.search(r"\{[\s\S]*\}", text or "")
    if not m:
        return {}
    try:
        return json.loads(m.group(0))
    except ValueError:
        items = re.findall(r'\{\s*"id"\s*:\s*"([^"]+)"\s*,\s*"applies"\s*:\s*(true|false)\s*,\s*"change"\s*:\s*"(.*?)"\s*\}'
                           r'(?=\s*[,\]])', m.group(0), re.S)
        return {"lessons": [{"id": i, "applies": a == "true", "change": c} for i, a, c in items], "repaired": True}


def parse_recall(d, lib):
    """Lessons, reads and usage of a finished recall worker (d = its recall dir)."""
    reads, answer = [], {}
    for line in (d / "stream.jsonl").read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            o = json.loads(line)
        except ValueError:
            continue
        if o.get("type") == "assistant":
            for b in (o.get("message") or {}).get("content") or []:
                if isinstance(b, dict) and b.get("type") == "tool_use" and b.get("name") == "Read":
                    reads.append(str((b.get("input") or {}).get("file_path") or "").replace("\\", "/"))
        if o.get("type") == "result" and (o.get("result") or "").strip():   # -p can emit an empty result row first
            answer = parse_answer(o.get("result"))
    known = {f.name[:-len(".lesson.md")] for f in lib.rglob("*.lesson.md")}
    lessons = []
    for x in answer.get("lessons") or []:
        lid = re.sub(r"\.lesson\.md$", "", str(x.get("id", "")).replace("\\", "/").split("/")[-1])
        if x.get("applies", True) and lid in known and lid not in lessons:
            lessons.append(lid)
    return {"usage": usage(d / "stream.jsonl"), "lessons": lessons, "answer": answer,
            "lesson_reads": [r.split("/")[-1][:-len(".lesson.md")] for r in reads if r.endswith(".lesson.md")],
            "index_reads": [r.split("/memory/")[-1] for r in reads if r.endswith("index.md")]}


def key(slot):
    with KEYS.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            if row.get("slot") == slot:
                return row["base_url"].strip(), row["api_key"].strip()
    raise SystemExit(f"no slot {slot}")


def usage(stream):
    tot = {"turns": 0, "input": 0, "cache_read": 0, "output": 0, "rate_limited": 0}
    if not stream.exists():
        return tot
    for line in stream.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            o = json.loads(line)
        except ValueError:
            continue
        if o.get("type") == "assistant":
            u = (o.get("message") or {}).get("usage") or {}
            tot["turns"] += 1
            tot["input"] += u.get("input_tokens", 0)
            tot["cache_read"] += u.get("cache_read_input_tokens", 0)
            tot["output"] += u.get("output_tokens", 0)
        if o.get("type") == "system" and o.get("subtype") == "api_retry" and o.get("error_status") == 429:
            tot["rate_limited"] += 1
        if o.get("type") == "result":   # per-message usage can be empty (GLM); the result rows carry the totals
            u = o.get("usage") or {}
            for k, f in (("billed_input", "input_tokens"), ("billed_cache_read", "cache_read_input_tokens"),
                         ("billed_output", "output_tokens")):
                tot[k] = tot.get(k, 0) + (u.get(f) or 0)
    return tot
