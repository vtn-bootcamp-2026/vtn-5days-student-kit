# Package Validation Checklist

Dùng trong PHASE 5 của vibe-packaging-orchestrator.

## Structure Checks

```
□ SKILL.md exists in every skill folder
□ SKILL.md is not empty (> 100 bytes)
□ YAML frontmatter present and parseable
□ YAML has "name" field
□ YAML has "description" field
□ No symlinks in staging (all real files)
□ No .git/ directories
□ No node_modules/ directories
□ No __pycache__/ directories
□ No .DS_Store files
□ File encoding is UTF-8
```

## Content Checks

```
□ No personal info remaining (re-scan after sanitize)
□ No broken internal file references
□ All referenced skills in package or marked external
□ Code blocks properly formatted
□ Markdown headers not duplicated/broken
□ [CUSTOMIZE: ...] placeholders are clear and actionable
```

## ZIP Checks

```
□ ZIP contains root folder (not loose files)
□ Root folder name matches package name
□ ZIP filename follows convention: [name].zip or [name]-v[X.Y].zip
□ Total size < 10MB (warning if > 10MB, hard limit 50MB)
□ ZIP can be extracted without errors
```

## Install Checks

```
□ INSTALL.md exists in package
□ Install instructions are accurate
□ GETTING-STARTED.md exists (multi-skill packages)
□ Dependencies documented clearly
□ External tools/MCP servers listed
```

## Validation Report Template

```
## Package Validation Report

**Package:** [name]
**Skills included:** [count]
**Total files:** [count]
**Total size:** [size] MB
**Personal info findings:** [count] (must be 0)
**Broken references:** [count] (must be 0)
**YAML parse errors:** [count] (must be 0)

Status: READY TO PACKAGE / ISSUES FOUND

[Issue list if any]
```
