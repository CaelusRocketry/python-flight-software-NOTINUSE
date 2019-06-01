package sensors

import (
    "log"
    "time"

    "github.com/waltzofpearls/go-servo-picobber"
)

func main() {
    servoMin := 150 // Min pulse length out of 4096
    servoMax := 600 // Max pulse length out of 4096

    sv, err := servo.NewServo()
    if err != nil {
        log.Println(err)
    }
    sv.SetPwmFreq(60) // Set frequency to 60 Hz
    for {
        // Change speed of continuous servo on channel O
        sv.SetPwm(0, 0, servoMin)
        time.Sleep(1 * time.Second)
        sv.SetPwm(0, 0, servoMax)
        time.Sleep(1 * time.Second)
    }
}
