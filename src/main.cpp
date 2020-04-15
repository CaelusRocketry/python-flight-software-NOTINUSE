#include <iostream> // printing I/O

#include <Logger/logger_util.h> // external logging utility

#include <flight/modules/mcl/Supervisor.hpp> // Includes 'Supervisor' type


using namespace std; // allows access to standard library utilities

int main(int argc, char** argv){ // argc = len(argv) in python; char** argv = actual arguments
    log("INFO: Starting Application"); 
    
    Supervisor* supervisor = new Supervisor(); // Creates a new instance of 'Supervisor'
    supervisor->initialize();
    supervisor->run();

    log("INFO: Created supervisor");

    /**
    Another way to write the above code block, using Pointers
    'Core*' defines a type that is a pointer to a 'Core' object
    '->' notation "dereferences" the pointer and accesses the method/variable of the object
    'cc->start' accesses the 'start' method attribute of 'Core' and the '()' executes the function

    Core* cc = new Core("core");
    cc->start();
    **/
    
    return 0; // return exit code (0=application completed successfully)
}