package sensors

type Sensor interface {
	name() string
	correct() bool
	safe() float32
	warning() float32
	critical() float32
	getData() string
}
