#!/usr/bin/env bash

# ----------------------------------------------------------------------------------------------------------------------
# "Bootstrap"
# ----------------------------------------------------------------------------------------------------------------------

set -o errexit
set -o errtrace
set -o functrace
set -o nounset
set -o pipefail

# Use xtrace ?
if [ "`getopt --longoptions xtrace -- x "$@" 2> /dev/null | grep --color=none "\(^\|\s\)\(\-x\|\-\-xtrace\)\($\|\s\)"`" != "" ] ; then
    set -o xtrace
fi

# ======================================================================================================================

__trap_exit__()
{
    local code="${1}"

    # Make sure we're called from the main script
    if [ "${$}" -eq "${BASHPID}" ]; then
        printf "\n"
        if [ ${code} -eq 0 ] ; then
            log_success "process ${BASHPID} exited normally in ${SECONDS}s at `date_now`"
        else
            # Unset trap so we exit immediately
            trap - ERR EXIT

            # Prepare stack trace
            local stack_trace=()
            for ((i=0;i<${#FUNCNAME[@]}-1;i++)) ; do
                stack_trace+=("${BASH_SOURCE[$i+1]}:${BASH_LINENO[$i]} in function ${FUNCNAME[$i+1]}")
            done

            # Print the stack trace
            log_error "process ${BASHPID} exited with error code ${code} in ${SECONDS}s at `date_now`"
            >&2 printf "\nStack trace (most recent call last):\n"
            for ((i=${#stack_trace[@]}-1;i>=0;i--)) ; do
                >&2 printf "  ${stack_trace[$i]}\n"
            done
        fi
    fi
}

# @fixme: wrong code
__trap_signals__()
{
    local code="${?}"

    if [ ${code} -ne 0 ] ; then
        local signal=$((${code} - 128))
        local name="`kill -l ${signal}`"

        >&2 printf "\nProcess ${BASHPID} received SIG${name} (${signal}), exiting...\n"
    fi
}

trap '__trap_exit__ ${?} ${LINENO}' ERR EXIT
trap '__trap_signals__ ${?}' SIGHUP SIGINT SIGQUIT SIGTERM

# ======================================================================================================================

declare -r _blue_="\e[34m"
declare -r _cyan_="\e[36m"
declare -r _default_="\e[0m"
declare -r _green_="\e[32m"
declare -r _light_yellow_="\e[93m"
declare -r _red_="\e[31m"

# @see https://unix.stackexchange.com/a/25907
declare -r _check_="\xE2\x9C\x94"
declare -r _cross_="\xE2\x9D\x8C"
declare -r _warning_="\xE2\x9A\xA0"

# ----------------------------------------------------------------------------------------------------------------------

date_now() { date "+%Y-%m-%d %H:%M:%S"; }

log_error()   { printf "${_red_}${2:-Error:}${_default_} ${1}\n"; }
log_info()    { printf "${_cyan_}${2:-Info:}${_default_} ${1}\n"; }
log_success() { printf "${_green_}${2:-Success:}${_default_} ${1}\n"; }
log_warning() { printf "${_light_yellow_}${2:-Warning:}${_default_} ${1}\n"; }

log_icon_check()   { log_success "${1}" "${_check_}"; }
log_icon_cross()   { log_error "${1}" "${_cross_}"; }
log_icon_warning() { log_warning "${1}" "${_warning_}"; }

log_hr()   {
    local char=${1:--}
    local times=${2:-80}
    printf "%${times}s\n" | sed "s/ /${char}/g"
}

# ----------------------------------------------------------------------------------------------------------------------

declare -r __FILE__="$(realpath "${0}")"
declare -r __SCRIPT__="$(basename "${__FILE__}")"
declare -r __ROOT__="$(realpath "$(dirname "${__FILE__}")")"

# ======================================================================================================================

log_info "started process ${BASHPID} at `date_now`\n" "Startup:"

git_tag()
{
    git rev-parse --abbrev-ref HEAD
}

docker_build()
{
    cd "${__ROOT__}" \
    && docker \
        build \
        --file docker/Dockerfile \
        --pull \
        --tag "jmjjg/cloudooo:`git_tag`" \
        .
}

bash()
{
    docker run \
        --interactive \
        --publish 8011:8011 \
        --tty \
        --volume "$(pwd)":/opt/cloudooo \
        jmjjg/cloudooo:`git_tag` \
        /bin/bash
}

run()
{
    docker run \
        --interactive \
        --publish 8011:8011 \
        --tty \
        --volume "$(pwd)":/opt/cloudooo \
        jmjjg/cloudooo:`git_tag`
}

usage()
{
    printf "NAME\n"
    printf "  %s\n" "${__SCRIPT__}"
    printf "\nEXEMPLES\n"
    printf "  %s build\n" "${__SCRIPT__}"
    printf "  %s bash\n" "${__SCRIPT__}"
    printf "  %s run\n" "${__SCRIPT__}"
}

(
    cd "${__ROOT__}"

    getopt -- t: "${@}" > /dev/null || ( echo "" ; >&2 usage ; >&2 printf "\nThe following parameters are not correct: %s\n" "${@}" ; exit 1 )
    params=""
    while test "${#}" -gt 0; do
        case "${1}" in
            -t)
                tag="${2}"
                shift 2
            ;;
            *)
                params="${params} ${1}"
                shift
            ;;
        esac
    done

    set -- ${params}
    while test "${#}" -gt 0 ; do
        case "${1}" in
            bash)
                bash
            ;;
            build)
                docker_build
                shift 1
            ;;
            run)
                run
            ;;
            *)
                >&2 usage
                >&2 printf "\nThe following parameters are not correct: %s\n" "${@}"
                exit 1
            ;;
        esac
    done
    exit 0
)
