package main

import (
	// sensors "flight-software/modules/sensors"
	telemetry "flight-software/modules/telemetry"
	// "fmt"
	// "time"
	// "bytes"
	"os"
)

// func main() {
// 	imu = sensors.InitIMU()
// 	time.Sleep(2 * time.Second)
// 	fmt.Println(imu.AccX())
// }

func main() {
	if os.Args[1] == "server" {
		 telemetry.TestServer()
	} else {
		telemetry.TestClient()
	}
}
