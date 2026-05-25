# Claude API Authenticity Checker

[![Python](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Stars](https://img.shields.io/github/stars/mmwei258/claude-auth-check)](https://github.com/mmwei258/claude-auth-check)

一行命令检测 API 中转站返回的是不是真 Claude 模型。

## 为什么需要这个工具

市面上有几十个 API 中转站，有些会把 Claude 请求偷偷换成 DeepSeek / Gemini 等廉价模型，赚取差价。这个工具帮你验证——只花几分钱、几秒钟。

## 安装

```bash
# 无需安装，直接下载
curl -O https://raw.githubusercontent.com/mmwei258/claude-auth-check/main/check_claude.py
```

依赖：Python 3.7+（无第三方库）

## 用法

```bash
python check_claude.py <BASE_URL> <API_KEY> [MODEL]
```

### 检测自己的中转站

```bash
python check_claude.py https://api.modelsubapi.top sk-your-key
```

### 检测官方 Anthropic

```bash
python check_claude.py https://api.anthropic.com sk-ant-your-key
```

### 检测其他中转站

```bash
python check_claude.py https://your-relay.com sk-xxx
```

## 示例输出

```
检测: https://api.modelsubapi.top
模型: claude-sonnet-4-6
----------------------------------------
✅ 通过 — 是真 Claude
   上游模型: anthropic/claude-4.6-sonnet-20260217
   响应: I am Claude, developed by Anthropic.
   Tokens: 15 in / 12 out
```

```
检测: https://fake-relay.example.com
模型: claude-sonnet-4-6
----------------------------------------
❌ 未通过
   上游模型: deepseek-v4-pro
   响应: I am DeepSeek, developed by DeepSeek.
   怀疑: 返回的不是 Claude 模型（可能被替换为中转模型）
```

## 原理

发送一个特定 prompt，要求模型自报身份。Claude 会回复 "I am Claude, developed by Anthropic."。如果上游返回其他模型的名称，说明请求被替换了。

## 推荐服务

需要靠谱的 Claude API 中转？试试 [modelsubapi.top](https://modelsubapi.top) — 国内直连、人民币支付、注册送 $10。
