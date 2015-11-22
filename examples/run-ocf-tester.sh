#!/bin/sh
export OCF_ROOT='/usr/lib/ocf'
export TESTER_OPTS='-v -d'

check_ocf_tester() {
  which ocf-tester 1>/dev/null 2>/dev/null
  if [ $? -gt "0" ]; then
    echo "OCF Tester is not installed. Skipping tests!"
    exit 0
  fi
}

run_ocf_tester() {
  echo "========================================"
  echo "Running ocf-tester on script '${SCRIPT}'"
  ocf-tester ${TESTER_OPTS} -n 'ocf-tester' ocf-tester-wrapper.sh
  if [ $? -gt "0" ]; then
    echo "Script: '${SCRIPT}' have FAILED the test!"
    exit 1
  else
    echo "Script: '${SCRIPT}' have PASSED the test!"
  fi
  echo "========================================"
}

check_ocf_tester

for script in ${@}; do
  export SCRIPT="${script}"
  run_ocf_tester
done
