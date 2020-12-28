// Ily anup
#include <Logger/logger_util.h> // external logging utility
#include <flight/modules/mcl/Supervisor.hpp> // Includes 'Supervisor' type

using namespace std; // allows access to standard library utilities

int main(int argc, char** argv) { // argc = len(argv) in python; char** argv = actual arguments
    log("INFO: Starting Application"); 
    
    Supervisor supervisor; // Creates a new instance of 'Supervisor'
    supervisor.initialize();
    supervisor.run();

    log("INFO: Created supervisor");

    return 0; // return exit code (0=application completed successfully)
}