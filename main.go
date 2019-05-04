package main

import (
	sensors "flight-software/modules/sensors"
	_ "flight-software/modules/telemetry"
	"fmt"
	"time"
)

func main() {
	imu = sensors.InitIMU()
	time.Sleep(2 * time.Second)
	fmt.Println(imu.AccX())
}
