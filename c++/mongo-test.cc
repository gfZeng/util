#include "mongo/client/dbclient.h"

#include <cstdlib>
#include <iostream>


void
run(void)
{
    mongo::DBClientConnection c;
    c.connect("violet");
}

int
main(void)
{
    try {
	run();
	std::cout << "Connected ok!" << std::endl;
    } catch (const mongo::DBException &e) {
	std::cout << "caught " << e.what() << std::endl;
    }

    return EXIT_SUCCESS;
}
