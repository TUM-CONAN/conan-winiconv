from conan.packager import ConanMultiPackager
from conans import tools

if __name__ == "__main__":
    if tools.os_info.is_windows:
        builder = ConanMultiPackager(
            username="fw4spl", 
            visual_runtimes=["MD", "MDd"],
            archs=["x86_64"])
        builder.add_common_builds(shared_option_name=False, pure_c=True)
        builder.run()
    else:
        print("This package is only available on Windows")