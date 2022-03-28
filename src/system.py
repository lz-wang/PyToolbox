import platform


def get_os_type():
    return platform.system()


def get_os_sdk_build_number():
    return platform.version()


def get_os_version():
    # TODO: wait for Python fix this issue
    #    cannot use platform.release() on Windows 11
    if platform.version() in ['10.0.22000']:
        return '11'
    else:
        return platform.release()


def get_os_arch():
    return platform.architecture()[0]


def get_os_machine():
    return platform.machine()


if __name__ == "__main__":
    os = get_os_type()
    ver = get_os_version()
    arch = get_os_arch()
    machine = get_os_machine()
    print(os, ver, arch, machine)
