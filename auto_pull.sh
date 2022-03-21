#!/bin/sh

repository_url="git@github.com:kmoonsun/repository_parser.git"

git add -A
git status
git commit -m "auto icommit"

git push $repository_url main
