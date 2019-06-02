package sensors

type Sensor interface {
	Name() string
	Correct() bool
<<<<<<< HEAD
	Safe() float64
	Warning() float64
	Critical() float64
=======
	Safe() float32
	Warning() float32
	Critical() float32
>>>>>>> 9e7d2ecaea97dc61ae526b4a0987f652effd2fa6
	GetData() float64
	GetLevel() string
}
