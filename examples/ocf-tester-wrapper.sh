#!/bin/sh
if [ -f "${SCRIPT}" ]; then
  python "${SCRIPT}" ${@}
else
  echo "There is no such script: '${SCRIPT}'"
  exit 1
fi
