package main

import (
	// sensors "flight-software/modules/sensors"
	telemetry "flight-software/modules/telemetry"
	// "fmt"
	// "time"
	// "bytes"
	"os"
)

func main() {
	//	imu := sensors.InitIMU()
	//	for {
	//		time.Sleep(500 * time.Millisecond)
	//		fmt.Println(imu.Gyro())
	//	}
	if os.Args[1] == "server" {
		telemetry.TestServer()
	} else {
		telemetry.TestClient()
	}
}
