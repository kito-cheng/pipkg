import subprocess
import importlib
import sys
import os

def _get_pip():
    # Find correct version of pip,
    # the order is pip<major>.<minor>, pip<major> then pip
    # Because we did't knwo which version are used for pip.
    pip_candidates = ['pip%s.%s' % (sys.version_info.major,
                                     sys.version_info.minor),
                      'pip%s' % sys.version_info.major,
                      'pip']
    if sys.platform.startswith("linux") or sys.platform.startswith('darwin'):
        prefixs = [os.path.join(os.environ['USER'], ".local", "bin")]
    else:
        prefixs = []

    if sys.executable:
        interpreter_path = os.path.dirname(sys.executable)
        prefix = interpreter_path + os.path.sep
        prefixs.append(prefix)

    prefixs.append("")

    for pip in pip_candidates:
        for prefix in prefixs:
            which_result = subprocess.Popen("which %s%s" % (prefix, pip),
                                            shell=True, stdout=subprocess.PIPE)
            pip_path = which_result.communicate()[0].strip()

            if len(pip_path) != 0:
                return pip_path
    # TODO: get pip from internet.
    raise Exception("pip not found!")

_pip_path = None

def _pip_install(package, upgrade=True, user=True):
    global _pip_path
    if _pip_path is None:
        _pip_path = _get_pip()
    upgrade_opt = "--upgrade" if upgrade else ""
    user_opt = "--user" if upgrade else ""
    subprocess.call("{pip} install {upgrade} {user} {package}".format(
                      pip=_pip_path, upgrade=upgrade_opt,
                      user=user_opt, package=package),
                    shell=True)

def check_package(package_name,
                  install_name=None,
                  always_update=False,
                  update_pip=True):

    if install_name is None:
        install_name = package_name

    pip = _get_pip()

    if always_update:
        if update_pip:
            _pip_install("pip", upgrade=True)

        _pip_install(install_name, upgrade=True)
    else:
        try:
            importlib.import_module(package_name)
        except ImportError:
            if update_pip:
               _pip_install("pip", upgrade=True)

            _pip_install(install_name, upgrade=False)
