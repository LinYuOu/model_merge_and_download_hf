20260204 使用 claude 

安装参考
```bash
https://code.claude.com/docs/en/setup#installation
```

查看
```bash
claude --version
```
有版本号就ok

配置
```bash
vim ~/.claude/settings.json
```
直接粘贴
```
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "sk-or-xxxxxxxxxx",
    "ANTHROPIC_BASE_URL": "https://openrouter.ai/api",
    "ANTHROPIC_API_KEY": "", # 为空即可
    "API_TIMEOUT_MS": "3000000",
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": 1,
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "openrouter/free",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "openrouter/free",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "openrouter/free",
    "HTTP_X_TITLE": "openrouter/free"
  }
}
```
即可

不习惯命令行的，在完成以上配置后，可以安装 cluade vscode 插件
