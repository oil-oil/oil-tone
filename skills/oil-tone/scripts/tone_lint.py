#!/usr/bin/env python3
"""Suggest Chinese wording to review in context."""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path


Rule = tuple[re.Pattern[str], str]

WARNING_RULES: tuple[Rule, ...] = (
    (re.compile(r"(?:赋能|撬动|抓手|沉淀价值|价值落地)"), "确认这些词是否说明了具体作用；若没有，直接写动作或结果。"),
    (re.compile(r"(?:原因很简单|真正重要的是|真正的关键是|这不仅仅?是|从更大的角度看)"), "确认领起语是否有助于当前论证；若没有，直接说明事实或判断。"),
    (re.compile(r"(?:在当今|在当前).{0,16}(?:时代|背景|环境)下"), "确认这段背景是否提供了必要信息，否则直接进入具体内容。"),
    (re.compile(r"随着.{0,16}(?:不断|持续)(?:发展|演变|变化)"), "确认这段变化是否与后文存在具体关系。"),
    (re.compile(r"(?:值得注意的是|需要指出的是|毋庸置疑|不可否认的是?)"), "删除没有承担限定或转折作用的固定领起语。"),
    (re.compile(r"(?:标志着|代表着).{0,24}(?:重要|关键)(?:一步|时刻|转折点)"), "改为材料已经确认的动作、变化或结果。"),
    (re.compile(r"为.{1,24}奠定(?:了)?(?:坚实的?)?基础"), "说明具体产生了什么后续条件或结果。"),
    (re.compile(r"(?:彰显|凸显|体现)(?:了)?.{0,20}(?:重要性|意义|价值)"), "确认重要性判断是否有材料支持。"),
    (re.compile(r"(?:业内|行业|专家|观察者)(?:普遍)?(?:认为|指出|表示)"), "写出材料提供的明确来源；没有来源时删除模糊归因。"),
    (re.compile(r"(?:很多|不少|部分)用户(?:认为|指出|表示|反馈)"), "确认用户判断或反馈是否有明确材料依据。"),
    (re.compile(r"(?:有|相关|多项|大量)研究(?:均)?(?:表明|显示|指出)"), "写出材料提供的研究来源；不能自行补充来源。"),
    (re.compile(r"(?:从而确保|进而体现|进一步彰显|反映了更深层次)"), "确认尾句是否有真实因果或材料依据。"),
    (re.compile(r"尽管.{0,24}(?:挑战|困难).{0,24}(?:仍|依然|未来)"), "直接说明已经确认的限制、结果或后续安排。"),
    (re.compile(r"(?:未来可期|迈出(?:了)?(?:至关重要|重要|关键)的一步|开启(?:了)?(?:全新|新的?)篇章)"), "删除通用乐观结尾，说明具体结果或下一步。"),
    (re.compile(r"(?:当然可以|这是一个(?:非常|很)?好的问题|你说得(?:完全)?正确|希望这对(?:你|您)有帮助|如需更多(?:信息|帮助).{0,8}(?:请)?(?:随时)?(?:告诉我|联系我))"), "删除读者成稿中的聊天残留或讨好表达。"),
    (re.compile(r"(?:可能|或许|也许|在一定程度上|在某种程度上).{0,8}(?:可能|或许|也许|在一定程度上|在某种程度上)"), "合并重复限定，保留一个符合事实状态的说法。"),
)


def read_text(name: str) -> str:
    return sys.stdin.read() if name == "-" else Path(name).read_text(encoding="utf-8")


def visible_lines(text: str) -> list[tuple[int, str]]:
    lines: list[tuple[int, str]] = []
    in_fence = False
    in_script = False
    for number, raw in enumerate(text.splitlines(), start=1):
        stripped = raw.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if re.search(r"<(script|style)\b", raw, flags=re.IGNORECASE):
            in_script = True
        if in_script:
            if re.search(r"</(script|style)>", raw, flags=re.IGNORECASE):
                in_script = False
            continue
        without_tags = re.sub(r"<[^>]+>", " ", raw)
        without_code = re.sub(r"`[^`]*`", " ", without_tags)
        visible = html.unescape(re.sub(r"\s+", " ", without_code)).strip()
        if visible:
            lines.append((number, visible))
    return lines


def find_matches(text: str, rules: tuple[Rule, ...]) -> list[tuple[int, str, str]]:
    matches: list[tuple[int, str, str]] = []
    for line_number, line in visible_lines(text):
        for pattern, fix in rules:
            if pattern.search(line):
                matches.append((line_number, line, fix))
    return matches


def find_warnings(text: str) -> list[tuple[int, str, str]]:
    return find_matches(text, WARNING_RULES)


def self_test() -> int:
    warning_bad = "\n".join((
        "在当今快速变化的时代下，团队需要保持敏捷。",
        "随着人工智能技术的不断发展，工具越来越多。",
        "值得注意的是，这项功能已经发布。",
        "这标志着产品迈出了重要一步。",
        "这次更新为后续增长奠定了坚实的基础。",
        "这体现了自动化的重要性。",
        "业内普遍认为，这种方案更可靠。",
        "不少用户反馈，新的设计更自然。",
        "有研究表明，这种方法可以提高效率。",
        "这项改动进一步彰显了产品价值。",
        "尽管面临诸多挑战，团队未来仍将继续前进。",
        "产品完成升级，未来可期。",
        "希望这对你有帮助。",
        "这项政策可能在一定程度上或许会影响结果。",
    ))
    warning_good = "\n".join((
        "2025 年 3 月接口升级后，旧版客户端无法继续登录。",
        "清华大学发布的报告显示，样本中的响应时间缩短了 12%。",
        "产品支持批量处理和离线模式。",
        "这项政策可能影响结果。",
    ))
    warnings = find_warnings(warning_bad)
    warning_lines = {line_number for line_number, _, _ in warnings}
    if (
        warning_lines != set(range(1, len(warning_bad.splitlines()) + 1))
        or find_warnings(warning_good)
    ):
        print("FAIL  tone lint self-test")
        for warning in warnings:
            print(f"      {warning}")
        return 1
    print("PASS  tone lint self-test")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Suggest Chinese wording to review in context.")
    parser.add_argument("files", nargs="*", help="UTF-8 files to scan, or - for stdin")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    if not args.files:
        parser.error("provide one or more files, or use --self-test")
    warned = False
    for name in args.files:
        content = read_text(name)
        for line_number, line, fix in find_warnings(content):
            print(f"WARN  {name}:{line_number}: {line}\n      {fix}")
            warned = True
    if not warned:
        print("PASS  no wording hints")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
