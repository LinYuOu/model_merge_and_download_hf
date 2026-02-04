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
vim ~/.bashrc
```
直接粘贴
```bash
# Set these in your shell (e.g., ~/.bashrc, ~/.zshrc)
export ANTHROPIC_BASE_URL="https://openrouter.ai/api"
export ANTHROPIC_AUTH_TOKEN="sk-or-v1-xxx"
export ANTHROPIC_API_KEY="" # Important: Must be explicitly empty
export HTTP_X_TITLE=$CODE_MODEL         # 复制 openrouter 上的名字
export ANTHROPIC_DEFAULT_HAIKU_MODEL=$CODE_MODEL
export ANTHROPIC_DEFAULT_SONNET_MODEL=$CODE_MODEL
export ANTHROPIC_DEFAULT_OPUS_MODEL=$CODE_MODEL
```
即可

不习惯命令行的，在完成以上配置后，可以安装 cluade for vscode 插件
