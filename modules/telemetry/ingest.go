package telemetry

import (
  sensors "flight-software/modules/testsensors"
	//"fmt"
  "strings"
  "strconv"
)

var PASSWORD = "abc"
var ERROR = "NOO ERROR GO AWAY!"

func parse(msg string) string {
  parts := strings.Split(msg, " ")
  header := parts[0]
  cmd := parts[1]
  if header != PASSWORD {
    return ERROR
  }
  return strings.TrimSpace(cmd)
}

func Ingest(command string) string {
  command = parse(command)
  if command == ERROR {
    return ERROR
  }

  funcs := make(map[string] func() int)
  funcs["Temp"] = sensors.Temp
  funcs["Pressure"] = sensors.Pressure

  if value, ok := funcs[command]; ok {
    return  strconv.Itoa(value())
  }
  return "Unknown Command!"
}
