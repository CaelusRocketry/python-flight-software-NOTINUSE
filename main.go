package main

import (
	"fmt"
	"io/ioutil"
	"os"

	"gopkg.in/yaml.v2"

	sensors "flight-software/modules/sensors"
)

// ConfigStruct represents the structure of the YAML configuration file.
type ConfigStruct struct {
	Main struct {
		Startup struct {
			Telemetry []string
		}
	}
	Modules struct {
		Telemetry struct {
		}
	}
}

func loadConfig() {
	var configFile *os.File
	if _, err := os.Stat("config_custom.yml"); err != nil && os.IsNotExist(err) {
		configFile, err = os.Open("config_default.yml")
		if err != nil {
			fmt.Println("Error occurred with reading 'config_default.yml'")
		}
	} else {
		configFile, _ = os.Open("config_custom.yml")
	}

	fmt.Println("Config filename:", configFile.Name())

	configBytes, _ := ioutil.ReadAll(configFile)
	fmt.Println(string(configBytes))

	config := ConfigStruct{}

	err := yaml.Unmarshal(configBytes, &config)
	if err != nil {
		fmt.Println("Error occured with generating YAML map")
	}

	fmt.Println(config.Main.Startup.Telemetry)
}

func main() {
	loadConfig()
	sensors.X()
}
