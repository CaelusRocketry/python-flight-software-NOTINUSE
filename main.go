package main

import (
	"fmt"
	"os"
)

func loadConfig() *os.File {
	var file *os.File
	if _, err := os.Stat("config_custom.yml"); err != nil && os.IsNotExist(err) {
		file, err = os.Open("config_default.yml")
		if err != nil {
			fmt.Println("Bad")
		}
	} else {
		file, _ = os.Open("config_custom.yml")
	}

	return file
}

func main() {
	config := loadConfig()
	fmt.Println(config.Name())
}
