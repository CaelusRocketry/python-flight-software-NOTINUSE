package supervisor

import "time"

func Start() {
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
