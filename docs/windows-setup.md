# Windows Setup Guide

This guide helps Windows users set up project-specify with symlink support.

## Overview

Project-specify uses symlinks to efficiently share agent command files across multiple projects. On Windows, creating symlinks requires special permissions that are not enabled by default.

You have three options for using project-specify on Windows:

1. **Enable Developer Mode** (Recommended) - One-time setup, best experience
2. **Use --copy flag** - No setup required, but uses more disk space
3. **Run as Administrator** - Not recommended for daily use

---

## Option 1: Enable Developer Mode (Recommended)

Developer Mode allows regular users to create symlinks without administrator privileges. This is the recommended approach for the best experience.

### Steps to Enable Developer Mode

1. **Open Windows Settings**
   - Press `Windows + I` to open Settings
   - Or click Start → Settings

2. **Navigate to Developer Settings**
   - Click on **Privacy & Security** (left sidebar)
   - Scroll down and click on **For developers**

3. **Enable Developer Mode**
   - Find the "Developer Mode" toggle
   - Turn it **On**
   - Click **Yes** when prompted to confirm

4. **Restart Your Terminal**
   - Close all open terminal windows
   - Open a new terminal (Command Prompt, PowerShell, or Windows Terminal)

5. **Verify Setup**
   ```cmd
   project-specify init my-project --ai claude
   ```

   If successful, you'll see:
   ```
   ✅ .claude/commands -> C:\Users\YourName\.project-specify\agents\claude\commands
   ```

### Troubleshooting Developer Mode

**Issue: Toggle is grayed out**
- You may not have sufficient privileges on your Windows account
- Contact your system administrator or use Option 2 (--copy flag)

**Issue: Symlinks still fail after enabling**
- Make sure you restarted your terminal after enabling Developer Mode
- Try logging out and back in to Windows
- If still failing, try Option 2 (--copy flag)

---

## Option 2: Use --copy Flag

If you cannot enable Developer Mode, use the `--copy` flag to copy command files instead of creating symlinks.

### How to Use --copy

Instead of:
```cmd
project-specify init my-project --ai claude
```

Use:
```cmd
project-specify init my-project --ai claude --copy
```

### Pros and Cons

**Pros:**
- ✅ No special permissions required
- ✅ Works on any Windows system
- ✅ Works in restricted environments (corporate laptops, etc.)

**Cons:**
- ❌ Uses more disk space (files are copied, not linked)
- ❌ Updates to central commands won't automatically apply to existing projects
- ❌ Must manually update projects when upgrading project-specify

### Updating Projects with --copy

When you upgrade project-specify, you'll need to update each project manually:

```cmd
cd my-project
project-specify init . --here --ai claude --copy --force
```

The `--force` flag overwrites existing command files with the updated versions.

---

## Option 3: Run as Administrator

You can run your terminal as Administrator to create symlinks, but this is **not recommended** for daily use due to security risks.

### Steps to Run as Administrator

1. **Close All Terminal Windows**

2. **Open Terminal as Administrator**
   - Search for "Command Prompt" or "PowerShell" in Start Menu
   - Right-click on it
   - Select **Run as Administrator**
   - Click **Yes** when prompted by UAC

3. **Run project-specify Commands**
   ```cmd
   project-specify init my-project --ai claude
   ```

4. **Close Administrator Terminal**
   - After initialization, close the administrator terminal
   - Use regular terminals for day-to-day work

### Why This is Not Recommended

- ⚠️ Running as Administrator gives programs unrestricted access to your system
- ⚠️ Accidental commands could damage your system
- ⚠️ Many development tools warn against running as Administrator
- ⚠️ You'll need to repeat this for every project initialization

**Better alternatives:** Use Option 1 (Developer Mode) or Option 2 (--copy flag)

---

## Comparison Table

| Feature | Developer Mode | --copy Flag | Run as Admin |
|---------|---------------|-------------|--------------|
| One-time setup | ✅ Yes | ❌ No | ❌ No |
| No admin required | ✅ Yes | ✅ Yes | ❌ No |
| Auto-updates work | ✅ Yes | ❌ No | ✅ Yes |
| Disk space efficient | ✅ Yes | ❌ No | ✅ Yes |
| Works in corp. env. | ⚠️ Maybe | ✅ Yes | ⚠️ Maybe |
| Security risk | ✅ Low | ✅ Low | ❌ High |
| **Recommendation** | **Best** | **Good** | **Avoid** |

---

## Verifying Symlinks vs Copies

After initialization, you can verify whether symlinks or copies were created:

### Check with File Explorer

1. Navigate to your project directory
2. Look at `.claude/commands` (or other agent folders)
3. **Symlinks** will show:
   - Arrow overlay on folder icon
   - Properties → Type: "File Folder Shortcut"
4. **Copies** will show:
   - Regular folder icon
   - Properties → Type: "File Folder"

### Check with Command Line

```cmd
cd my-project
dir .claude /AL
```

- If it shows "SYMLINKD", it's a symlink ✅
- If nothing appears, it's a regular copy 📋

---

## Common Issues

### "Access is denied" Error

**Symptom:**
```
❌ Error creating .claude/commands: [WinError 5] Access is denied
```

**Solutions:**
1. Enable Developer Mode (Option 1)
2. Use `--copy` flag (Option 2)
3. Check if antivirus is blocking symlink creation

### "A required privilege is not held by the client"

**Symptom:**
```
OSError: [WinError 1314] A required privilege is not held by the client
```

**Solutions:**
1. This means you don't have symlink permissions
2. Enable Developer Mode (Option 1)
3. Or use `--copy` flag (Option 2)

### Junction Points Created Instead of Symlinks

**Symptom:**
```
ℹ️  Created junction point (Windows requires Developer Mode for symlinks)
```

**Explanation:**
- Junction points are Windows-specific directory links
- They work similarly to symlinks for directories
- This is expected if Developer Mode is not enabled
- For best compatibility, enable Developer Mode

**Solutions:**
1. Enable Developer Mode for true symlink support
2. Junction points will work fine, but `--copy` is more portable

### Symlinks Work in One Terminal But Not Another

**Symptom:**
- Works in PowerShell but not in Git Bash (or vice versa)

**Solutions:**
1. Make sure Developer Mode is enabled
2. Restart the terminal that's not working
3. Try logging out and back in to Windows
4. As a workaround, use `--copy` flag for consistency

---

## Windows-Specific Notes

### Windows Defender and Antivirus

Some antivirus software may block symlink creation as a security precaution:

1. Check your antivirus logs for blocked actions
2. Add an exception for your development folder
3. Add an exception for project-specify executable
4. If issues persist, use `--copy` flag

### WSL (Windows Subsystem for Linux)

If you're using WSL, you have two options:

**Option A: Install in Windows**
- Install project-specify in Windows (PowerShell/Command Prompt)
- Access projects from Windows side

**Option B: Install in WSL**
- Install project-specify inside your WSL distribution
- Symlinks work natively in WSL without special permissions
- Projects must stay within WSL filesystem for best performance

**Do not mix:** Installing in Windows and using from WSL (or vice versa) may cause path issues.

### OneDrive / Cloud Storage

If your project is in OneDrive, Google Drive, or similar:

1. Symlinks in cloud-synced folders may not sync correctly
2. Different computers may have different symlink support
3. **Recommendation:** Use `--copy` flag for cloud-synced projects
4. Or move projects outside cloud-synced folders

---

## Getting Help

If you're still having issues:

1. Check this guide's Common Issues section
2. Run with `--debug` flag for detailed error messages:
   ```cmd
   project-specify init my-project --ai claude --debug
   ```
3. Report issues at: [GitHub Issues](https://github.com/ddunnock/project-specify/issues)
4. Include:
   - Full error message
   - Output with `--debug` flag
   - Windows version (run `winver` to check)
   - Whether Developer Mode is enabled

---

## Summary

**Quick Start for Windows Users:**

```cmd
# Best option: Enable Developer Mode (one-time setup)
# Settings → Privacy & Security → For developers → Enable Developer Mode
# Then restart terminal and run:
project-specify init my-project --ai claude

# OR: No setup required, use --copy flag
project-specify init my-project --ai claude --copy
```

Choose the approach that works best for your environment!
