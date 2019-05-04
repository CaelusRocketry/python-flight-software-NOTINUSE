package main

import (
	"fmt"

	sensors "flight-software/modules/sensors"
)

func main() {
	x := sensors.X()
	fmt.Println(x)
}
