#!/bin/zsh

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_DIR="$REPO_DIR/Skills"
PROJECT_COMMANDS="$REPO_DIR/.claude/commands"
GLOBAL_SKILLS="$HOME/.claude/skills"

echo "Setting up Claude Code skills..."

# Create commands directory if missing
mkdir -p "$PROJECT_COMMANDS"
mkdir -p "$GLOBAL_SKILLS"

# Symlink all skills
for file in "$SKILLS_DIR"/*_SKILL.md; do
  [ -f "$file" ] || continue
  name=$(basename "$file" _SKILL.md)

  ln -sf "$file" "$PROJECT_COMMANDS/$name.md"
  echo "  ✓ Command: /$name"

  if [ ! -d "$GLOBAL_SKILLS/$name" ]; then
    mkdir -p "$GLOBAL_SKILLS/$name"
  fi
  ln -sf "$file" "$GLOBAL_SKILLS/$name/SKILL.md"
  echo "  ✓ Global skill: $name"
done

# Install post-merge hook (uses dynamic paths so it works for any team member)
HOOK_PATH="$REPO_DIR/.git/hooks/post-merge"
cat > "$HOOK_PATH" << EOF
#!/bin/zsh

REPO_DIR="\$(cd "\$(dirname "\$0")/../.." && pwd)"
SKILLS_DIR="\$REPO_DIR/Skills"
PROJECT_COMMANDS="\$REPO_DIR/.claude/commands"
GLOBAL_SKILLS="\$HOME/.claude/skills"

for file in "\$SKILLS_DIR"/*_SKILL.md; do
  [ -f "\$file" ] || continue
  name=\$(basename "\$file" _SKILL.md)

  if [ ! -L "\$PROJECT_COMMANDS/\$name.md" ]; then
    ln -sf "\$file" "\$PROJECT_COMMANDS/\$name.md"
    echo "[post-merge] Added command: /\$name"
  fi

  if [ ! -d "\$GLOBAL_SKILLS/\$name" ]; then
    mkdir -p "\$GLOBAL_SKILLS/\$name"
    ln -sf "\$file" "\$GLOBAL_SKILLS/\$name/SKILL.md"
    echo "[post-merge] Added global skill: \$name"
  fi
done
EOF
chmod +x "$HOOK_PATH"
echo "  ✓ post-merge hook installed"

echo ""
echo "Done. Restart Claude Code to pick up new slash commands."
