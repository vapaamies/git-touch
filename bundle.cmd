@echo off

if -%1==- (
  call %0 "%~dp0."
  goto :eof
)

set versioned=./script/git-touch
set non-versioned=hook-samples/*
set version=0.0

for /f "delims=/- tokens=2" %%v in ('git describe --tags --long --always --candidates=1 --match release/*') do (
  set version=%%v
)

set arc=%~n1-%version%.7z
set opt=-bb -stl -ms -mx -myx -myv -mqs

python script/version.py %versioned%
7z a "%arc%" %opt% -m0=PPMd:o8 %versioned% %non-versioned%