cmake_minimum_required( VERSION 3.0 ) # set min CMAKE version to 3.0

project( flight ) # project name

set (SOURCE_FILES
    "./src/main.cpp"
    "./src/modules/mcl/Supervisor.cpp"
        "./src/modules/mcl/Registry.cpp"
        "./src/modules/mcl/Flag.cpp")


set(CMAKE_CXX_STANDARD 11) # misc stuff
set(CMAKE_CXX_STANDARD_REQUIRED True)  # misc stuff

include_directories( ./include ./src ./libs/Logger/include) # ALL directories than contain .h/.hpp files

add_executable( flight ${SOURCE_FILES}) # ALL .cpp files, first arg is output file, second arg is ALWAYS main.cpp

add_subdirectory( ./libs/Logger ) # external dependency
target_link_libraries( flight logger ) # tells cmake that the specified dependency library should be included in executable output file