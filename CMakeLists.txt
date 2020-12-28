cmake_minimum_required( VERSION 3.0 ) # set min CMAKE version to 3.0

project( flight ) # project name

set (SOURCE_FILES
        "./src/main.cpp"
        "./src/modules/mcl/Supervisor.cpp"
        "./src/modules/mcl/Registry.cpp"
        "./src/modules/mcl/Flag.cpp"
        "src/modules/drivers/Telemetry.cpp"
        "src/modules/tasks/TelemetryTask.cpp"
        src/modules/tasks/SensorTask.cpp
        src/modules/tasks/ValveTask.cpp
        src/modules/drivers/Arduino.cpp
        src/modules/drivers/PseudoSensor.cpp
        src/modules/drivers/PseudoValve.cpp
        src/modules/control_tasks/TelemetryControl.cpp
        src/modules/control_tasks/SensorControl.cpp
        src/modules/control_tasks/ValveControl.cpp
        src/modules/control_tasks/ControlTask.cpp
        src/modules/control_tasks/StageControl.cpp
        src/modules/lib/Util.cpp
        src/modules/lib/Packet.cpp
        src/modules/lib/Kalman.cpp
        src/modules/lib/Log.cpp
        src/modules/control_tasks/PressureControl.cpp
        src/modules/mcl/Config.cpp)


set(CMAKE_CXX_STANDARD 11) # misc stuff
set(CMAKE_CXX_STANDARD_REQUIRED True)  # misc stuff
#set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -pthread")  # misc stuff
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -pthread")  # misc stuff

find_package(Boost REQUIRED COMPONENTS system)
include_directories( ${Boost_INCLUDE_DIR} )

include_directories( ./include ./src ./libs/Logger/include) # ALL directories than contain .h/.hpp files

add_executable( flight ${SOURCE_FILES}) # ALL .cpp files, first arg is output file, second arg is ALWAYS main.cpp

add_subdirectory( ./libs/Logger ) # external dependency
target_link_libraries( flight logger ${Boost_LIBRARIES} ) # tells cmake that the specified dependency library should be included in executable output file
