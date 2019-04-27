package main

import (
	"fmt"
	"time"
)

type Sensor struct {
	critlow, low, high, crithigh float64
	correcting                   bool
}

var sensors = map[string]Sensor{
	"Sensor1": Sensor{-100, 0, 100, 500, false},
	"Sensor2": Sensor{-100, 0, 100, 500, false},
}

func Telemetrypush(time int, data [string]float64) {
	fmt.Println(time, ":", data)
}

func Start() {
	data = {50, 50, 50, 50, 1000, 50, 50}
	for {
		start := time.Now()
		var data = make(map[string]float64)
		for sensorname, sensor := range sensors {
			//var reading = sensor.getData()
			reading := 0
			data[sensorname] = reading
			if !sensor.corrected && (reading < sensor.low || reading > sensor.high) {
				sensor.correcting = true
				 go sensor.correct()
				//determine if correction is critical or not,
				//do some correction in seperate thread,
				//flag correction once done
			}
		}
		telemetrypush(time.Now().Sub(start), data)
		for time.Since(start) < 200 {
			//wait until 200 nanoseconds have passed
		}
	}
}

func main() {
	Start()
}
