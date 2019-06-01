package supervisor

import "time"

var delay = 0.01

func Start() {
	iters := 0
	start := time.Now()

	allSensors := 

	sensors := []SensorObj

	for {
		for time.Since(start)-iters*delay < 0 {
			//wait until 200 nanoseconds have passed
		}
		var data = make(map[string]float64)
		for curr := range sensors {
			sensorname := curr.name
			//var reading = sensor.getData()
			reading := curr.GetData()
			data[sensorname] = reading
			if !curr.corrected && (reading < curr.low || reading > curr.high) {
				curr.correcting = true
				go curr.correct()
				//determine if correction is critical or not,
				//do some correction in seperate thread,
				//flag correction once done
			}
		}
		telemetrypush(time.Now().Sub(start), data)
		iters++

	}
}

func (s *SensorObj) GetData() {

}
