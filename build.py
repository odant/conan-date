import platform, os
from subprocess import check_call
from conan.packager import ConanMultiPackager


# Common settings
username = "odant" if "CONAN_USERNAME" not in os.environ else None
# Windows settings
visual_versions = ["14", "15"] if "CONAN_VISUAL_VERSIONS" not in os.environ else None
visual_runtimes = ["MD", "MDd"] if "CONAN_VISUAL_RUNTIMES" not in os.environ else None


def filter_libcxx(builds):
    result = []
    for settings, options, env_vars, build_requires, reference in builds:
        if settings["compiler.libcxx"] == "libstdc++11":
            result.append([settings, options, env_vars, build_requires, reference])
    return result


if __name__ == "__main__":
    if os.environ.get('CONAN_DOCKER_IMAGE'):
        image = os.environ['CONAN_DOCKER_IMAGE']
        print("Installing tzdata in {}".format(image))
        modified_image = '{}-tzdata'.format(image)
        #check_call(['docker', 'pull', image])
        check_call(['docker', 'run', '--name', 'img', image, 'bash', '-c', 'sudo apt-get update && sudo apt-get install -qy tzdata'])
        check_call(['docker', 'commit', 'img', modified_image])
        os.environ['CONAN_DOCKER_IMAGE'] = modified_image
    #
    builder = ConanMultiPackager(
        username=username,
        visual_versions=visual_versions,
        visual_runtimes=visual_runtimes,
        exclude_vcvars_precommand=True
    )
    builder.add_common_builds(pure_c=False)
    # Adjusting build configurations
    builds = builder.items
    if platform.system() == "Linux":
        builds = filter_libcxx(builds)
    # Replace build configurations
    builder.items = []
    for settings, options, env_vars, build_requires, _ in builds:
        builder.add(
            settings=settings,
            options=options,
            env_vars=env_vars,
            build_requires=build_requires
        )
    builder.run()
