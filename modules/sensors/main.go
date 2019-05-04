package sensors

import (
	"fmt"
	"log"

	"periph.io/x/periph/conn/i2c"
	"periph.io/x/periph/conn/i2c/i2creg"
	"periph.io/x/periph/host"
)

// GetFromPort returns the value by the hex port command
func GetFromPort(byte port) []byte {
	// Make sure periph is initialized.
	if _, err := host.Init(); err != nil {
		log.Fatal(err)
	}

	// Use i2creg I²C bus registry to find the first available I²C bus
	b, err := i2creg.Open("")
	if err != nil {
		log.Fatal(err)
	}
	defer b.Close()

	// d is a valid conn.Conn
	d := &i2c.Dev{Addr: 68, Bus: b}

	// Send a command 0x10 and expect a 5 bytes reply
	write := []byte{0x00, port}
	read := make([]byte, 8)
	if err := d.Tx(write, read); err != nil {
		log.Fatal(err)
	}

	return read
}

func main() {
	fmt.Println("in Sensors package")
}
