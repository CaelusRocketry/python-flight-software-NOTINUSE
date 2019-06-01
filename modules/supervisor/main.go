package supervisor

import "time"
import sensor "flight-software/modules/sensors"

var delay = 0.1

func Start() {
	iters := 0
	start := time.Now()

	sensors := []sensor.Sensor
	sensors = append(sensors, sensors.InitIMU())

	for i := 0; i < 50; i++{
		for time.Since(start)-iters*delay < 0 {
			//wait until 200 nanoseconds have passed
		}
		var data = make(map[string]float64)
		for curr := range sensors {
			sensorname := curr.Name()
			//var reading = sensor.getData()
			reading := curr.GetData()
			data[sensorname] = reading
//			if !curr.corrected && (reading < curr.low || reading > curr.high) {
//				curr.correcting = true
//				go curr.correct()
				//determine if correction is critical or not,
				//do some correction in seperate thread,
				//flag correction once done
//			}
		}
//		telemetrypush(time.Now().Sub(start), data)
		fmt.Println(data)
		iters++
	}
}