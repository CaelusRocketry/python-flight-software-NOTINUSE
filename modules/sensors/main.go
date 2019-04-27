package sensors

import (
	"fmt"
)

// Sensor represents a sensor.
type Sensor struct {
	critLow, low, high, critHigh float64
	isCorrecting                 bool
}

// Pitch = nil.
func Pitch() {
	fmt.Println("PITCH")
}
