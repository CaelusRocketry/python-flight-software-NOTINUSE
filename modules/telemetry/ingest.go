package telemetry

import (
	"encoding/json"
	sensors "flight-software/modules/testsensors"
	"fmt"
	"strconv"
	"strings"
	"time"
	//"os"
)

var PASSWORD = "abc"
var ERROR = "NOO ERROR GO AWAY!"

func parse(pack Packet) string {
	header := pack.Header
	cmd := pack.Message
	if header != PASSWORD {
		return ERROR
	}
	return strings.TrimSpace(cmd)
}

func Ingest(pack Packet) string {
	command := parse(pack)
	if command == ERROR {
		return ERROR
	}

	funcs := make(map[string]func() int)
	funcs["Temp"] = sensors.Temp
	funcs["Pressure"] = sensors.Pressure

	fmt.Println(command)
	if value, ok := funcs[command]; ok {
		return strconv.Itoa(value())
	}
	if command == "ABORT" {
		return "ABORT"
	}
	return "Unknown Command!"
}

func Outqueue(header string, command string) {
	toOutqueue := Packet{
		Header:    header,
		Message:   command,
		Timestamp: time.Now(),
	}
	b, _ := json.Marshal(toOutqueue)
	s := string(b)
	fmt.Println(s)
	OUTQUEUE = append(OUTQUEUE, command)
}

type Packet struct {
	Message   string
	Header    string
	Timestamp time.Time
}

func Enqueue(header string, message string) {
	toEnqueue := Packet{
		Header:    header,
		Message:   message,
		Timestamp: time.Now(),
	}
	b, _ := json.Marshal(toEnqueue)
	s := string(b)
	fmt.Println(s)
	QUEUE = append(QUEUE, s)
}
