#!/usr/bin/env python3
"""
Git 冲突解析脚本 - 确定性提取所有冲突文件和冲突块
输出结构化 JSON，供 AI agent 消费

用法: python3 parse_conflicts.py [git_repo_path]
默认使用当前目录
"""

import json
import os
import re
import subprocess
import sys
from collections import Counter

VERSION = "1.1.0"


def get_git_dir(repo_path):
    """获取实际的 .git 目录路径（支持 worktree 和 submodule）"""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            capture_output=True, text=True, cwd=repo_path
        )
        if result.returncode != 0:
            return None
        git_dir = result.stdout.strip()
        if not os.path.isabs(git_dir):
            git_dir = os.path.join(repo_path, git_dir)
        return git_dir
    except (FileNotFoundError, OSError):
        return None


def get_conflict_files(repo_path):
    """获取所有冲突文件列表"""
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=U"],
            capture_output=True, text=True, cwd=repo_path
        )
    except (FileNotFoundError, OSError) as e:
        return {"error": str(e), "files": []}
    if result.returncode != 0:
        return {"error": result.stderr.strip(), "files": []}
    files = [f.strip() for f in result.stdout.strip().split("\n") if f.strip()]
    return {"error": None, "files": files}


def is_binary_file(filepath):
    """检测是否为二进制文件"""
    try:
        with open(filepath, "rb") as f:
            chunk = f.read(8192)
            return b"\x00" in chunk
    except (IOError, OSError):
        return True  # 读取失败时保守认为是二进制


def parse_conflict_blocks(content):
    """从文件内容中提取所有冲突块"""
    blocks = []
    # 标准化换行符（处理 CRLF）
    content = content.replace("\r\n", "\n").replace("\r", "\n")
    lines = content.split("\n")
    i = 0
    block_index = 0

    while i < len(lines):
        # 检测冲突开始标记（必须是 <<<<<<< 后跟空格和标签）
        if lines[i].startswith("<<<<<<< ") or lines[i] == "<<<<<<<":
            ours_label = lines[i][7:].strip()
            ours_lines = []
            base_lines = []
            theirs_lines = []
            has_base = False
            start_line = i + 1  # 1-indexed
            found_end = False

            i += 1
            section = "ours"

            while i < len(lines):
                if lines[i].startswith("||||||| ") or lines[i] == "|||||||":
                    has_base = True
                    section = "base"
                    i += 1
                    continue
                elif lines[i] == "=======":
                    section = "theirs"
                    i += 1
                    continue
                elif lines[i].startswith(">>>>>>> ") or lines[i] == ">>>>>>>":
                    theirs_label = lines[i][7:].strip()
                    end_line = i + 1  # 1-indexed
                    found_end = True

                    # 提取上下文（冲突块前后各 3 行，过滤掉冲突标记行）
                    ctx_before_start = max(0, start_line - 1 - 3)
                    ctx_after_end = min(len(lines), end_line + 3)
                    context_before = lines[ctx_before_start:start_line - 1]
                    context_after = lines[end_line:ctx_after_end]

                    block = {
                        "index": block_index,
                        "startLine": start_line,
                        "endLine": end_line,
                        "oursLabel": ours_label,
                        "theirsLabel": theirs_label,
                        "ours": "\n".join(ours_lines),
                        "theirs": "\n".join(theirs_lines),
                        "hasBase": has_base,
                        "contextBefore": "\n".join(context_before),
                        "contextAfter": "\n".join(context_after),
                    }
                    if has_base:
                        block["base"] = "\n".join(base_lines)

                    blocks.append(block)
                    block_index += 1
                    break
                else:
                    if section == "ours":
                        ours_lines.append(lines[i])
                    elif section == "base":
                        base_lines.append(lines[i])
                    elif section == "theirs":
                        theirs_lines.append(lines[i])
                    i += 1
                    continue

            # 孤立的 <<<<<<< 没有匹配到 >>>>>>>
            if not found_end:
                blocks.append({
                    "index": block_index,
                    "startLine": start_line,
                    "endLine": len(lines),
                    "oursLabel": ours_label,
                    "theirsLabel": "",
                    "ours": "\n".join(ours_lines),
                    "theirs": "\n".join(theirs_lines),
                    "hasBase": has_base,
                    "contextBefore": "",
                    "contextAfter": "",
                    "error": "冲突标记不完整：缺少 >>>>>>> 结束标记",
                    "classification": "complex"
                })
                block_index += 1

        i += 1

    return blocks


def classify_conflict(block):
    """对冲突块做初步分类，辅助 AI 判断"""
    # 已有 error 标记的直接返回 complex
    if "error" in block:
        return "complex"

    ours = block["ours"]
    theirs = block["theirs"]

    # 双方都为空
    if not ours.strip() and not theirs.strip():
        return "both_empty"

    # 空白差异（去除空白后内容完全一致）
    if ours.strip() == theirs.strip():
        return "whitespace"

    ours_lines = [l.strip() for l in ours.split("\n") if l.strip()]
    theirs_lines = [l.strip() for l in theirs.split("\n") if l.strip()]

    # 一方为空（删除 vs 保留）- 必须交互处理
    if not ours_lines:
        return "ours_deleted"
    if not theirs_lines:
        return "theirs_deleted"

    # import 语句检测（扩展正则覆盖更多语法）
    import_pattern = re.compile(
        r"^(import\s|from\s|require\(|export\s.*\sfrom\s|"
        r"const\s+[\w{].*=\s*require|@import\s|@use\s)"
    )
    if all(import_pattern.match(l) for l in ours_lines) and \
       all(import_pattern.match(l) for l in theirs_lines):
        return "import_order"

    # 超集检测 - 使用 Counter（多重集合）保留重复行信息
    ours_counter = Counter(ours_lines)
    theirs_counter = Counter(theirs_lines)
    # A 是 B 的子集：A 中每个元素的计数都 <= B 中的计数
    ours_is_sub = all(ours_counter[k] <= theirs_counter[k] for k in ours_counter)
    theirs_is_sub = all(theirs_counter[k] <= ours_counter[k] for k in theirs_counter)

    if ours_is_sub and not theirs_is_sub:
        # 进一步检查：行数差异不超过 30% 才认为是超集（防止误判）
        if len(theirs_lines) <= len(ours_lines) * 1.3 + 5:
            return "theirs_superset"
    if theirs_is_sub and not ours_is_sub:
        if len(ours_lines) <= len(theirs_lines) * 1.3 + 5:
            return "ours_superset"

    # 两边内容相同但顺序不同
    if ours_counter == theirs_counter:
        return "reorder"

    # 版本号差异（package.json 场景）
    version_pattern = re.compile(r'^\s*"[^"]+"\s*:\s*"[\w^~>=<.*:| -]')
    if all(version_pattern.match(l) for l in ours_lines) and \
       all(version_pattern.match(l) for l in theirs_lines):
        return "version_diff"

    return "complex"


def detect_merge_type(repo_path):
    """检测当前是 merge、rebase、cherry-pick 还是 revert"""
    git_dir = get_git_dir(repo_path)
    if not git_dir:
        return "unknown"

    if os.path.exists(os.path.join(git_dir, "MERGE_HEAD")):
        return "merge"
    elif os.path.exists(os.path.join(git_dir, "rebase-merge")) or \
         os.path.exists(os.path.join(git_dir, "rebase-apply")):
        return "rebase"
    elif os.path.exists(os.path.join(git_dir, "CHERRY_PICK_HEAD")):
        return "cherry-pick"
    elif os.path.exists(os.path.join(git_dir, "REVERT_HEAD")):
        return "revert"
    return "unknown"


def get_branch_names(repo_path):
    """获取当前分支和合入分支名"""
    try:
        current = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True, text=True, cwd=repo_path
        ).stdout.strip()
    except (FileNotFoundError, OSError):
        current = ""

    git_dir = get_git_dir(repo_path)
    incoming = ""
    if git_dir:
        # 按优先级检查不同类型的 HEAD 文件
        for head_file in ["MERGE_HEAD", "CHERRY_PICK_HEAD", "REVERT_HEAD"]:
            head_path = os.path.join(git_dir, head_file)
            if os.path.exists(head_path):
                try:
                    with open(head_path) as f:
                        commit_hash = f.read().strip()
                    result = subprocess.run(
                        ["git", "name-rev", "--name-only", commit_hash],
                        capture_output=True, text=True, cwd=repo_path
                    )
                    incoming = result.stdout.strip()
                except (IOError, OSError):
                    pass
                break

    return {"current": current or "HEAD", "incoming": incoming or "unknown"}


# lock 文件列表
LOCK_FILES = {
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
    "Gemfile.lock", "Cargo.lock", "poetry.lock",
    "composer.lock", "Pipfile.lock", "go.sum"
}


def main():
    repo_path = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()

    # 确认是 git 仓库
    try:
        check = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            capture_output=True, text=True, cwd=repo_path
        )
    except (FileNotFoundError, OSError) as e:
        print(json.dumps({"error": f"无法执行 git: {e}", "files": []}, ensure_ascii=False))
        sys.exit(1)

    if check.returncode != 0:
        print(json.dumps({"error": "不是 Git 仓库", "files": []}, ensure_ascii=False))
        sys.exit(1)

    result = get_conflict_files(repo_path)
    if result["error"]:
        print(json.dumps({"error": result["error"], "files": []}, ensure_ascii=False))
        sys.exit(1)

    conflict_files = result["files"]
    merge_type = detect_merge_type(repo_path)

    if not conflict_files:
        print(json.dumps({
            "version": VERSION,
            "mergeType": merge_type,
            "branches": get_branch_names(repo_path),
            "totalFiles": 0,
            "files": [],
            "summary": {"auto": 0, "complex": 0, "binary": 0, "lock": 0}
        }, ensure_ascii=False))
        sys.exit(0)

    files_data = []
    summary = {"auto": 0, "complex": 0, "binary": 0, "lock": 0}

    for filepath in conflict_files:
        full_path = os.path.join(repo_path, filepath)
        filename = os.path.basename(filepath)

        file_info = {
            "path": filepath,
            "filename": filename,
        }

        # lock 文件
        if filename in LOCK_FILES:
            file_info["type"] = "lock"
            file_info["blocks"] = []
            file_info["suggestion"] = "删除此文件后重新 install 生成"
            summary["lock"] += 1
            files_data.append(file_info)
            continue

        # 二进制文件
        if is_binary_file(full_path):
            file_info["type"] = "binary"
            file_info["blocks"] = []
            summary["binary"] += 1
            files_data.append(file_info)
            continue

        # 文本文件 - 解析冲突块
        try:
            with open(full_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
        except (IOError, OSError) as e:
            file_info["type"] = "error"
            file_info["error"] = str(e)
            file_info["blocks"] = []
            files_data.append(file_info)
            continue

        # 检测是否包含 replacement character（非 UTF-8 文件）
        has_encoding_issues = "\ufffd" in content

        blocks = parse_conflict_blocks(content)
        for block in blocks:
            if "classification" not in block:  # 孤立标记已有分类
                block["classification"] = classify_conflict(block)

        # 统计：ours_deleted/theirs_deleted 归入 complex（需用户介入）
        auto_classifications = {
            "whitespace", "import_order", "ours_superset",
            "theirs_superset", "reorder", "both_empty"
        }
        auto_count = sum(1 for b in blocks if b["classification"] in auto_classifications)
        complex_count = len(blocks) - auto_count

        file_info["type"] = "text"
        file_info["totalLines"] = len(content.split("\n"))
        file_info["blocks"] = blocks
        file_info["autoCount"] = auto_count
        file_info["complexCount"] = complex_count
        if has_encoding_issues:
            file_info["encodingWarning"] = "文件可能非 UTF-8 编码，逐块替换可能损坏文件，建议使用 git checkout --ours/--theirs"

        summary["auto"] += auto_count
        summary["complex"] += complex_count
        files_data.append(file_info)

    output = {
        "version": VERSION,
        "mergeType": merge_type,
        "branches": get_branch_names(repo_path),
        "totalFiles": len(conflict_files),
        "files": files_data,
        "summary": summary
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
