package supervisor

import "time"
import sensor "flight-software/modules/sensors"
import blackbox "flight-software/modules/blackbox"
<<<<<<< HEAD
import "strconv"
import "fmt"
=======
>>>>>>> 9e7d2ecaea97dc61ae526b4a0987f652effd2fa6

var delay = 0.1

func Start() {
	iters := 0
	start := time.Now()
	setConstants()

	sensors := []sensor.Sensor
<<<<<<< HEAD
	sensors = append(sensors, sensor.InitIMU())
=======
	sensors = append(sensors, sensors.InitIMU())
>>>>>>> 9e7d2ecaea97dc61ae526b4a0987f652effd2fa6

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
//		blackbox.save(time.Now(), data)
<<<<<<< HEAD
		fmt.Println(strconv.ParseFloat(data))
=======
		fmt.Println(data)
>>>>>>> 9e7d2ecaea97dc61ae526b4a0987f652effd2fa6
		iters++
	}
}
