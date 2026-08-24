# Models and API Tiers

## Local primary models

### Qwen3-8B
`Qwen/Qwen3-8B`

Pinned bootstrap revision: `b968826d9c46dd6066d109eabc6255188de91218`.

Use as a primary local model. Detect whether BF16, 8-bit, 4-bit, or another serving format is stable on the actual workstation before freezing deployment.

### Mistral-7B-Instruct-v0.3
`mistralai/Mistral-7B-Instruct-v0.3`

Pinned bootstrap revision: `c170c708c41dac9275d15a8fff4eca08d52bab71`.

Use as a primary local model. Keep the official tokenizer/chat template and record the exact serving stack.

### Gemma 3 12B IT
`google/gemma-3-12b-it`

Use as the larger local robustness model. Access requires acceptance of the Gemma usage license on Hugging Face. Freeze the exact revision after access is confirmed.

## Secondary API reference tier

The API tier exists to test whether conclusions transfer to stronger/different provider families without multiplying the entire experiment cost.

- OpenAI `gpt-5.6-terra`
- Anthropic `claude-sonnet-5`
- DeepSeek `deepseek-v4-flash`
- Google `gemini-3.7-flash`

Use a frozen, preregistered subset after the local pilot. Record provider model ID, date, request ID where available, reasoning/effort mode, sampling parameters, context window, input/output tokens, latency, retries, and pricing snapshot.

## Fairness rule

The central cross-model analysis may use only uncertainty features observable for all compared models. Logit-dependent or hidden-state-dependent features belong in explicitly labeled white-box secondary analyses.

## Hardware note

Two 15.92 GiB-class GPUs do not automatically behave like one 31.84 GiB GPU. Model parallelism, quantization, KV cache, context length, and serving backend must be empirically validated. Preflight owns the final deployment decision.
