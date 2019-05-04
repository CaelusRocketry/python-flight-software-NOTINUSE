package main

import (
	telemetry "flight-software/modules/telemetry"
	"fmt"
	"time"
)

func main() {
	telemetry.TestServer()
	time.Sleep(3 * time.Second)
	fmt.Println("Starting Client")
	telemetry.TestClient()
}
