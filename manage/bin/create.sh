#!/bin/bash

pthtop="$(cd "$(dirname "${0}")/../../../.." && pwd)"
source "${pthtop}"/manage/lib/params.sh
source "${pthtop}"/manage/lib/shared.sh
source "${pthcrr}"/params.sh

pthapp="${pthsrc}"/appvox

addimg ${imgtgt} "${cnfimg}" "${pthdoc}"
test -d "${pthapp}" || mkdir "${pthapp}"
cd "${pthapp}"
if test ! -e download
then
  arc=$(docker run --rm ${imgtgt} uname -m)
  if test ${arc} = 'x86_64'
  then
    curl -sSfL https://github.com/VOICEVOX/voicevox_core/releases/latest/download/download-linux-x64 -o download && chmod 755 download
  fi
  if test ${arc} = 'aarch64'
  then
    curl -sSfL https://github.com/VOICEVOX/voicevox_core/releases/latest/download/download-linux-arm64 -o download && chmod 755 download
  fi
fi
if test ! -d "${pthapp}"/voicevox_core
then
  if test -t 0
  then
    docker run -it --rm -v "${pthapp}":/opt/appvox --name ${cnttgt} ${imgtgt} bash -c "cd /opt/appvox && ./download"
  else
    docker run -i  --rm -v "${pthapp}":/opt/appvox --name ${cnttgt} ${imgtgt} bash -c "cd /opt/appvox && ./download"
  fi
fi
