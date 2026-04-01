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
