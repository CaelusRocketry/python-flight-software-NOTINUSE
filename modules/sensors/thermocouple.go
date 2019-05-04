package main
import (
	"fmt"
	"gopkg.in/yaml.v2"
	"io/ioutil"
	"path/filepath"
	"strconv"
	"bytes"
	"github.com/lunixbochs/struc.git"
	spi "golang.org/x/exp/io/spi"
  )

struct MAX31855 type{
//  Driver for MAX31855
	var devval string
	var modenum int
	var speednum int64
	dev, err := spi.Open(&spi.Devfs{
					Dev:      devval,
					Mode:     spi.Mode(modenum),
					MaxSpeed: speednum,
	})
	if err != nil {
					panic(err)
	}
}


    func (dev MAX31855) read(bool internal){

		if err := dev.Tx(nil, []byte{0x01}); err != nil {
			panic("thermocouple not connecteed")
		} 

		if err := dev.Tx(nil, []byte{0x02}); err != nil {
			panic("short circuit to ground")
		} 

    	if err := dev.Tx(nil, []byte{0x04}); err != nil {
			panic("short circuit to power")
		} 

        if err := dev.Tx([]byte{0x01}, nil); err != nil {
			panic("faulty reading")
		} 

		var buf []byte{}
		dev.Tx([]byte{0x01, 0x2, 0x3, 0x4}, buf)
    	out := []byte{}
		err = struc.Unpack(&buf, out)
		
        refer := out[4]
        temp := out[2]
        if internal{
            return refer
		}
        return temp
	}

    func (dev MAX31855) temperature() int{
		return dev.read(false) / 4
	}

    func (dev MAX31855) reference_temperature() int{
		return dev.read(true) * 0.625
	}

	func main(){
		fmt.Print("hi there")
	}