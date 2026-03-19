---
name: clear-desktop
description: Move all screenshots from the Desktop to the Trash
---

Move all screenshot files from the user's Desktop to the macOS Trash.

## Step 1 — Find screenshots

Run the following to list all screenshot files on the Desktop (macOS uses "Screenshot" in English and "Bildschirmfoto" in German):

```bash
ls ~/Desktop/ | grep -E "^(Screenshot|Bildschirmfoto)"
```

## Step 2 — Move to Trash

Use the macOS `trash` CLI or `osascript` to move files to Trash (not permanent delete):

```bash
for f in ~/Desktop/Screenshot* ~/Desktop/Bildschirmfoto*; do
  [ -e "$f" ] && osascript -e "tell application \"Finder\" to delete POSIX file \"$f\""
done
```

Confirm how many files were moved and report back to the user.
