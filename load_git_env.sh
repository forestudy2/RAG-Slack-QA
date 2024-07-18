#!/bin/bash

# .env 파일 로드
export $(grep -v '^#' .env | xargs)

# Git 설정
git config --global user.name "$GIT_AUTHOR_NAME"
git config --global user.email "$GIT_AUTHOR_EMAIL"
git config --global author.name "$GIT_AUTHOR_NAME"
git config --global author.email "$GIT_AUTHOR_EMAIL"
git config --global committer.name "$GIT_COMMITTER_NAME"
git config --global committer.email "$GIT_COMMITTER_EMAIL"
