package supervisor

import "time"

type sensor struct {
	correted boolean
}

var delay = 0.01

func Start() {
	iters := 0
	start := time.Now()

	for {
		for time.Since(start)-iters*delay < 0 {
			//wait until 200 nanoseconds have passed
		}
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
		iters++

	}
}
