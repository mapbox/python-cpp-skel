import platform
import os
import tarfile
try:
    from urllib.request import urlretrieve
except ImportError:
    from urllib import urlretrieve
try:
    from configparser import ConfigParser
    from itertools import chain

    def read_config_file(filename):
        parser = ConfigParser()
        with open(filename) as lines:
            lines = chain(("[top]",), lines)  # This line does the trick.
            parser.read_file(lines)
        return parser.items('top')
except ImportError:
    from ConfigParser import ConfigParser
    from StringIO import StringIO

    def read_config_file(filename):
        parser = ConfigParser()
        with open(filename) as stream:
            stream = StringIO("[top]\n" + stream.read())  # This line does the trick.
            parser.readfp(stream)
        return parser.items('top')
    
def _set_default(config, key, default=None):
    value = os.environ.get(key.upper())
    if value is None:
        value = config.get(key, default)
    return value

class Mason:

    def __init__(self, **kwargs):
        self.mason_package_dir = _set_default(kwargs, 'mason_package_dir', "./mason_packages")
        self.mason_repository = _set_default(kwargs, 'mason_repository', "https://mason-binaries.s3.amazonaws.com")
        self.mason_command = _set_default(kwargs, 'mason_command', '.mason/mason')
        self.mason_platform = _set_default(kwargs, 'mason_platform')
        self.mason_platform_version = _set_default(kwargs, 'mason_platform_version')
        self.android_abi = _set_default(kwargs, 'android_abi')
        self.packages = {}
        self.uname = platform.system()
        if self.mason_platform is None:
            if self.uname == "Darwin":
                self.mason_platform = "osx"
            else:
                self.mason_platform = "linux"
        if self.mason_platform == "ios":
            self.mason_platform_version = "8.0"
        elif self.mason_platform == "android":
            if self.android_abi == "armeabi":
                self.mason_platform_version = "arm-v5-9"
            elif self.android_abi == "arm64-v8a":
                self.mason_platform_version = "arm-v8-21"
            elif self.android_abi == "x86":
                self.mason_platform_version = "x86-9"
            elif self.android_abi == "x86_64":
                self.mason_platform_version = "x86-64-21"
            elif self.android_abi == "mips":
                self.mason_platform_version = "mips-9"
            elif self.android_abi == "mips64":
                self.mason_platform_version = "mips64-21"
            else:
                self.mason_platform_version = "arm-v7-9"
        elif self.mason_platform_version is None:
            self.mason_platform_version = platform.machine()

    def use(self, package_name, version, header_only=False):
        if package_name in self.packages and self.packages[package_name]['version'] != version:
            raise Exception("[mason] Already using package " + package_name + " with version "+ self.packages[package_name]['version']+". Can not select version " + version)
        
        if header_only:
            platform_id = "headers"
        else:
            platform_id = "{0}-{1}".format(self.mason_platform, self.mason_platform_version)
        
        slug = "{0}/{1}/{2}".format(platform_id, package_name, version)
        install_path = os.path.join(self.mason_package_dir, slug)
        relative_path = os.path.relpath(install_path)
        
        if not os.path.isdir(install_path):
            cache_path = os.path.join(self.mason_package_dir, ".binaries", slug + ".tar.gz")
            cache_dir = os.path.dirname(cache_path)
            if not os.path.isdir(cache_dir):
                os.makedirs(cache_dir)
            if not os.path.exists(cache_path):
                url = "{0}/{1}.tar.gz".format(self.mason_repository, slug)
                print("[Mason] Downloading package " + url)
                urlretrieve(url, cache_path)
            print("[Mason] Unpacking package to "+ relative_path + "...")
            os.makedirs(install_path)
            tar = tarfile.open(cache_path)
            tar.extractall(install_path)
            tar.close()

        ini_file = os.path.join(install_path, "mason.ini")
        if not os.path.exists(ini_file):
            raise Exception("[Mason] Can not find mason.ini file at " + ini_file)
        
        package = {}
        package['prefix'] = package_name + " " + install_path
        config_info = read_config_file(ini_file)
        for (key, value) in config_info:
            key = key.lower()
            value = value.replace('{prefix}', install_path)
            if key == 'include_dirs' or key == 'static_libs':
                value = value.split(',')
            package[key] = value
        
        if version != package['version']:
            raise Exception("[Mason] Package at {0} has version {1}, but required {2}".format(install_path, package['version'], version))
        if package_name != package['name']:
            raise Exception("[Mason] Package at {0} has name {1}, but required {2}".format(install_path, package['name'], package_name))

        if not header_only:
            if self.mason_platform != package['platform']:
                raise Exception("[Mason] Package at {0} has platform {1}, but required {2}".format(install_path, package['platform'], self.mason_platform))
            if self.mason_platform_version != package['platform_version']:
                raise Exception("[Mason] Package at {0} has platform version {1}, but required {2}".format(install_path, package['platform_version'], self.mason_platform_verison))

        self.packages[package_name] = package

    def includes(self, package_name):
        return self.packages[package_name].get('include_dirs', [])
    
    def ldflags(self, package_name):
        if 'ldflags' in self.packages[package_name]:
            return self.packages[package_name]['ldflags'].split(' ')       
        return []


