#!/usr/bin/env bash
set -euo pipefail

LABEL="com.decoy-service.daemon"
PORT="9999"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE_PLIST="${PROJECT_DIR}/com.decoy-service.daemon.plist"
LAUNCH_AGENTS_DIR="${HOME}/Library/LaunchAgents"
TARGET_PLIST="${LAUNCH_AGENTS_DIR}/${LABEL}.plist"
RUNTIME_DIR="${HOME}/.decoy-service"
APP_DIR="${RUNTIME_DIR}/app"
STDOUT_LOG="${RUNTIME_DIR}/daemon-stdout.log"
STDERR_LOG="${RUNTIME_DIR}/daemon-stderr.log"
LAUNCH_DOMAIN="gui/$(id -u)"

usage() {
  cat <<'EOF'
Usage: ./daemonctl.sh <command>

Commands:
  install    Install + start LaunchAgent
  sync       Restage latest project code into daemon runtime path
  start      Start daemon (or restart if already loaded)
  stop       Stop daemon
  restart    Restart daemon
  status     Show launchd + health status
  logs       Tail daemon stdout/stderr logs
  uninstall  Stop and remove LaunchAgent
EOF
}

resolve_python_bin() {
  local candidates=()
  local candidate

  candidates+=("${PROJECT_DIR}/venv/bin/python3")
  candidates+=("$(command -v python3 2>/dev/null || true)")
  candidates+=("/opt/homebrew/bin/python3")
  candidates+=("/usr/local/bin/python3")
  candidates+=("/usr/bin/python3")

  for candidate in "${candidates[@]}"; do
    if [[ -x "${candidate}" ]] && "${candidate}" -c "import flask, flask_cors" >/dev/null 2>&1; then
      echo "${candidate}"
      return 0
    fi
  done

  for candidate in "${candidates[@]}"; do
    if [[ -x "${candidate}" ]]; then
      echo "${candidate}"
      return 0
    fi
  done

  return 1
}

render_plist() {
  local python_bin="$1"
  local service_dir="$2"
  local escaped_service_dir escaped_python_bin escaped_home

  escaped_service_dir="${service_dir//\//\\/}"
  escaped_python_bin="${python_bin//\//\\/}"
  escaped_home="${HOME//\//\\/}"

  sed \
    -e "s/{{DECOY_SERVICE_PATH}}/${escaped_service_dir}/g" \
    -e "s/{{PYTHON_BIN}}/${escaped_python_bin}/g" \
    -e "s/{{USER_HOME}}/${escaped_home}/g" \
    "${TEMPLATE_PLIST}" > "${TARGET_PLIST}"
}

stage_runtime_files() {
  rm -rf "${APP_DIR}"
  mkdir -p "${APP_DIR}"
  cp "${PROJECT_DIR}/api_server.py" "${APP_DIR}/api_server.py"
  cp -R "${PROJECT_DIR}/decoy_service" "${APP_DIR}/decoy_service"
}

bootout_if_loaded() {
  if launchctl print "${LAUNCH_DOMAIN}/${LABEL}" >/dev/null 2>&1; then
    launchctl bootout "${LAUNCH_DOMAIN}/${LABEL}"
  fi
}

install_daemon() {
  local python_bin
  python_bin="$(resolve_python_bin)"
  if [[ -z "${python_bin}" ]]; then
    echo "python3 not found on PATH."
    exit 1
  fi
  if ! "${python_bin}" -c "import flask, flask_cors" >/dev/null 2>&1; then
    echo "Warning: ${python_bin} does not have flask/flask-cors installed."
    echo "Install dependencies with: ${python_bin} -m pip install -r decoy_service/requirements.txt"
  fi

  mkdir -p "${LAUNCH_AGENTS_DIR}" "${RUNTIME_DIR}"
  stage_runtime_files
  render_plist "${python_bin}" "${APP_DIR}"

  bootout_if_loaded || true
  launchctl bootstrap "${LAUNCH_DOMAIN}" "${TARGET_PLIST}"
  launchctl kickstart -k "${LAUNCH_DOMAIN}/${LABEL}"

  echo "Installed and started ${LABEL}"
  echo "Daemon code staged at ${APP_DIR}"
  echo "API should be available at http://localhost:${PORT}/api/health"
}

start_daemon() {
  if [[ ! -f "${TARGET_PLIST}" ]]; then
    echo "LaunchAgent is not installed. Run: ./daemonctl.sh install"
    exit 1
  fi

  if ! launchctl print "${LAUNCH_DOMAIN}/${LABEL}" >/dev/null 2>&1; then
    launchctl bootstrap "${LAUNCH_DOMAIN}" "${TARGET_PLIST}"
  fi
  launchctl kickstart -k "${LAUNCH_DOMAIN}/${LABEL}"
  echo "Started ${LABEL}"
}

stop_daemon() {
  if launchctl print "${LAUNCH_DOMAIN}/${LABEL}" >/dev/null 2>&1; then
    launchctl bootout "${LAUNCH_DOMAIN}/${LABEL}"
    echo "Stopped ${LABEL}"
  else
    echo "${LABEL} is not running"
  fi
}

status_daemon() {
  if launchctl print "${LAUNCH_DOMAIN}/${LABEL}" >/dev/null 2>&1; then
    echo "LaunchAgent: loaded"
    launchctl print "${LAUNCH_DOMAIN}/${LABEL}" | grep -E "state =|pid =|last exit code =" || true
  else
    echo "LaunchAgent: not loaded"
  fi

  if command -v curl >/dev/null 2>&1 && curl -fsS "http://localhost:${PORT}/api/health" >/dev/null; then
    echo "API health: reachable (localhost:${PORT})"
  else
    echo "API health: unreachable (localhost:${PORT})"
  fi
}

restart_daemon() {
  stop_daemon || true
  start_daemon
}

uninstall_daemon() {
  stop_daemon || true
  rm -f "${TARGET_PLIST}"
  echo "Removed ${TARGET_PLIST}"
}

sync_runtime() {
  mkdir -p "${RUNTIME_DIR}"
  stage_runtime_files
  echo "Staged latest code to ${APP_DIR}"
  echo "Run ./daemonctl.sh restart to apply staged changes."
}

tail_logs() {
  mkdir -p "${RUNTIME_DIR}"
  touch "${STDOUT_LOG}" "${STDERR_LOG}"
  tail -f "${STDOUT_LOG}" "${STDERR_LOG}"
}

main() {
  local command="${1:-}"
  case "${command}" in
    install)
      install_daemon
      ;;
    sync)
      sync_runtime
      ;;
    start)
      start_daemon
      ;;
    stop)
      stop_daemon
      ;;
    restart)
      restart_daemon
      ;;
    status)
      status_daemon
      ;;
    logs)
      tail_logs
      ;;
    uninstall)
      uninstall_daemon
      ;;
    *)
      usage
      exit 1
      ;;
  esac
}

main "$@"
