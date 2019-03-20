package main

import (
	"fmt"
	"io/ioutil"
	"os"
)

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
}

func main() {
	loadConfig()
}
