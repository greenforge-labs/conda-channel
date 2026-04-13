"""Patch cmake/DownloadExternal.cmake to use local pmc and xenium sources."""

import re
import sys


def patch_cmake(filepath):
    with open(filepath, "r") as f:
        content = f.read()

    # Replace robin_download_pmc function
    pmc_replacement = r"""function(robin_download_pmc)
	set(pmc_SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/pmc-local" PARENT_SCOPE)
	set(pmc_BINARY_DIR "${CMAKE_CURRENT_BINARY_DIR}/pmc-build" PARENT_SCOPE)
endfunction()"""

    content = re.sub(
        r"function\(robin_download_pmc\).*?endfunction\(\)",
        pmc_replacement,
        content,
        flags=re.DOTALL,
    )

    # Replace robin_download_xenium function
    xenium_replacement = r"""function(robin_download_xenium)
	add_library(xenium INTERFACE)
	target_include_directories(xenium
			INTERFACE
			$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/xenium-local>
			$<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>)

	install(
			TARGETS xenium
			EXPORT xeniumTargets
			ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
	)

	export(
			EXPORT xeniumTargets
			FILE ${CMAKE_CURRENT_BINARY_DIR}/xeniumTargets.cmake
			NAMESPACE xenium::
	)

	install(
			EXPORT xeniumTargets
			FILE xeniumTargets.cmake
			DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/xenium/
			NAMESPACE xenium::
	)
	install(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/xenium-local/xenium DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
endfunction()"""

    content = re.sub(
        r"function\(robin_download_xenium\).*?endfunction\(\)",
        xenium_replacement,
        content,
        flags=re.DOTALL,
    )

    with open(filepath, "w") as f:
        f.write(content)

    print(f"Patched {filepath}")


if __name__ == "__main__":
    patch_cmake(sys.argv[1])
