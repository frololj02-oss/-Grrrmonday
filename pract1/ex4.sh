#!/bin/bash
file="$1"
grep -oE '\b[a-zA-Z_][a-zA-Z0-9_]*\b' "$file" | sort -u | tr '\n' ' '
echo ""