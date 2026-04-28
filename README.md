# AI Provider Switcher (APS)

**APS** is a lightweight, zero-dependency CLI tool designed for developers who switch between multiple AI model providers (like Anthropic, OpenAI, DeepSeek, or local LLMs) while using tools like **Claude Code** and **Codex**.

It manages the complexity of different API protocols, varying keys for the same provider, and model-specific configurations by centralizing them into simple TOML files.

## Features

- 🚀 **One-Command Switch**: Update both Claude and Codex configurations simultaneously.
- 🎯 **Granular Control**: Switch providers for only one service (`aps claude use ...` or `aps codex use ...`).
- 📁 **Hierarchical Configuration**: 
  - Define global settings (URLs/Keys).
  - Override settings for specific services (`claude` or `codex`).
  - Create specific **Groups** for different models within the same provider (e.g., `nvidia:glm5` vs `nvidia:llama3`).
- 🛠️ **Alias Support**: Supports both `api_key`/`key` and `base_url`/`url` for maximum compatibility with your existing snippets.

## Installation

1. Clone or download the `aps` script.
2. Make it executable:
   ```bash
   chmod +x aps
   ```
3. Link it to your local bin:
   ```bash
   mkdir -p ~/.local/bin
   ln -s $(pwd)/aps ~/.local/bin/aps
   ```
4. Ensure `~/.local/bin` is in your `PATH`.

## Configuration

Configurations are stored in `~/.ai-provider-switch/<provider-name>.toml`.

### Example: `~/.ai-provider-switch/my-provider.toml`

```toml
# Global URL used if not overridden
url = "https://api.proxy.com/v1"

[claude]
key = "sk-ant-xxxxxx"
model = "claude-3-5-sonnet"

[codex]
key = "sk-op-xxxxxx"
model = "gpt-4o"

[codex.fast]
model = "gpt-4o-mini"
```

Claude Code settings that are stored under `settings.json` `env` can be added
to the same Claude section with APS field names:

```toml
[claude]
key = "sk-ant-xxxxxx"
model = "claude-3-5-sonnet"
default_opus_model = "deepseek-v4-pro[1m]"
default_sonnet_model = "deepseek-v4-pro[1m]"
default_haiku_model = "deepseek-v4-flash"
subagent_model = "deepseek-v4-flash"
effort_level = "max"
```

APS writes these fields to Claude Code's `settings.json` `env` object as
`ANTHROPIC_DEFAULT_OPUS_MODEL`, `ANTHROPIC_DEFAULT_SONNET_MODEL`,
`ANTHROPIC_DEFAULT_HAIKU_MODEL`, and `CLAUDE_CODE_SUBAGENT_MODEL`. The regular
`model` field is written to `settings.json` as Claude Code's top-level `model`;
`effort_level` is written as the top-level `effortLevel` setting.

When switching Claude providers, APS removes its managed Claude settings before
writing the selected provider, so model defaults from a previous provider do not
leak into the next one.

## Usage

| Command | Description |
| :--- | :--- |
| `aps list` | List all configured providers and their groups. |
| `aps use <name>` | Switch both Claude and Codex to the provider. |
| `aps use <name>:<group>` | Switch to a specific group (e.g., `aps use my-provider:fast`). |
| `aps claude use <name>` | Switch only Claude settings. |
| `aps codex use <name>` | Switch only Codex settings. |

## License

MIT License.
