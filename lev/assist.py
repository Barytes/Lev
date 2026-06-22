from __future__ import annotations

import difflib
import textwrap

from lev.models import AssistRequest, AssistResponse


MAX_DOCUMENT_CHARS = 9000
MAX_DIFF_CHARS = 2500


def build_recent_diff(previous: str, current: str) -> str:
    if not previous:
        return "No previous snapshot. Treat this as the opening document state."

    diff = "\n".join(
        difflib.unified_diff(
            previous.splitlines(),
            current.splitlines(),
            fromfile="previous",
            tofile="current",
            lineterm="",
            n=3,
        )
    )
    if len(diff) > MAX_DIFF_CHARS:
        return diff[-MAX_DIFF_CHARS:]
    return diff or "No textual change detected."


def extract_cursor_context(content: str, cursor: int, radius: int = 700) -> str:
    cursor = max(0, min(cursor, len(content)))
    start = max(0, cursor - radius)
    end = min(len(content), cursor + radius)
    return content[start:end]


def infer_lightweight_intent(content: str, diff: str) -> str:
    text = f"{diff}\n{content[-1200:]}".lower()
    if any(marker in text for marker in ["mvp", "产品", "功能", "架构", "界面"]):
        return "product_design"
    if any(marker in text for marker in ["引用", "资料", "搜索", "论文", "source"]):
        return "research_support"
    if any(marker in text for marker in ["区别", "对比", "versus", "vs", "误区"]):
        return "compare_or_clarify"
    if any(marker in text for marker in ["todo", "下一步", "plan", "实现"]):
        return "planning"
    return "writing_support"


def build_assist_prompt(request: AssistRequest, diff: str, cursor_context: str) -> str:
    clipped_document = request.content[-MAX_DOCUMENT_CHARS:]
    return textwrap.dedent(
        f"""
        You are Lev, a human-centered agent for a live writing workspace.

        The user is actively editing a document. Do not take over the user's
        subject action. Do not write a full replacement draft. Your job is to
        infer the user's current intent from the document and recent diff, then
        prepare concise support that helps the user continue their own work.

        Output only the side-panel assistance text in Chinese. No chatty opener.
        Keep it useful, sparse, and grounded in the document.

        Good assistance:
        - names the likely current intent
        - surfaces missing context, contradictions, useful references, or next
          small moves
        - may include short candidate phrases, but not a full answer
        - searches the web only if current external facts or references are
          useful for the user's immediate writing intent

        Bad assistance:
        - completing the whole document for the user
        - asking the user to approve an agent-written answer
        - giving generic advice that ignores the current cursor area

        Active file: {request.path}
        Cursor offset: {request.cursor}
        Selection: {request.selection_start}-{request.selection_end}

        Recent diff:
        {diff}

        Cursor neighborhood:
        {cursor_context}

        Document tail / snapshot:
        {clipped_document}
        """
    ).strip()


def fallback_assistance(request: AssistRequest, error: Exception | None = None) -> AssistResponse:
    diff = build_recent_diff(request.previous_content, request.content)
    cursor_context = extract_cursor_context(request.content, request.cursor)
    intent = infer_lightweight_intent(cursor_context, diff)
    note = ""
    if error is not None:
        note = f"\n\nAgent 暂时不可用：{error}"

    assistance = textwrap.dedent(
        f"""
        当前推断：{intent}

        我看到你正在编辑 `{request.path}`。这一版先不替你写正文，只把最近变化和光标附近内容整理出来，方便你继续自己的判断。

        最近变化：
        {diff[:900]}

        光标附近：
        {cursor_context[:900]}
        {note}
        """
    ).strip()
    return AssistResponse(assistance=assistance, intent=intent, source="fallback")


def generate_assistance(request: AssistRequest) -> AssistResponse:
    diff = build_recent_diff(request.previous_content, request.content)
    cursor_context = extract_cursor_context(request.content, request.cursor)
    intent = infer_lightweight_intent(cursor_context, diff)
    prompt = build_assist_prompt(request, diff, cursor_context)

    try:
        from main import ChatRequest, run_agent_loop

        response = run_agent_loop(ChatRequest(message=prompt))
    except Exception as exc:
        return fallback_assistance(request, exc)

    return AssistResponse(assistance=response.response, intent=intent, source="agent")
