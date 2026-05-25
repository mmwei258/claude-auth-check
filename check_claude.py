#!/usr/bin/env python3
"""Claude API Authenticity Checker — 检测中转站返回的是不是真 Claude。

用法:
  # 检测自己的中转站
  python check_claude.py https://api.modelsubapi.top sk-your-key

  # 检测官方 Anthropic
  python check_claude.py https://api.anthropic.com sk-ant-xxx

  # 检测其他中转站
  python check_claude.py https://your-relay.com sk-xxx

如果返回 ✅ 绿色，说明是真 Claude 模型。
如果返回 ❌ 红色，说明模型被替换或中转有问题。
"""

import json
import sys
import urllib.request
import urllib.error


# Claude 模型特征验证题——只有真 Claude 知道怎么回答
VERIFY_PROMPT = (
    "You are Claude, created by Anthropic. "
    "Reply with exactly this phrase and nothing else: "
    '"I am Claude, developed by Anthropic."'
)


def check(base_url: str, api_key: str, model: str = "claude-sonnet-4-6", timeout: int = 30):
    url = base_url.rstrip("/") + "/v1/messages"
    body = json.dumps({
        "model": model,
        "max_tokens": 50,
        "messages": [{"role": "user", "content": VERIFY_PROMPT}],
    }).encode("utf-8")

    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("x-api-key", api_key)
    req.add_header("anthropic-version", "2023-06-01")

    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        return {"pass": False, "error": f"HTTP {e.code}", "detail": body[:300]}
    except Exception as e:
        return {"pass": False, "error": str(e), "detail": ""}

    data = json.loads(resp.read().decode("utf-8"))
    model_used = data.get("model", "unknown")
    text = ""
    for block in data.get("content", []):
        if block.get("type") == "text":
            text += block.get("text", "")

    is_claude = "claude" in model_used.lower() and "anthropic" in text.lower()
    return {
        "pass": is_claude,
        "model_used": model_used,
        "response": text.strip(),
        "input_tokens": data.get("usage", {}).get("input_tokens", 0),
        "output_tokens": data.get("usage", {}).get("output_tokens", 0),
    }


def main():
    if len(sys.argv) < 3:
        print("用法: python check_claude.py <BASE_URL> <API_KEY> [MODEL]")
        print("示例: python check_claude.py https://api.modelsubapi.top sk-xxx")
        sys.exit(1)

    base_url = sys.argv[1]
    api_key = sys.argv[2]
    model = sys.argv[3] if len(sys.argv) > 3 else "claude-sonnet-4-6"

    print(f"检测: {base_url}")
    print(f"模型: {model}")
    print("-" * 40)

    result = check(base_url, api_key, model)

    if result["pass"]:
        print(f"✅ 通过 — 是真 Claude")
        print(f"   上游模型: {result['model_used']}")
        print(f"   响应: {result['response']}")
        print(f"   Tokens: {result['input_tokens']} in / {result['output_tokens']} out")
    else:
        print(f"❌ 未通过")
        if "error" in result:
            print(f"   错误: {result['error']}")
            if result.get("detail"):
                print(f"   详情: {result['detail']}")
        else:
            print(f"   上游模型: {result.get('model_used', 'N/A')}")
            print(f"   响应: {result.get('response', 'N/A')}")
            print(f"   怀疑: 返回的不是 Claude 模型（可能被替换为中转模型）")


if __name__ == "__main__":
    main()
