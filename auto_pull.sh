#!/bin/sh

repository_url="https://github.com/kmoonsun/repository_parser"
toekn="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"

git add -A
git status
git commit -m "auto icommit"

git push $repository main
echo "kmoonsun"
echo $token

