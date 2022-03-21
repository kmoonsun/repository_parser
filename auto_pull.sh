#!/bin/sh

repository_url="git@github.com:kmoonsun/repository_parser.git"

git add -A
git status

echo "comment > "
read comment

git commit -m"$comment"

git push $repository_url main
