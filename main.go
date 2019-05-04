package main

import (
<<<<<<< Updated upstream
	sensors "flight-software/modules/sensors"
	_ "flight-software/modules/telemetry"
	"fmt"
	"time"
)

func main() {
	imu = sensors.InitIMU()
	time.Sleep(2 * time.Second)
	fmt.Println(imu.AccX())

=======
	telemetry "flight-software/modules/telemetry"
	"os"
	// "fmt"
	// "time"
)

func main() {
	if os.Args[1] == "server" {
		 telemetry.TestServer()
	} else {
		telemetry.TestClient()
	}
>>>>>>> Stashed changes
}
